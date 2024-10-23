
import sys
import webbrowser
import requests
import os
import re
import time
import copy
import subprocess
from threading import Thread, Barrier, Timer, Lock
from collections import deque

from modules.downloaditem import DownloadItem
from collections import deque
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

from modules.utils import (clipboard_read, clipboard_write, size_format, validate_file_name, 
                           log, log_recorder, delete_file, time_format, truncate, notify, open_file, run_command, handle_exceptions)
from modules import config, brain, setting, video

from modules.video import(Video, ytdl, check_ffmpeg, download_ffmpeg, unzip_ffmpeg, get_ytdl_options, get_ytdl_options)

from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QThread
from PySide6.QtCore import QObject, QThread, Signal, Slot

from PySide6.QtGui import QAction, QIcon
# from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox, QVBoxLayout, 
                               QLabel, QProgressBar, QPushButton, QTextEdit, QHBoxLayout, QWidget, QFrame, QTableWidgetItem, 
                               QDialog, QComboBox, QInputDialog, QMenu)


class ClipboardWorker(QThread):
    def __init__(self):
        super().__init__()
        self.old_data = ''

    def run(self):
        while not config.terminate:
            new_data = clipboard_read()  # Read from the clipboard

            # Check if monitoring is active and clipboard content has changed
            if config.monitor_clipboard and new_data != self.old_data:
                if new_data.startswith('http') and ' ' not in new_data:
                    # Send the URL to the main window queue
                    config.main_window_q.put(('url', new_data))

                # Update old data
                self.old_data = new_data

            # Sleep briefly to avoid busy-waiting
            time.sleep(0.2)

   

class HeaderWorker(QThread):
    headers_refreshed = Signal(str)  # Signal to emit when headers are refreshed
    busy_cursor = Signal()  # Signal to indicate busy cursor
    normal_cursor = Signal()  # Signal to reset cursor

    def __init__(self, url):
        super().__init__()
        self.url = url
        

    def run(self):
        self.busy_cursor.emit()  # Set cursor to busy
        headers = self.get_header(self.url)  # Replace with your actual get_header method
        self.headers_refreshed.emit(headers)  # Emit the signal with the result
        self.normal_cursor.emit()  # Reset cursor when done

    def get_header(self, url):
        # Placeholder for the actual header fetching method
        # Replace this with the actual logic you want to use
        time.sleep(2)  # Simulate a time-consuming task
        return f"Headers for {url}"


class DownloadWorker(QObject):
    download_info_signal = Signal(dict)  # Signal to send download info

    def __init__(self, download_item):
        super().__init__()
        self.d = download_item  # Pass the download item (self.d) from MainWindow
        log(f"THIS IS US: {self.d}", log_level=3)
        

    def run(self):
        # Perform tasks, then emit signals with the data from self.d
        info = {
            'name': self.d.name,
            'total_size': self.d.total_size,
            'type': self.d.type,
            'protocol': self.d.protocol,
            'resumable': self.d.resumable,
            'total_speed': '',  # Add this if you have total_speed
        }
        self.download_info_signal.emit(info)


