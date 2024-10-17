# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

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

from PySide6.QtCore import QTimer, Qt, QSize, QPoint
from PySide6.QtGui import QAction, QIcon

from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox, QVBoxLayout, 
                               QLabel, QProgressBar, QPushButton, QTextEdit, QHBoxLayout, QWidget, QFrame, QTableWidgetItem, 
                               QDialog, QComboBox, QInputDialog, QMenu)


class MainWindow(QMainWindow):
    def __init__(self, d_list):
        QMainWindow.__init__(self)


        # current download_item
        self.d = DownloadItem()

        

        # download windows
        self.download_windows = {}  # dict that holds Download_Window() objects --> {d.id: Download_Window()}

        # url
        self.url_timer = None  # usage: Timer(0.5, self.refresh_headers, args=[self.d.url])
        self.bad_headers = [0, range(400, 404), range(405, 418), range(500, 506)]  # response codes

        # youtube specific
        

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
        self.m_bar_lock = Lock()  # a lock to access a video quality progress bar from threads
        # self._s_bar = 0  # side progress bar for video quality loading
        self._m_bar = 0  # main playlist progress par
        self.stream_menu_selection = ''

        # thumbnail
        self.current_thumbnail = None


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

        # self.retry_button = widgets.home_retry_pushbutton  # Assuming this is defined in your UI
        # self.retry_button.clicked.connect(self.on_retry_clicked)  # Connect to the event handler

        # Initialize the PyQt run loop with a timer (to replace the PySimpleGUI event loop)
        self.run_timer = QTimer(self)
        self.run_timer.timeout.connect(self.run)
        self.run_timer.start(800)  # Runs every 500ms

        # self.retry_button_clicked = False
        # Flag to indicate if the filename is being updated programmatically
        self.filename_set_by_program = False

        widgets.home_retry_pushbutton.clicked.connect(self.retry)
        widgets.home_open_pushButton.clicked.connect(self.open_folder_dialog)
        widgets.home_folder_path_lineEdit.setText(config.download_folder)
        widgets.home_filename_lineEdit.textChanged.connect(self.on_filename_changed)
        widgets.DownloadButton.clicked.connect(self.on_download_button_clicked)
        
        #widgets.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
        # Enable custom context menu on the table widget
        widgets.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        widgets.tableWidget.customContextMenuRequested.connect(self.show_table_context_menu)
        
        

        

        log('Starting PyIDM version:', config.APP_VERSION, 'Frozen' if config.FROZEN else 'Non-Frozen')
        # log('starting application')
        log('operating system:', config.operating_system_info)
        log('current working directory:', config.current_directory)
        os.chdir(config.current_directory)

        # load stored setting from disk
        setting.load_setting()
        self.d_list = setting.load_d_list()

        # Add this line to set the checkbox state based on the loaded setting
        widgets.monitor_clipboard.setChecked(config.monitor_clipboard)
        widgets.checkBox2.setChecked(config.show_download_window)
        widgets.checkBox3.setChecked(config.auto_close_download_window)
        widgets.checkBox4.setChecked(config.show_thumbnail)
        
        widgets.combo_setting.setCurrentText('Global' if config.sett_folder == config.global_sett_folder else 'Local')
        seg_size = config.segment_size // 1024  # kb
        if seg_size >= 1024:
            seg_size = seg_size // 1024
            seg_size_unit = 'MB'
        else:
            seg_size_unit = 'KB'

        widgets.lineEdit_segment.setText(str(seg_size))
        widgets.segment_combo_setting.setCurrentText(seg_size_unit)
        # Connect the stateChanged signal of the checkbox to the update function

        
        widgets.lineEdit_network.setText(str(config.speed_limit) if config.speed_limit > 0 else "")
        widgets.checkBox_network.setChecked(True if config.speed_limit > 0 else False)
        widgets.combo_max_downloads.setCurrentText(str(config.max_concurrent_downloads))
        widgets.combo_max_connections.setCurrentText(str(config.max_connections))
        widgets.checkBox_proxy.setChecked(True if config.enable_proxy else False)
        widgets.lineEdit_proxy.setText(config.proxy if config.enable_proxy == True else "")
        widgets.combo_proxy_type.setCurrentText(config.proxy_type)
        
        


        

        
        




       


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
            #print(f"Processing queue: {k} -> {v}")

            if k == 'log':
                try:
                    contents = widgets.logDisplay.toPlainText()

                    
                    # print(size_format(len(contents)))
                    if len(contents) > config.max_log_size:
                        # delete 20% of contents to keep size under max_log_size
                        slice_size = int(config.max_log_size * 0.2)
                        widgets.logDisplay.setPlainText(contents[slice_size:])

                    # parse youtube output while fetching playlist info with option "process=True"
                    if '[download]' in v:  # "[download] Downloading video 3 of 30"
                        try:
                            b = v.rsplit(maxsplit=3)  # ['[download] Downloading video', '3', 'of', '30']
                            total_num = int(b[-1])
                            num = int(b[-3])

                            # get 50% of this value and the remaining 50% will be for other processing
                            percent = int(num * 100 / total_num)
                            percent = percent // 2

                            # # update media progress bar
                            # self.m_bar = percent

                            # # update playlist frame title
                            # self.window['playlist_frame'](
                            #     value=f'Playlist ({num} of {total_num} {"videos" if num > 1 else "video"}):')
                        except:
                            pass
                        

                    widgets.logDisplay.append(v)
                except Exception as e:
                    log(f"{e}")

                self.set_status(v.strip('\n'))

            elif k == 'url':
                # Update the QLineEdit with the new URL
                widgets.home_link_lineEdit.setText(v)
                #print(f"Updated QLineEdit with URL: {v}")
                # Thread(target=self.youtube_func, daemon=True).start()
                self.url_text_change()
                self.update_progress_bar()
            
            elif k == "download":
                self.start_download(*v)
            elif k == "monitor":
                widgets.monitor_clipboard.setChecked(v)

                

            


    def run(self):
        """Handle the event loop."""
        try:

            self.read_q()
            self.update_gui()  # You can also update the GUI components based on certain conditions
        except Exception as e:
            print(f"Error in run loop: {e}")

    # region Url stuffs
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
            #self.d.update(url)
            
            # schedule refresh header func
            if isinstance(self.url_timer, Timer):
                self.url_timer.cancel()  # cancel previous timer

            self.url_timer = Timer(0.5, self.refresh_headers, args=[url])
            self.url_timer.start()
            self.update_progress_bar()
        except Exception as e:
            print(f"Error in url_text_change: {e}")

    def process_url(self):
        """Simulate processing the URL and update the progress bar."""
        progress_steps = [10, 50, 100]  # Define the progress steps
        for step in progress_steps:
            time.sleep(1)  # Simulate processing time
            # Update the progress bar in the main thread
            self.update_progress_bar_value(step)
        self.update_gui()


    def update_progress_bar_value(self, value):
        """Update the progress bar value in the GUI."""
        try:
            widgets.progressBar.setValue(value)
            
        except Exception as e:
            print(f"Error updating progress bar: {e}")


    def retry(self):
        self.d.url = ''
        self.url_text_change()

    def reset(self):
        # create new download item, the old one will be garbage collected by python interpreter
        self.d = DownloadItem()

        # reset some values
        self.set_status('')
        self.playlist = []
        self.video = None


    def set_status(self, text):
        """update status bar text widget"""
        try:
            self.window['status_bar'](text)
        except:
            pass

    def update_progress_bar(self):
        """Update the progress bar based on URL processing."""
        # Start a new thread for the progress updates
        Thread(target=self.process_url, daemon=True).start()

    
    def refresh_headers(self, url):
        if self.d.url != '':
            #self.change_cursor('busy')
            Thread(target=self.get_header, args=[url], daemon=True).start()


    def get_header(self, url):
        # curl_headers = get_headers(url)
        self.d.update(url)

        # update headers only if no other curl thread created with different url
        if url == self.d.url:

    
            if self.d.status_code not in self.bad_headers and self.d.type != 'text/html':
                widgets.DownloadButton.setEnabled(True)

            # check if the link contains stream videos by youtube-dl
            Thread(target=self.youtube_func, daemon=True).start()


    # region download folder
    def open_folder_dialog(self):
        """Open a dialog to select a folder and update the line edit."""
        # Open a folder selection dialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")

        # If a folder is selected, update the line edit with the absolute path
        if folder_path:
            widgets.home_folder_path_lineEdit.setText(folder_path)
            config.download_folder = os.path.abspath(folder_path)
        else:
            # If no folder is selected, reset to the default folder (config.download_folder)
            widgets.home_folder_path_lineEdit.setText(config.download_folder)
    

    def on_filename_changed(self, text):
        """Handle manual changes to the filename line edit."""
        # Only update the download item if the change was made manually
        if not self.filename_set_by_program:
            self.d.name = text


    
    # region Update Gui
    def update_gui(self):
        """Update GUI elements with current download information."""
        try:
            # Update the filename only if it's different
            if widgets.home_filename_lineEdit.text() != self.d.name:
                self.filename_set_by_program = True  # Set the flag
                widgets.home_filename_lineEdit.setText(self.d.name)
                self.filename_set_by_program = False

            if self.d.status_code == 200:
                cod = "ok"
            else:
                cod = ""

            widgets.statusCodeValue.setText(f"{self.d.status_code} {cod}")

            # Update size label
            size_text = size_format(self.d.total_size) if self.d.total_size else "Unknown"
            widgets.size_value_label.setText(size_text)

            # Update the type label
            type_text = self.d.type
            widgets.type_value_label.setText(type_text)

            # Update the protocol label
            protocol_text = self.d.protocol
            widgets.protocol_value_label.setText(protocol_text)

            # Update the resumable label
            resumable_text = "Yes" if self.d.resumable else "No"
            widgets.resumable_value_label.setText(resumable_text)

            total_speed = 0
            for i in self.active_downloads:
                d = self.d_list[i]
                total_speed += d.speed
            
            if total_speed != 0:
                widgets.totalSpeedValue.setText((f'⬇ {size_format(total_speed, "/s")}'))
            else:
                widgets.totalSpeedValue.setText((f'⬇ 0 bytes'))

            # Fill table with download data
            self.populate_table()

            # Save setting to disk
            setting.save_setting()
            setting.save_d_list(self.d_list)

            self.check_scheduled()

            self.settings_folder()
            self.monitor_clip()
            self.show_download_win()
            self.auto_close_win()
        except Exception as e:
            log('MainWindow.update_gui() error:', e)
    

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

        # Update the GUI to reflect the current selection
        #self.update_gui()


    def stream_OnChoice(self, selected_stream):
        """Handle stream selection."""
        if selected_stream not in self.video.stream_names:
            selected_stream = self.video.stream_names[0]  # Default to the first stream

        self.video.selected_stream = self.video.streams[selected_stream]  # Set the selected stream
        #self.update_gui()  # Update the GUI to reflect the selected stream





# Define clipboard_listener and singleApp functions here

def clipboard_listener():
    old_data = ''
    
    while True:
        # Read from the clipboard
        new_data = clipboard_read()
        #print(f"Clipboard data: {new_data}")

        # Check if a message is received from another instance
        if new_data == 'any one there?':  
            clipboard_write('yes')  # Reply to the instance
            config.main_window_q.put(('visibility', 'show'))  # Request main window visibility

        # Check if clipboard monitoring is active and the content has changed
        if config.monitor_clipboard and new_data != old_data:
            if new_data.startswith('http') and ' ' not in new_data:
                # Send the URL to the main window queue
                config.main_window_q.put(('url', new_data))
            
            old_data = new_data
            #print(f"Updated clipboard data: {old_data}")

        # Stop the clipboard listener if needed
        if config.terminate:
            break

        # Sleep briefly to avoid busy-waiting
        time.sleep(0.2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow(config.d_list)
    window.show()
    
    Thread(target=video.import_ytdl, daemon=True).start()
        
    # Start the clipboard listener in a separate thread
    Thread(target=clipboard_listener, daemon=True).start()
    # Start logging
    Thread(target=log_recorder, daemon=True).start()


    
    # Start the event loop
    sys.exit(app.exec())