class MainWindow(QMainWindow):
    def __init__(self, d_list):
        QMainWindow.__init__(self)
        
        # current download_item
        self.d = DownloadItem()

        # Create the worker and pass self.d
        #self.worker = DownloadWorker(self.d)
        
        # download windows
        self.download_windows = {}  # dict that holds Download_Window() objects --> {d.id: Download_Window()}
        
        # url
        self.url_timer = None  # usage: Timer(0.5, self.refresh_headers, args=[self.d.url])
        self.bad_headers = [0, range(400, 404), range(405, 418), range(500, 506)]  # response codes
        # download
        self.pending = deque()
        self.disabled = True  # for download button

        # download list
        self.d_headers = ['id', 'name', 'progress', 'speed', 'time_left', 'downloaded', 'total_size', 'status', 'i']
        self.d_list = d_list  # list of DownloadItem() objects
        self.selected_row_num = None
        self._selected_d = None

        # update
        self.new_version_available = False
        self.new_version_description = None
        
        # youtube specific
        self.video = None
        self.yt_id = 0  # unique id for each youtube thread
        self.playlist = []
        self.pl_title = ''
        self.pl_quality = None
        self._pl_menu = []
        self._stream_menu = []
        self.stream_menu_selection = ''

        # thumbnail
        self.current_thumbnail = None

        self.url_timer = None


        # initial setup
        self.setup()
        ##########################################################################################

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        self.resize(500, 750)

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = config.APP_TITLE
        description = config.APP_NAME
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        #widgets.btn_save.clicked.connect(self.buttonClick)
        

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes/py_dracula_light.qss"


        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


        widgets.version.setText(f"{config.APP_VERSION}")
        widgets.titleLeftApp.setText(f"{config.APP_NAME}")
        widgets.titleLeftDescription.setText(f"{config.APP_DEC}")
        log('Starting PyIDM version:', config.APP_VERSION, 'Frozen' if config.FROZEN else 'Non-Frozen')
        # log('starting application')
        log('operating system:', config.operating_system_info)
        log('current working directory:', config.current_directory)

        # Call read_q periodically to process the queue
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_q)
        self.timer.start(100)  # Check the queue every 100ms


        # Starting QThreads 
        # Start the clipboard listener in a separate thread
        self.clipboard_worker = ClipboardWorker()
        self.clipboard_worker.start()

        
        # # Create the worker and pass self.d
        self.worker = DownloadWorker(self.d)
        # Start the worker thread
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        # Connect signals and slots
        self.worker.download_info_signal.connect(self.update_gui_slot)
        self.worker_thread.start()


    
    # BUTTONS CLICK
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_downloads":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_logs":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)


    def setup(self):
        """initial setup"""
        
        # download folder
        if not self.d.folder:
            self.d.folder = config.download_folder

    def read_q(self):
        """Read from the queue and update the GUI."""
        while not config.main_window_q.empty():
            k, v = config.main_window_q.get()

            if k == 'log':
                try:
                    contents = widgets.logDisplay.toPlainText()

                    
                    # print(size_format(len(contents)))
                    if len(contents) > config.max_log_size:
                        # delete 20% of contents to keep size under max_log_size
                        slice_size = int(config.max_log_size * 0.2)
                        widgets.logDisplay.setPlainText(contents[slice_size:])

                    widgets.logDisplay.append(v)
                except Exception as e:
                    log(f"{e}")

                #self.set_status(v.strip('\n'))

            elif k == 'url':
                # Update the QLineEdit with the new URL
                widgets.home_link_lineEdit.setText(v)
                print(f"Updated QLineEdit with URL: {v}")
                self.url_text_change()
                
            
            elif k == "download":
                self.start_download(*v)

            elif k == "monitor":
                widgets.monitor_clipboard.setChecked(v)


    # region Url stuffs
    def reset(self):
        # create new download item, the old one will be garbage collected by python interpreter
        self.d = DownloadItem()

        # reset some values
        self.playlist = []
        self.video = None


    def url_text_change(self):
        """Handle URL changes in the QLineEdit."""
        url = widgets.home_link_lineEdit.text().strip()
        if url == self.d.url:
            return

        self.reset()
        try:
            self.d.eff_url = self.d.url = url
            print(f"New URL set: {url}")
             
            # Update the DownloadItem with the new URL
            self.d.update(url)

            if isinstance(self.url_timer, QThread):
                self.url_timer.quit()  # Ensure any existing QThread is stopped

            # Start a new QThread for refreshing headers
            self.url_timer = HeaderWorker(url)
            self.url_timer.headers_refreshed.connect(self.handle_headers_refreshed)
            self.url_timer.busy_cursor.connect(lambda: self.change_cursor('busy'))
            self.url_timer.normal_cursor.connect(lambda: self.change_cursor('normal'))
            self.url_timer.start()  # Start the QThread


        except Exception as e:
            print(f"Error in url_text_change: {e}")

    def change_cursor(self, cursor_type):
        """Change cursor to busy or normal."""
        if cursor_type == 'busy':
            QApplication.setOverrideCursor(Qt.WaitCursor)  # Busy cursor
        elif cursor_type == 'normal':
            QApplication.restoreOverrideCursor()  # Restore normal cursor

    def handle_headers_refreshed(self, headers):
        """Handle the refreshed headers."""
        print(f"Headers refreshed: {headers}")


    @Slot(dict)
    def update_gui_slot(self, info):
        """Slot to handle updating the GUI elements with new download info."""
        print("Download info received:", info)  # Debug print

        widgets.home_filename_lineEdit.setText(info.get('name', ''))
        widgets.size_value_label.setText(size_format(info.get('total_size', 0)) if info.get('total_size') else "Unknown")
        widgets.type_value_label.setText(info.get('type', 'Unknown'))
        widgets.protocol_value_label.setText(info.get('protocol', 'Unknown'))
        widgets.resumable_value_label.setText("Yes" if info.get('resumable', False) else "No")
        widgets.totalSpeedValue.setText(f'⬇ {size_format(info["total_speed"], "/s")}' if info.get('total_speed', 0) != 0 else '⬇ 0 bytes')


    def get_header(self, url):
        # curl_headers = get_headers(url)
        self.d.update(url)

        # update headers only if no other curl thread created with different url
        if url == self.d.url:

            # update status code widget
            try:
                if self.d.status_code == 200:
                    cod = "ok"
                else:
                    cod = ""

                widgets.statusCodeValue.setText(f"{self.d.status_code} {cod}")
            except:
                pass
        
            # enable download button
            if self.d.status_code not in self.bad_headers and self.d.type != 'text/html':
                widgets.DownloadButton.setEnabled(True)

            # check if the link contains stream videos by youtube-dl
            Thread(target=self.youtube_func, daemon=True).start()

    def youtube_func(self):
        """Fetch metadata from YouTube and process it."""
        try:
            # Ensure youtube-dl is loaded
            if video.ytdl is None:
                log('youtube-dl module still loading, please wait')
                while not video.ytdl:
                    time.sleep(0.1)

            log(f"Extracting info for URL: {self.d.url}")
            # Extract information with youtube-dl
            with video.ytdl.YoutubeDL(get_ytdl_options()) as ydl:
                info = ydl.extract_info(self.d.url, download=False, process=False)
                log('Media info:', info, log_level=3)

                # Check if it's a playlist
                if info.get('_type') == 'playlist' or 'entries' in info:
                    pl_info = list(info.get('entries', []))
                    self.playlist = []
                    for item in pl_info:
                        url = item.get('url') or item.get('webpage_url') or item.get('id')
                        if url:
                            self.playlist.append(Video(url))

                    # Make sure the first video is valid
                    if self.playlist:
                        self.d = self.playlist[0]
                        log(f"Playlist processed. First video: {self.d.title}")
                    else:
                        log("Error: No valid videos found in playlist")
                        return

                else:
                    # Single video case
                    log("Processing single video")
                    video_obj = Video(self.d.url, vid_info=info)
                    if video_obj.title:  # Check if the video object is valid
                        self.playlist = [video_obj]
                        self.d = video_obj
                        log(f'Single video processed: {self.d.title}')
                    else:
                        log("Error: Single video extraction failed")
                        return

                # Update GUI elements
                self.update_pl_menu()
                self.update_stream_menu()

        except Exception as e:
            log('youtube_func()> error:', e)
            log('Error occurred on line:', sys.exc_info()[-1].tb_lineno)
            import traceback
            log('Traceback:', traceback.format_exc())

    def update_pl_menu(self):
        """Update the playlist combobox after processing."""
        try:
            log("Updating playlist menu")
            if not hasattr(self, 'playlist') or not self.playlist:
                log("Error: Playlist is empty or not initialized")
                return

            # Set the playlist combobox with video titles
            widgets.combo_setting_c.clear()  # Clear existing items
            for i, video in enumerate(self.playlist):
                if hasattr(video, 'title') and video.title:
                    widgets.combo_setting_c.addItem(f'{i + 1} - {video.title}')
                else:
                    log(f"Warning: Video at index {i} has no title")

            # Automatically select the first video in the playlist
            if self.playlist:
                self.playlist_OnChoice(self.playlist[0])

        except Exception as e:
            log(f"Error updating playlist menu: {e}")
            import traceback
            log('Traceback:', traceback.format_exc())

    def update_stream_menu(self):
        """Update the stream combobox after selecting a video."""
        try:
            log("Updating stream menu")
            if not hasattr(self, 'd') or not self.d:
                log("Error: No video selected")
                return
            
            if not hasattr(self.d, 'stream_names') or not self.d.stream_names:
                log("Error: Selected video has no streams")
                return

            # Set the stream combobox with available stream options
            widgets.stream_combo.clear()  # Clear existing items
            widgets.stream_combo.addItems(self.d.stream_names)

            # Automatically select the first stream
            if self.d.stream_names:
                selected_stream = self.d.stream_names[0]
                widgets.stream_combo.setCurrentText(selected_stream)
                self.stream_OnChoice(selected_stream)

        except Exception as e:
            log(f"Error updating stream menu: {e}")
            import traceback
            log('Traceback:', traceback.format_exc())



    def playlist_OnChoice(self, selected_video):
        """Handle playlist item selection."""
        if selected_video not in self.playlist:
            return

        # Find the selected video index and set it as the current download item
        index = self.playlist.index(selected_video)
        self.video = self.playlist[index]
        self.d = self.video  # Update current download item to the selected video

        # Update the stream menu based on the selected video
        self.update_stream_menu()

        # Optionally load the video thumbnail in a separate thread
        if config.show_thumbnail:
            Thread(target=self.video.get_thumbnail).start()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(config.d_list)
    window.show()
    sys.exit(app.exec())

