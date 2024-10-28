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

from modules.utils import (clipboard_read, clipboard_write, size_format, validate_file_name, compare_versions, 
                           log, log_recorder, delete_file, time_format, truncate, notify, open_file, run_command, handle_exceptions)
from modules import config, brain, setting, video, update

from modules.video import(Video, ytdl, check_ffmpeg, download_ffmpeg, unzip_ffmpeg, get_ytdl_options, get_ytdl_options)

from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QThread, Signal, Slot, QUrl

from PySide6.QtGui import QAction, QIcon, QPixmap, QImage, QClipboard
from typing import Optional
from PySide6.QtWidgets import (QMainWindow, QApplication, QFileDialog, QMessageBox, QVBoxLayout, 
                               QLabel, QProgressBar, QPushButton, QTextEdit, QHBoxLayout, QWidget, QFrame, QTableWidgetItem, 
                               QDialog, QComboBox, QInputDialog, QMenu, QRadioButton, QButtonGroup, QHeaderView, QScrollArea, QCheckBox)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class YouTubeThread(QThread):
    finished = Signal(object)  # Signal to emit when the process is complete

    def __init__(self, url):
        super().__init__()
        self.url = url

    def change_cursor(self, cursor_type):
        """Change cursor to busy or normal."""
        if cursor_type == 'busy':
            QApplication.setOverrideCursor(Qt.WaitCursor)  # Busy cursor
        elif cursor_type == 'normal':
            QApplication.restoreOverrideCursor()  # Restore normal cursor

    def run(self):
        try:
            # Ensure youtube-dl is loaded
            if video.ytdl is None:
                log('youtube-dl module still loading, please wait')
                while not video.ytdl:
                    time.sleep(0.1)
            widgets.DownloadButton.setEnabled(False)
            log(f"Extracting info for URL: {self.url}")
            self.change_cursor('busy')
            # Extract information with youtube-dl
            with video.ytdl.YoutubeDL(get_ytdl_options()) as ydl:
                info = ydl.extract_info(self.url, download=False, process=False)
                log('Media info:', info, log_level=3)

                # Process the info and create Video objects
                if info.get('_type') == 'playlist' or 'entries' in info:
                    pl_info = list(info.get('entries', []))
                    playlist = []
                    for item in pl_info:
                        url = item.get('url') or item.get('webpage_url') or item.get('id')
                        if url:
                            playlist.append(Video(url))
                    result = playlist
                else:
                    result = Video(self.url, vid_info=None)

                self.finished.emit(result)
                self.change_cursor('normal')
                widgets.DownloadButton.setEnabled(True)
        except Exception as e:
            log('YouTubeThread error:', e)
            self.finished.emit(None)
    
        
class UpdateAppThread(QThread):
    app_update = Signal()
    def __ini__(self, remote=True):
        super().__init__()
        self.remote = remote
    
    def run(self):
        
        self.app_update.emit()


class FileOpenThread(QThread):
    # Define a signal to communicate with the main window
    critical_signal = Signal(str, str)

    def __init__(self, file_path, parent=None):
        super(FileOpenThread, self).__init__(parent)
        self.file_path = file_path

    def run(self):
        try:
            if not os.path.exists(self.file_path):
                # Emit the signal if the file doesn't exist, sending the title and message
                self.critical_signal.emit('File Not Found', f"The file '{self.file_path}' could not be found or has been deleted.")
                return  # Exit the thread if the file doesn't exist

            # Opening the file
            if config.operating_system == 'Windows':
                os.startfile(self.file_path)
            elif config.operating_system == 'Linux':
                run_command(f'xdg-open "{self.file_path}"', verbose=False)
            elif config.operating_system == 'Darwin':
                run_command(f'open "{self.file_path}"', verbose=False)

        except Exception as e:
            print(f'Error opening file: {e}')

class LogRecorderThread(QThread):
    error_signal = Signal(str)  # Signal to report errors to main thread
    
    def __init__(self):
        super().__init__()
        self.buffer = ''
        self.file = os.path.join(config.sett_folder, 'log.txt')
        
        # Clear previous file
        try:
            with open(self.file, 'w') as f:
                f.write(self.buffer)
        except Exception as e:
            self.error_signal.emit(f'Failed to clear log file: {str(e)}')
    
    def run(self):
        while not config.terminate:
            try:
                # Read log messages from queue
                q = config.log_recorder_q
                for _ in range(q.qsize()):
                    self.buffer += q.get()
                
                # Write buffer to file
                if self.buffer:
                    with open(self.file, 'a', encoding="utf-8", errors="ignore") as f:
                        f.write(self.buffer)
                        self.buffer = ''  # Reset buffer
                
                # Sleep briefly to prevent high CPU usage
                self.msleep(100)  # QThread's msleep is more precise than time.sleep
                
            except Exception as e:
                self.error_signal.emit(f'Log recorder error: {str(e)}')
                self.msleep(100)



class MainWindow(QMainWindow):
    update_gui_signal = Signal(dict)
    def __init__(self, d_list):
        QMainWindow.__init__(self)


        # current download_item
        self.d = DownloadItem()

        self.dragPos = None
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

        # Initialize and start log recorder thread
        self.log_recorder_thread = LogRecorderThread()
        self.log_recorder_thread.error_signal.connect(self.handle_log_error)
        self.log_recorder_thread.start()

        # Setup clipboard monitoring
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        self.old_clipboard_data = ''



        # Initialize the PyQt run loop with a timer (to replace the PySimpleGUI event loop)
        self.run_timer = QTimer(self)
        self.run_timer.timeout.connect(self.run)
        self.run_timer.start(900)  # Runs every 500ms

        # self.retry_button_clicked = False
        # Flag to indicate if the filename is being updated programmatically
        self.filename_set_by_program = False

        widgets.home_retry_pushbutton.clicked.connect(self.retry)
        widgets.home_open_pushButton.clicked.connect(self.open_folder_dialog)
        widgets.home_folder_path_lineEdit.setText(config.download_folder)
        widgets.home_filename_lineEdit.textChanged.connect(self.on_filename_changed)
        widgets.DownloadButton.clicked.connect(self.on_download_button_clicked)
        widgets.delete.clicked.connect(self.delete_btn)
        widgets.resume.clicked.connect(self.resume_btn)
        widgets.resume_all.clicked.connect(self.resume_all_downloads)
        widgets.cancel.clicked.connect(self.cancel_btn)
        widgets.refresh.clicked.connect(self.refresh_link_btn)
        widgets.d_window.clicked.connect(self.download_window)
        widgets.schedule_all.clicked.connect(self.schedule_all)
        widgets.stop_all.clicked.connect(self.stop_all_downloads)
        widgets.delete_all.clicked.connect(self.delete_all_downloads)
        widgets.update_button.clicked.connect(self.start_update)
        widgets.playlist_button.clicked.connect(self.download_playlist)
        # Enable custom context menu on the table widget
        widgets.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        widgets.tableWidget.customContextMenuRequested.connect(self.show_table_context_menu)
        widgets.clearButton.clicked.connect(self.clear_log)
        widgets.tableWidget.itemClicked.connect(self.update_item_label)

        # widgets.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        #widgets.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        # widgets.tableWidget.horizontalHeader().setStretchLastSection(True)
        # widgets.tableWidget.horizontalHeader().setDefaultSectionSize(150)  # Adjust column size if needed
        
        

        widgets.version.setText(f"{config.APP_VERSION}")
        widgets.version_label.setText(f"App Version: {config.APP_VERSION}")
        
        widgets.titleLeftApp.setText(f"{config.APP_NAME}")
        widgets.titleLeftDescription.setText(f"{config.APP_DEC}")

        log(f'Starting {config.APP_NAME} version:', config.APP_VERSION, 'Frozen' if config.FROZEN else 'Non-Frozen')
        # log('starting application')
        log('operating system:', config.operating_system_info)
        log('current working directory:', config.current_directory)
        os.chdir(config.current_directory)

        # load stored setting from disk
        setting.load_setting()
        self.d_list = setting.load_d_list()

        widgets.home_folder_path_lineEdit.setText(config.download_folder)

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
        widgets.combo_check_update.setCurrentText(str(config.update_frequency))
        #widgets.label_proxy_info.setText(config.proxy == '' if config.enable_proxy)
        

        self.update_gui_signal.connect(self.process_gui_updates)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.check_for_updates)
        self.update_timer.start(100)  # Check for updates every 100ms

        self.pending_updates = {}
        
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_thumbnail_downloaded)
        self.one_time = True
        

        

        
        




       


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

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()  # Use globalPosition() and convert to QPoint



    def on_clipboard_change(self):
        try:
            new_data = self.clipboard.text()
            
            # Check for instance message
            if new_data == 'any one there?':
                self.clipboard.setText('yes')
                self.show()
                self.raise_()
                return
            
            # Check for URLs if monitoring is active
            if config.monitor_clipboard and new_data != self.old_clipboard_data:
                if new_data.startswith('http') and ' ' not in new_data:
                    config.main_window_q.put(('url', new_data))
                
                self.old_clipboard_data = new_data
                
        except Exception as e:
            print(f'Clipboard error: {str(e)}')
    
    # def show_window(self):
    #     """Show and raise window"""
    #     self.show()
    #     self.raise_()
    
    def handle_clipboard_error(self, error_msg: str):
        """Handle clipboard errors"""
        log(error_msg)
    
    def handle_log_error(self, error_msg: str):
        """Handle log errors"""
        log(error_msg)
        
    def closeEvent(self, event):
        # Ensure clean shutdown of all threads
        config.terminate = True
        self.log_recorder_thread.wait()
        super().closeEvent(event)


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

                

            elif k == 'url':
                # Update the QLineEdit with the new URL
                widgets.home_link_lineEdit.setText(v)
                self.url_text_change()
                self.update_progress_bar()
            
            elif k == "download":
                self.start_download(*v)
            elif k == "monitor":
                widgets.monitor_clipboard.setChecked(v)
            
            elif k == 'show_update_gui':  # show update gui
                self.show_update_gui()

                

    def run(self):
        """Handle the event loop."""
        try:

            self.read_q()
            self.queue_updates()  # You can also update the GUI components based on certain conditions
            if self.one_time:
                self.one_time = False
                # check availability of ffmpeg in the system or in same folder with this script
                
                # check_for_update
                t = time.localtime()
                today = t.tm_yday  # today number in the year range (1 to 366)

                try:
                    days_since_last_update = today - config.last_update_check
                    log('days since last check for update:', days_since_last_update, 'day(s).')

                    if days_since_last_update >= config.update_frequency:
                        Thread(target=self.update_available, daemon=True).start()
                        Thread(target=self.check_for_ytdl_update, daemon=True).start()
                        config.last_update_check = today
                except Exception as e:
                    log('MainWindow.run()>', e)
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
            # Trigger the progress bar update and GUI refresh
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
        self.playlist = []
        self.video = None



    def update_progress_bar(self):
        """Update the progress bar based on URL processing."""
        # Start a new thread for the progress updates
        Thread(target=self.process_url, daemon=True).start()

    
    def refresh_headers(self, url):
        if self.d.url != '':
            #self.change_cursor('busy')
            Thread(target=self.get_header, args=[url], daemon=True).start()


    

    def get_header(self, url):
        self.d.update(url)

        if url == self.d.url:
            if self.d.status_code not in self.bad_headers and self.d.type != 'text/html':
                widgets.DownloadButton.setEnabled(True)

            # Use QThread for YouTube function
            self.yt_thread = YouTubeThread(url)
            self.yt_thread.finished.connect(self.on_youtube_finished)
            self.yt_thread.start()

    def on_youtube_finished(self, result):
        if isinstance(result, list):
            self.playlist = result
            if self.playlist:
                self.d = self.playlist[0]
        elif isinstance(result, Video):
            self.playlist = [result]
            self.d = result
        else:
            log("Error: YouTube extraction failed")
            self.change_cursor('normal')
            widgets.DownloadButton.setEnabled(True)
            widgets.combo_setting_c.clear()
            widgets.stream_combo.clear()
            self.reset_to_default_thumbnail()
            return

        self.update_pl_menu()
        self.update_stream_menu()

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
    def check_for_updates(self):
        if self.pending_updates:
            self.update_gui_signal.emit(self.pending_updates)
            self.pending_updates.clear()

    def queue_update(self, key, value):
        self.pending_updates[key] = value

    @Slot(dict)
    def process_gui_updates(self, updates):
        try:
            for key, value in updates.items():
                if key == 'filename':
                    if widgets.home_filename_lineEdit.text() != value:
                        self.filename_set_by_program = True
                        widgets.home_filename_lineEdit.setText(value)
                        self.filename_set_by_program = False
                elif key == 'status_code':
                    cod = "ok" if value == 200 else ""
                    widgets.statusCodeValue.setText(f"{value} {cod}")
                elif key == 'size':
                    size_text = size_format(value) if value else "Unknown"
                    widgets.size_value_label.setText(size_text)
                elif key == 'type':
                    widgets.type_value_label.setText(value)
                elif key == 'protocol':
                    widgets.protocol_value_label.setText(value)
                elif key == 'resumable':
                    widgets.resumable_value_label.setText("Yes" if value else "No")
                elif key == 'total_speed':
                    speed_text = f'⬇ {size_format(value, "/s")}' if value else '⬇ 0 bytes'
                    widgets.totalSpeedValue.setText(speed_text)
                elif key == 'populate_table':
                    self.populate_table()
                elif key == 'check_scheduled':
                    self.check_scheduled()
                elif key == 'settings_folder':
                    self.settings_folder()
                elif key == 'monitor_clip':
                    self.monitor_clip()
                elif key == 'show_download_win':
                    self.show_download_win()
                elif key == 'auto_close_win':
                    self.auto_close_win()
                elif key == 'show_thumb_nail':
                    self.show_thumb_nail()
                elif key == 'segment_size_set':
                    self.segment_size_set()
                elif key == 'speed_limit_set':
                    self.speed_limit_set()
                elif key == 'max_current_dl':
                    self.max_current_dl()
                elif key == 'max_connection':
                    self.max_connection()
                elif key == 'proxy_settings':
                    self.proxy_settings()
                elif key == 'pending_jobs':
                    self.pending_jobs()
                elif key == 'check_update_frequency':
                    self.check_update_frequency()
                elif key == 'set_log':
                    self.set_log()
               
               
            # Save settings (consider if this needs to be done every update)
            setting.save_setting()
            setting.save_d_list(self.d_list)

        except Exception as e:
            log('MainWindow.process_gui_updates() error:', e)

    def queue_updates(self):
        """Queue updates instead of directly modifying GUI"""
        self.queue_update('filename', self.d.name)
        self.queue_update('status_code', self.d.status_code)
        self.queue_update('size', self.d.total_size)
        self.queue_update('type', self.d.type)
        self.queue_update('protocol', self.d.protocol)
        self.queue_update('resumable', self.d.resumable)

        total_speed = sum(self.d_list[i].speed for i in self.active_downloads)
        self.queue_update('total_speed', total_speed)

        # Queue other updates
        self.queue_update('populate_table', None)
        self.queue_update('check_scheduled', None)
        self.queue_update('settings_folder', None)
        self.queue_update('monitor_clip', None)
        self.queue_update('show_download_win', None)
        self.queue_update('auto_close_win', None)
        self.queue_update('show_thumb_nail', None)
        self.queue_update('segment_size_set', None)
        self.queue_update('speed_limit_set', None)
        self.queue_update('max_current_dl', None)
        self.queue_update('max_connection', None)
        self.queue_update('proxy_settings', None)
        self.queue_update('pending_jobs', None)
        self.queue_update('check_update_frequency', None)
        self.queue_update('set_log', None)
        #self.queue_update('thumbnail', None)
    
    
    

        
     # Clear Log
    def clear_log(self):
        widgets.logDisplay.clear()

    # Set Log level 
    def set_log(self):
        config.log_level = int(widgets.logLevelComboBox.currentText())
        #log('Log Level changed to:', config.log_level)


    # region Start download
    @property
    def active_downloads(self):
        # update active downloads
        _active_downloads = set(d.id for d in self.d_list if d.status == config.Status.downloading)
        config.active_downloads = _active_downloads

        return _active_downloads
    
    def pending_jobs(self):
        # process pending jobs
        if self.pending and len(self.active_downloads) < config.max_concurrent_downloads:
            self.start_download(self.pending.popleft(), silent=True)
    
    def start_download(self, d, silent=False, downloader=None):
        if not self.check_internet():
            self.show_warning("No Internet","Please check your internet connection and try again")
            return
        

        if d is None:
            return
        
         # check for ffmpeg availability in case this is a dash video
        if d.type == 'dash' or 'm3u8' in d.protocol:
            # log('Dash video detected')
            if not self.ffmpeg_check():
                log('Download cancelled, FFMPEG is missing')
                return 'cancelled'
        

        folder = d.folder or config.download_folder
        # validate destination folder for existence and permissions
        # in case of missing download folder value will fallback to current download folder
        try:
            with open(os.path.join(folder, 'test'), 'w') as test_file:
                test_file.write('0')
            os.unlink(os.path.join(folder, 'test'))

            # update download item
            d.folder = folder
        except FileNotFoundError:
            self.show_information('Folder Error', 'Please enter a valid folder name', f'destination folder {folder} does not exist')
           
            return
        except PermissionError:
            self.show_information('Folder Error', f"you don't have enough permission for destination folder {folder}", f"you don't have enough permission for destination folder {folder}")
           
        except Exception as e:
            self.show_warning('Folder Error',f'problem in destination folder {repr(e)}')
        
        # validate file name
        if d.name == '':
            self.show_warning('Download Error', 'File name is invalid. Please enter a valid filename')
            
        
        # check if file with the same name exist in destination
        if os.path.isfile(d.target_file):
            #  show dialogue
            msg = QMessageBox.question(self, f"File Overwrite", f"File with the same name already exist in {d.folder}. \n Do you want to overwrite file?", QMessageBox.Yes | QMessageBox.No)

            # msg.setInformationText(f"")
            #msg = 'File with the same name already exist in ' + d.folder + '\n Do you want to overwrite file?'

            if msg != QMessageBox.Yes:
                log('Download cancelled by user')
                return 'cancelled'
            else:
                delete_file(d.target_file)
    

        # ------------------------------------------------------------------
        # search current list for previous item with same name, folder
        found_index = self.file_in_d_list(d.target_file)
        if found_index is not None: # might be zero, file already exist in d_list
            log('donwload item', d.num, 'already in list, check resume availability')
            d_from_list = self.d_list[found_index]
            d.id = d_from_list.id

            # default
            response = "Resume"

            if not silent:
                # show dialogue
                msg_text = (f'File with the same name: \n{self.d.name},\n already exists in download list\n'
                'Do you want to resume this file?\n'
                'Resume ==> continue if it has been partially downloaded ... \n'
                'Overwrite ==> delete old downloads and overwrite existing item... \n'
                'Note: if you need a fresh download, you have to change file name \n'
                'or target folder, or delete the same entry from the download list.')

                # Create a QMessageBox
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("File Already Exists")
                msg.setText(msg_text)

                # Add buttons
                resume_button = msg.addButton("Resume", QMessageBox.YesRole)
                overwrite_button = msg.addButton("Overwrite", QMessageBox.NoRole)
                cancel_button = msg.addButton("Cancel", QMessageBox.RejectRole)

                # Execute the dialog and get the result
                msg.exec()

                # Check which button was clicked
                if msg.clickedButton() == resume_button:
                    response = 'Resume'
                elif msg.clickedButton() == overwrite_button:
                    response = 'Overwrite'
                else:
                    response = 'Cancel'

            # Handle responses
            if response == 'Resume':
                log('resuming')

                # to resume, size must match, otherwise it will just overwrite
                if d.size == d_from_list.size:
                    log('resume is possible')
                    # get the same segment size
                    d.segment_size = d_from_list.segment_size
                    d.downloaded = d_from_list.downloaded
                else:
                    log(f'file: {d.name} has a different size and will be downloaded from beginning')
                    d.delete_tempfiles()

                # Replace old item in download list
                self.d_list[found_index] = d

            elif response == 'Overwrite':
                log('overwrite')
                d.delete_tempfiles()

                # Replace old item in download list
                self.d_list[found_index] = d

            else:
                log('Download cancelled by user')
                d.status = config.Status.cancelled
                return
            
        # ------------------------------------------------------------------
        else:
            print("new file")
            # generate unique id number for each download
            d.id = len(self.d_list)

            # add to download list
            self.d_list.append(d)

        # if max concurrent downloads exceeded, this download job will be added to pending queue
        if len(self.active_downloads) >= config.max_concurrent_downloads:
            d.status = config.Status.pending
            self.pending.append(d)
            return

        # start downloading
        if config.show_download_window and not silent:
            # create download window
            self.download_windows[d.id] = DownloadWindow(d)
            self.download_windows[d.id].show()  # Add this line

        # create and start brain in a separate thread
        Thread(target=brain.brain, daemon=True, args=(d, downloader)).start()


    def file_in_d_list(self, target_file):
        for i, d in enumerate(self.d_list):
            if d.target_file == target_file:
                return i
        return None
    
    
    
    def on_download_button_clicked(self, downloader=None):
        """Handle DownloadButton click event."""
        # Check if the download button is disabled
        if self.d.url == "":
            # Use QMessageBox to display the popup in PyQt
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Download Error')
            msg.setStyleSheet("background-color: rgb(33, 37, 43); color: white; width: 280px;")
            msg.setText('Nothing to download')
            msg.setInformativeText('It might be a web page or an invalid URL link.\nCheck your link or click "Retry".')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return
        
        #     return


        # Get a copy of the current download item (self.d)
        d = copy.copy(self.d)

        # Set the folder for download
        d.folder = config.download_folder  # Ensure that config.download_folder is properly set

        # Start the download using the appropriate downloader
        r = self.start_download(d, downloader=downloader)

        
        if r not in ('error', 'cancelled', False):
            self.change_page(btn=widgets.btn_widgets, btnName="btn_downloads", page=widgets.widgets)
            

        # else:
        #     if r is None:
        #         return
    
    def change_page(self, btn, btnName, page):
        # GET BUTTON CLICKED
        btn = btn

        # SHOW WIDGETS PAGE
        btnName = btnName
        widgets.stackedWidget.setCurrentWidget(page)
        UIFunctions.resetStyle(self, btnName)
        btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    # endregion

    # region youtube

    def show_thumbnail(self, thumbnail=None):
        """Show video thumbnail in thumbnail image widget in main tab, call without parameter to reset thumbnail."""
        print(f"Attempting to show thumbnail: {thumbnail}")

        try:
            if thumbnail is None or thumbnail == "":
                # Reset to default thumbnail if no new thumbnail is provided
                default_pixmap = QPixmap(":/icons/images/icons/thumbnail-default.png")
                widgets.home_video_thumbnail_label.setPixmap(default_pixmap.scaled(150, 150, Qt.KeepAspectRatio))
                log("Resetting to default thumbnail")
            elif thumbnail != self.current_thumbnail:
                self.current_thumbnail = thumbnail

                if thumbnail.startswith(('http://', 'https://')):
                    # If it's a URL, download the image
                    print(f"Downloading thumbnail from URL: {thumbnail}")
                    request = QNetworkRequest(QUrl(thumbnail))
                    self.network_manager.get(request)
                else:
                    # If it's a local file path
                    pixmap = QPixmap(thumbnail)
                    if not pixmap.isNull():
                        print(f"Loaded local thumbnail: {thumbnail}")
                        widgets.home_video_thumbnail_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
                    else:
                        print(f"Failed to load local thumbnail: {thumbnail}")
                        self.reset_to_default_thumbnail()

        except Exception as e:
            log('show_thumbnail() error:', e)
            self.reset_to_default_thumbnail()
    
    def on_thumbnail_downloaded(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            image = QImage()
            if image.loadFromData(data):
                pixmap = QPixmap.fromImage(image)
                widgets.home_video_thumbnail_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
                print("Successfully downloaded and set thumbnail")
            else:
                print("Failed to create image from downloaded data")
                self.reset_to_default_thumbnail()
        else:
            print(f"Error downloading thumbnail: {reply.errorString()}")
            self.reset_to_default_thumbnail()

    def reset_to_default_thumbnail(self):
        default_pixmap = QPixmap(":/icons/images/icons/thumbnail-default.png")
        widgets.home_video_thumbnail_label.setPixmap(default_pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        print("Reset to default thumbnail due to error")


    def ytdl_downloader(self):
        """Launch youtube-dl with proper command arguments."""
        
        # Check for youtube-dl executable in current folder if app is FROZEN
        if config.FROZEN:
            cmd = 'where youtube-dl' if config.operating_system == 'Windows' else 'which yt-dlp'
            error, output = run_command(cmd, verbose=True)
            if not error:
                ytdl_executable = output.strip()
            else:
                # Show dialog for missing youtube-dl
                msg = ('Alternative Download with youtube-dl\n'
                    'youtube-dl executable is required. To use this option,\n'
                    'please download the right version into the application folder,\n'
                    'i.e. "youtube-dl.exe" for Windows or "youtube-dl" for other OS.')
                
                dialog = QDialog(self)
                dialog.setWindowTitle('Youtube-dl missing')
                layout = QVBoxLayout(dialog)

                label = QLabel(msg)
                layout.addWidget(label)

                open_website_btn = QPushButton('Open website', dialog)
                cancel_btn = QPushButton('Cancel', dialog)
                
                layout.addWidget(open_website_btn)
                layout.addWidget(cancel_btn)

                def on_open_website():
                    webbrowser.open_new('https://github.com/ytdl-org/youtube-dl/releases/latest')
                    dialog.close()

                def on_cancel():
                    dialog.close()

                open_website_btn.clicked.connect(on_open_website)
                cancel_btn.clicked.connect(on_cancel)

                dialog.exec_()

                return  # exit if youtube-dl is missing
        else:
            ytdl_executable = f'"{sys.executable}" -m yt-dlp'

        # Preparing the download command
        d = self.d
        verbose = '-v' if config.log_level >= 3 else ''

        if not self.video:
            requested_format = 'best'
            name = os.path.join(config.download_folder, '%(title)s.%(ext)s').replace("\\", "/")
        else:
            name = d.target_file.replace("\\", "/")
            if d.type == 'dash':
                requested_format = f'"{d.format_id}"+"{d.audio_format_id}"/"{d.format_id}"+bestaudio/best'
            else:
                requested_format = f'"{d.format_id}"/best'

        # Creating command
        cmd = (f'{ytdl_executable} -f {requested_format} {d.url} -o "{name}" {verbose} '
            f'--hls-use-mpegts --ffmpeg-location {config.ffmpeg_actual_path} --proxy "{config.proxy}"')
        log('cmd:', cmd)

        # Execute the command
        if config.operating_system == 'Windows':
            # Write a batch file to start a new cmd terminal
            batch_file = os.path.join(config.current_directory, 'ytdl_cmd.bat')
            with open(batch_file, 'w') as f:
                f.write(cmd + '\npause')

            # Execute the batch file
            os.startfile(batch_file)
        else:
            # For Linux/macOS (not tested)
            subprocess.Popen([os.getenv('SHELL'), '-i', '-c', cmd])
    


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
        print(f"This is the thumbnails url {self.video.thumbnail_url}")
        self.d = self.video  # Update current download item to the selected video

        # Update the stream menu based on the selected video
        self.update_stream_menu()

        # Optionally load the video thumbnail in a separate thread
        if config.show_thumbnail:
            Thread(target=self.video.get_thumbnail).start()
        
            self.show_thumbnail(thumbnail=self.video.thumbnail_url)
        
        # Update the GUI to reflect the current selection
        #self.update_gui()


    def stream_OnChoice(self, selected_stream):
        """Handle stream selection."""
        if selected_stream not in self.video.stream_names:
            selected_stream = self.video.stream_names[0]  # Default to the first stream
        # else: 
        #     selected_stream = widgets.stream_combo.setCurrentText(self.video.stream_names)

        self.video.selected_stream = self.video.streams[selected_stream]  # Set the selected stream
        #self.update_gui()  # Update the GUI to reflect the selected stream

    def download_playlist(self):
        """Download playlist with video stream selection using PyQt."""

        # Check if there is a video file or quit
        if not self.video:
            self.show_information("Play Download", "Please check the url",  "Playlist is empty, nothing to download :", )
            #QMessageBox.information(self, "Playlist Download", "Playlist is empty, nothing to download :)")
            return

        # Prepare lists for video and audio streams
        mp4_videos = {}
        other_videos = {}
        audio_streams = {}

        # Collect streams from all videos in playlist
        for video in self.playlist:
            mp4_videos.update({stream.raw_name: stream for stream in video.mp4_videos.values()})
            other_videos.update({stream.raw_name: stream for stream in video.other_videos.values()})
            audio_streams.update({stream.raw_name: stream for stream in video.audio_streams.values()})

        # Sort streams based on quality
        mp4_videos = {k: v for k, v in sorted(mp4_videos.items(), key=lambda item: item[1].quality, reverse=True)}
        other_videos = {k: v for k, v in sorted(other_videos.items(), key=lambda item: item[1].quality, reverse=True)}
        audio_streams = {k: v for k, v in sorted(audio_streams.items(), key=lambda item: item[1].quality, reverse=True)}

        raw_streams = {**mp4_videos, **other_videos, **audio_streams}

        # Create a QDialog
        dialog = QDialog(self)
        dialog.setStyleSheet("""
            QWidget {
                background-color: rgb(33, 37, 43);
                color: white;
                
            }
        """)
        
        dialog.setWindowTitle('Playlist Download')
        layout = QVBoxLayout(dialog)

        # Master stream combo box
        master_stream_menu = ['● Video streams:'] + list(mp4_videos.keys()) + list(other_videos.keys()) + \
                            ['', '● Audio streams:'] + list(audio_streams.keys())
        master_stream_combo = QComboBox()
        master_stream_combo.addItems(master_stream_menu)

        # General options layout
        select_all_checkbox = QCheckBox('Select All')
        general_options_layout = QHBoxLayout()
        general_options_layout.addWidget(select_all_checkbox)
        general_options_layout.addWidget(QLabel('Choose quality for all videos:'))
        general_options_layout.addWidget(master_stream_combo)

        layout.addLayout(general_options_layout)

        # Video layout inside a scrollable area
        scroll_area = QScrollArea(dialog)
        scroll_content = QFrame()
        scroll_layout = QVBoxLayout(scroll_content)

        video_checkboxes = []
        stream_combos = []

        for num, video in enumerate(self.playlist):
            # Create a checkbox for each video
            video_checkbox = QCheckBox(video.title[:40], scroll_content)
            video_checkbox.setToolTip(video.title)
            video_checkboxes.append(video_checkbox)

            # Create a combo box for stream selection
            stream_combo = QComboBox(scroll_content)
            stream_combo.addItems(video.raw_stream_menu)
            stream_combos.append(stream_combo)

            # Size label
            size_label = QLabel(size_format(video.total_size), scroll_content)

            # Create a row for each video
            video_row = QHBoxLayout()
            video_row.addWidget(video_checkbox)
            video_row.addWidget(stream_combo)
            video_row.addWidget(size_label)

            scroll_layout.addLayout(video_row)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(250)

        layout.addWidget(scroll_area)

        # OK and Cancel buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton('OK', dialog)
        cancel_button = QPushButton('Cancel', dialog)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        # Handle button actions
        def on_ok():
            chosen_videos = []
            for num, video in enumerate(self.playlist):
                selected_text = stream_combos[num].currentText()
                video.selected_stream = video.raw_streams[selected_text]
                print("Available keys in raw_streams:", video.raw_streams.keys())
                print("Selected text:", selected_text)

                if video_checkboxes[num].isChecked():
                    chosen_videos.append(video)

            dialog.accept()

            # Start download for the selected videos
            for video in chosen_videos:
                video.folder = config.download_folder
                self.start_download(video, silent=True)

        def on_cancel():
            dialog.reject()

        # Connect button actions
        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(on_cancel)

        # Select All functionality
        def on_select_all():
            for checkbox in video_checkboxes:
                checkbox.setChecked(select_all_checkbox.isChecked())

        select_all_checkbox.stateChanged.connect(on_select_all)

        # Master stream selection changes all streams
        def on_master_stream_combo_change():
            selected_text = master_stream_combo.currentText()
            if selected_text in raw_streams:
                for num, stream_combo in enumerate(stream_combos):
                    video = self.playlist[num]
                    if selected_text in video.raw_streams:
                        stream_combo.setCurrentText(selected_text)
                        video.selected_stream = video.raw_streams[selected_text]

        master_stream_combo.currentTextChanged.connect(on_master_stream_combo_change)

        # Show the dialog and process result
        if dialog.exec():
            self.change_page(btn=widgets.btn_widgets, btnName="btn_downloads", page=widgets.widgets)
   
   
    def ffmpeg_check(self):
        """Check if ffmpeg is available, if not, prompt user to download."""
        
        if not check_ffmpeg():
            if config.operating_system == 'Windows':
                # Create the dialog
                dialog = QDialog(self)
                dialog.setWindowTitle('FFmpeg is missing')

                # Layout setup
                layout = QVBoxLayout(dialog)

                # Label for missing FFmpeg
                label = QLabel('"ffmpeg" is missing!! and needs to be downloaded:\n')
                layout.addWidget(label)

                # Radio buttons for choosing destination folder
                recommended_radio = QRadioButton(f"Recommended: {config.global_sett_folder}")
                recommended_radio.setChecked(True)
                local_radio = QRadioButton(f"Local folder: {config.current_directory}")

                # Group radio buttons
                radio_group = QButtonGroup(dialog)
                radio_group.addButton(recommended_radio)
                radio_group.addButton(local_radio)

                # Layout for radio buttons
                radio_layout = QVBoxLayout()
                radio_layout.addWidget(recommended_radio)
                radio_layout.addWidget(local_radio)

                layout.addLayout(radio_layout)

                # Buttons for Download and Cancel
                button_layout = QHBoxLayout()
                download_button = QPushButton('Download')
                cancel_button = QPushButton('Cancel')
                button_layout.addWidget(download_button)
                button_layout.addWidget(cancel_button)

                layout.addLayout(button_layout)

                # Set layout and show the dialog
                dialog.setLayout(layout)

                # Handle button actions
                def on_download():
                    selected_folder = config.global_sett_folder if recommended_radio.isChecked() else config.current_directory
                    download_ffmpeg(destination=selected_folder)
                    dialog.accept()  # Close the dialog after download

                def on_cancel():
                    dialog.reject()  # Close dialog on cancel

                # Connect button signals
                download_button.clicked.connect(on_download)
                cancel_button.clicked.connect(on_cancel)

                # Execute the dialog
                dialog.exec_()

            else:
                # Show error popup for non-Windows systems
                QMessageBox.critical(self, 
                                    'FFmpeg is missing',
                                    '"ffmpeg" is required to merge an audio stream with your video.\n'
                                    'Executable must be copied into the PyIDM folder or add the ffmpeg path to system PATH.\n'
                                    'You can download it manually from https://www.ffmpeg.org/download.html.')

            return False
        else:
            return True
    # endregion

    # region downloads page
    @property
    def selected_d(self):
        self._selected_d = self.d_list[self.selected_row_num] if self.selected_row_num is not None else None
        return self._selected_d

    @selected_d.setter
    def selected_d(self, value):
        self._selected_d = value

    @staticmethod
    def format_cell_data(k, v):
        """take key, value and prepare it for display in cell"""
        if k in ['size', 'total_size', 'downloaded']:
            v = size_format(v)
        elif k == 'speed':
            v = size_format(v, '/s')
        elif k in ('percent', 'progress'):
            v = f'{v}%' if v else '---'
        elif k == 'time_left':
            v = time_format(v)
        elif k == 'resumable':
            v = 'yes' if v else 'no'
        elif k == 'name':
            v = validate_file_name(v)

        return v
    
    def populate_table(self):
        # Populate table with formatted data from d_list
        for row, d in enumerate(self.d_list):
            # Set the ID column (use row + 1 or d.id if available)
            id_item = QTableWidgetItem(str(row + 1))  # Row number starts from 1
            widgets.tableWidget.setItem(row, 0, id_item)  # First column is ID
            
            # Fill the remaining columns based on the d_headers
            for col, key in enumerate(self.d_headers[1:], 1):  # Skip 'id', already handled
                cell_value = self.format_cell_data(key, getattr(d, key, ''))
                item = QTableWidgetItem(cell_value)
                widgets.tableWidget.setItem(row, col, item)
        # Enable manual resizing by the user
        # widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # widgets.tableWidget.horizontalHeader().setStretchLastSection(True)
        # widgets.tableWidget.horizontalHeader().setDefaultSectionSize(150)

    # endregion

    # region downloads functions
    def show_critical(self,title, msg):
        critical_box = QMessageBox(self)
        critical_box.setStyleSheet("background-color: rgb(33, 37, 43); color: white;")
        critical_box.setWindowTitle(title)
        critical_box.setText(msg)
        critical_box.setIcon(QMessageBox.Critical)
        critical_box.setStandardButtons(QMessageBox.Ok)
        critical_box.exec()

    def show_warning(self,title, msg):
        warning_box = QMessageBox(self)
        warning_box.setStyleSheet("background-color: rgb(33, 37, 43); color: white;")
        warning_box.setWindowTitle(title)
        warning_box.setText(msg)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec()

    def show_information(self, title, inform, msg):
        information_box = QMessageBox(self)
        information_box.setStyleSheet("background-color: rgb(33, 37, 43); color: white;")
        information_box.setText(msg)
        information_box.setWindowTitle(title)
        information_box.setInformativeText(inform)
        information_box.setIcon(QMessageBox.Information)
        information_box.setStandardButtons(QMessageBox.Ok)
        information_box.exec()
        #QMessageBox.information(self, 'Error', "To open download window offline \n go to setting tab, then uncheck auto close download window", QMessageBox.Ok)
        return

    def check_internet(self):
        """Check if the system has internet connectivity."""

        # initializing URL
        url = "https://www.google.com"
        timeout = 10
        try:
            # requesting URL
            request = requests.get(url,
                                timeout=timeout)
            log("Internet is on")
            return True
        # catching exception
        except (requests.ConnectionError,
                requests.Timeout) as exception:
            log("Internet is off")
        

    def resume_btn(self):
        # Ensure a row is selected
        selected_row = widgets.tableWidget.currentRow()

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        # Now, self.selected_d should be properly set by the property
        if self.selected_d is None:
            self.show_warning("Error","No download item selected")
            # QMessageBox.warning(self, 'Error', "No download item selected.", QMessageBox.Ok)
            # return

        # Check if there is internet connectivity
        if not self.check_internet():
            self.show_warning("No Internet","Please check your internet connection and try again")
            # QMessageBox.warning(self, 'No Internet', "Please check your internet connection and try again.", QMessageBox.Ok)
            # return

        # If everything is good, resume the download
        # try:
        self.start_download(self.selected_d, silent=True)
        # except Exception as e:
        #     QMessageBox.critical(self, 'Error', f"An error occurred while resuming the download: {e}", QMessageBox.Ok)


        
    def cancel_btn(self):
        selected_row = widgets.tableWidget.currentRow()
        if selected_row < 0 or selected_row >= len(self.d_list):
           self.show_warning("Error","No download item selected")

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        if self.selected_row_num is None:
            return

        d = self.selected_d
        if d.status == config.Status.completed:
            return

        d.status = config.Status.cancelled

        if d.status == config.Status.pending:
            self.pending.pop(d.id)

    def refresh_link_btn(self):
        selected_row = widgets.tableWidget.currentRow()
        if selected_row < 0 or selected_row >= len(self.d_list):
           self.show_warning("Error","No download item selected")

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        if self.selected_row_num is None:
            return

        d = self.selected_d
        config.download_folder = d.folder

        widgets.home_link_lineEdit.setText(d.url)
        self.url_text_change()

        widgets.home_folder_path_lineEdit.setText(config.download_folder)
        self.change_page(btn=widgets.btn_home, btnName="btn_home", page=widgets.home)
        
    def download_window(self):
        selected_row = widgets.tableWidget.currentRow()
        
        if selected_row < 0 or selected_row >= len(self.d_list):
            self.show_warning("Error","No download item selected")
        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        if self.selected_d:
            if config.auto_close_download_window and self.selected_d.status != config.Status.downloading:
                self.show_information(title='Information',inform="", msg="To open download window offline \n go to setting tab, then uncheck auto close download window")
    
                
                
            else:
                d = self.selected_d
                if d.id not in self.download_windows:
                    self.download_windows[d.id] = DownloadWindow(d=d)
                else:
                    self.download_windows[d.id].focus()

    def stop_all_downloads(self):
        # change status of pending items to cancelled
        for d in self.d_list:
            d.status = config.Status.cancelled

        self.pending.clear()

    def resume_all_downloads(self):
        # change status of all non completed items to pending
        for d in self.d_list:
            if d.status == config.Status.cancelled:
                self.start_download(d, silent=True)

    
    def delete_btn(self):
        selected_items = widgets.tableWidget.selectedItems()
        if not selected_items:
            return

        selected_row = widgets.tableWidget.currentRow()

        # Assuming self.d_list is your list of download items
        if self.active_downloads:
            self.show_critical("Error","Can't delete items while downloading. Stop or cancel all downloads first!")
            return
            

        msg = f"Warning!!!\nAre you sure you want to delete {self.d_list[selected_row].name}?"
        confirmation_box = QMessageBox(self)
        confirmation_box.setStyleSheet("background-color: rgb(33, 37, 43); color: white;")
        confirmation_box.setWindowTitle('Delete file?')
        confirmation_box.setText(msg)
        confirmation_box.setIcon(QMessageBox.Question)
        confirmation_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = confirmation_box.exec_()

        if reply != QMessageBox.Yes:
            return

        try:
            # Remove the item from the list and update the table
            d = self.d_list.pop(selected_row)

            # Update the remaining items' IDs
            for i, item in enumerate(self.d_list):
                item.id = i

            # Log the deleted item (for debugging)
            log(f"D:  {d}")

            # Remove the row from the table
            widgets.tableWidget.removeRow(selected_row)

            notification = f"File: {d.name} has been deleted."
            notify(notification, title=f'{config.APP_NAME} - Download completed')
            d.delete_tempfiles()

        except Exception as e:
            log(f"Error deleting item: {e}")

    def delete_all_downloads(self):
        # Check if there are any active downloads
        if self.active_downloads:
            self.show_critical("Error","Can't delete items while downloading. Stop or cancel all downloads first!")
            return

        # Confirmation dialog - user has to write "delete" to proceed
        msg = 'Delete all items and their progress temp files\n Type the word "delete" and hit OK to proceed.'
        input_dialog = QInputDialog.getText(self, 'Warning!!', msg)
        #input_dialog[0].setStyleSheet("background-color: rgb(33, 37, 43); color: white;")  # Apply the stylesheet

        

        

        # Unpack the response and the 'OK' status
        response, ok = input_dialog
        if not ok or response != 'delete':
            return

        # Log the deletion process
        log('Start deleting all download items')

        # Stop all downloads
        self.stop_all_downloads()

        # Reset selected item number
        self.selected_row_num = None

        # Get the number of downloads
        n = len(self.d_list)

        # Delete temp files for each download in a separate thread
        for i in range(n):
            d = self.d_list[i]
            Thread(target=d.delete_tempfiles, daemon=True).start()

        # Clear the download list
        self.d_list.clear()

        # Optionally, update the UI (e.g., clearing table rows)
        widgets.tableWidget.setRowCount(0)


    def check_scheduled(self):
        t = time.localtime()
        c_t = (t.tm_hour, t.tm_min)
        for d in self.d_list:
            if d.sched and d.sched[0] <= c_t[0] and d.sched[1] <= c_t[1]:
                self.start_download(d, silent=True)  # send for download
                d.sched = None  # cancel schedule time

    def schedule_all(self):
        try:
            response = ask_for_sched_time('Download scheduled for...')

            if response:
                for d in self.d_list:
                    if d.status in (config.Status.pending, config.Status.cancelled):
                        d.sched = response
                        log(f'Scheduled {d.name} for {response[0]}:{response[1]}')
        except Exception as e:
            log(f'Error in scheduling: {e}')

    
    

    def show_table_context_menu(self, pos: QPoint):
        # Get the position of the click (row)
        index = widgets.tableWidget.indexAt(pos)
        if not index.isValid():
            return  # No valid cell clicked

        # Check if the cell contains data
        cell_data = widgets.tableWidget.item(index.row(), index.column())
        if cell_data is None or cell_data.text().strip() == "":
            return  # Cell is empty, don't show context menu

        # Create the context menu
        context_menu = QMenu(widgets.tableWidget)

        # Create actions
        action_open_file = QAction(QIcon(":/icons/images/icons/cil-file.png"), 'Open File', context_menu)
        action_open_location = QAction(QIcon(":/icons/images/icons/cil-folder.png"), 'Open File Location', context_menu)
        action_watch_downloading = QAction(QIcon(":/icons/images/icons/cil-media-play.png"), 'Watch while downloading', context_menu)
        action_schedule_download = QAction(QIcon(":/icons/images/icons/cil-clock.png"), 'Schedule download', context_menu)
        action_cancel_schedule = QAction(QIcon(":/icons/images/icons/cil-x.png"), ' Cancel schedule!', context_menu)
        action_file_properties = QAction(QIcon(":/icons/images/icons/cil-info.png"),'File Properties', context_menu)


        # Add actions to the context menu
        context_menu.addAction(action_open_file)
        context_menu.addAction(action_open_location)
        context_menu.addAction(action_watch_downloading)
        context_menu.addAction(action_schedule_download)
        context_menu.addAction(action_cancel_schedule)
        context_menu.addAction(action_file_properties)

        # Connect actions to methods
        action_open_file.triggered.connect(self.open_item)
        action_open_location.triggered.connect(self.open_file_location)
        action_watch_downloading.triggered.connect(self.watch_downloading)
        action_schedule_download.triggered.connect(self.schedule_download)
        action_cancel_schedule.triggered.connect(self.cancel_schedule)
        action_file_properties.triggered.connect(self.file_properties)
        # action_view_details.triggered.connect(self.view_details)

        # Show the context menu at the cursor position
        context_menu.exec(widgets.tableWidget.viewport().mapToGlobal(pos))

    def open_item(self):
        selected_row = widgets.tableWidget.currentRow()

        self.selected_row_num = selected_row
        try:
            if self.selected_d.status == config.Status.completed:
                # Create and start the file opening thread
                self.file_open_thread = FileOpenThread(self.selected_d.target_file, self)

                # Connect the thread's signal to a slot in the main window to show the message
                self.file_open_thread.critical_signal.connect(self.show_critical)

                # Start the thread
                self.file_open_thread.start()
                log(f"Opening completed file: {self.selected_d.target_file}")
            else:
                self.show_warning("Warning", "This download is not yet completed")
        except Exception as e:
            log(f"Error opening file: {e}")

           


    def watch_downloading(self):
        selected_row = widgets.tableWidget.currentRow()
       

        self.selected_row_num = selected_row
        try:
            # Always open the temporary file for in-progress downloads
            #open_file(self.selected_d.temp_file)
            self.file_open_thread = FileOpenThread(self.selected_d.temp_file, self)
            self.file_open_thread.start()
            log(f"Watching in-progress download: {self.selected_d.temp_file}")
        except Exception as e:
            log(f"Error watching in-progress download: {e}")

    def open_file_location(self):
        selected_row = widgets.tableWidget.currentRow()

            

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        d = self.selected_d

        try:
            folder = os.path.abspath(d.folder)
            
            
            file = d.target_file

            if config.operating_system == 'Windows':
                if not os.path.isfile(file):
                    os.startfile(folder)
                else:
                    cmd = f'explorer /select, "{file}"'
                    run_command(cmd)
            else:
                # linux
                cmd = f'xdg-open "{folder}"'
                # os.system(cmd)
                run_command(cmd)
        except Exception as e:
            handle_exceptions(e)


    def schedule_download(self):
        selected_row = widgets.tableWidget.currentRow()

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        response = ask_for_sched_time(msg=self.selected_d.name)
        if response:
            self.selected_d.sched = response
    
    def cancel_schedule(self):
        selected_row = widgets.tableWidget.currentRow()

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row
        
        self.selected_d.sched = None

     # Updating `self.itemLabel` text when an item in the table is clicked
    def update_item_label(self):
        selected_row = widgets.tableWidget.currentRow()
        self.selected_row_num = selected_row
        d = self.selected_d

        widgets.itemLabel.setText(f"Download Item: {d.name}")

    def file_properties(self):
        selected_row = widgets.tableWidget.currentRow()

            

        # Set selected_row_num to the selected row
        self.selected_row_num = selected_row

        d = self.selected_d
        if d:
            text = f'Name: {d.name} \n' \
                    f'Folder: {d.folder} \n' \
                    f'Progress: {d.progress}% \n' \
                    f'Downloaded: {size_format(d.downloaded)} \n' \
                    f'Total size: {size_format(d.total_size)} \n' \
                    f'Status: {d.status} \n' \
                    f'Resumable: {d.resumable} \n' \
                    f'Type: {d.type} \n' \
                    f'Protocol: {d.protocol} \n' \
                    f'Webpage url: {d.url}'
            self.show_information("File Properties", inform="", msg=f"{text}")

        
    # endregion

    # region settings
    def settings_folder(self):
        # Get the currently selected value in the combo box
        selected = widgets.combo_setting.currentText()
        if selected == "Local":
            # Choose local folder as the settings folder
            config.sett_folder = config.current_directory

            # Remove settings.cfg from global folder
            delete_file(os.path.join(config.global_sett_folder, 'setting.cfg'))
        else:
            # Choose global folder as the settings folder
            config.sett_folder = config.global_sett_folder

            # Remove settings.cfg from local folder
            delete_file(os.path.join(config.current_directory, 'setting.cfg'))

            # Check if the global settings folder exists
            if not os.path.isdir(config.global_sett_folder):
                try:
                    # Display a confirmation dialog using QMessageBox
                    choice = QMessageBox.question(self, 'Create Folder', 
                                                f'Folder: {config.global_sett_folder}\nwill be created',
                                                QMessageBox.Ok | QMessageBox.Cancel)

                    # If the user cancels, raise an exception
                    if choice != QMessageBox.Cancel:
                        # Try to create the folder
                        os.mkdir(config.global_sett_folder)
                    else:
                        raise Exception('Operation Cancelled by User')

                except Exception as e:
                    # Log the error
                    log('global setting folder error:', e)

                    # If there is an error, use the current directory as the fallback
                    config.sett_folder = config.current_directory

                    # Show a popup with the error and inform the user about the fallback
                    QMessageBox.critical(self, 'Error',
                                        f'Error while creating global settings folder\n'
                                        f'"{config.global_sett_folder}"\n'
                                        f'{str(e)}\n'
                                        f'Local folder will be used instead')

                    # Update the combo box to reflect the local folder choice
                    widgets.combo_setting.setCurrentText('Local')

        # Update the combo box to reflect the current setting folder
        try:
            widgets.combo_setting.setCurrentText('Global' if config.sett_folder == config.global_sett_folder else 'Local')
        except:
            pass
    

    def monitor_clip(self):
        checked = widgets.monitor_clipboard.isChecked()
        config.monitor_clipboard = checked
    
    def show_download_win(self):
        checked = widgets.checkBox2.isChecked()
        config.show_download_window = checked

    def auto_close_win(self):
        checked = widgets.checkBox3.isChecked()
        config.auto_close_download_window = checked
    
    def show_thumb_nail(self):
        checked = widgets.checkBox4.isChecked()
        config.show_thumbnail = checked

    def segment_size_set(self):
        selected_seg_unit = widgets.segment_combo_setting.currentText()
        selected_seg_size = widgets.lineEdit_segment.text()
        try:
            seg_size_unit = selected_seg_unit
            if seg_size_unit == 'KB':
                seg_size = int(selected_seg_size) * 1024
            else:
                seg_size = int(selected_seg_size) * 1024 * 1024
            config.segment_size = seg_size
            self.d.segment_size = seg_size
        except:
            pass

    def speed_limit_set(self):
        # Check the state of the checkbox and enable/disable the line edit accordingly
        
        if widgets.checkBox_network.isChecked():
            widgets.lineEdit_network.setEnabled(True)  # Enable editing

            sl = widgets.lineEdit_network.text().replace(' ', '')  # if values['speed_limit'] else 0

                    # validate speed limit,  expecting formats: number + (k, kb, m, mb) final value should be in kb
                    # pattern \d*[mk]b?

            match = re.fullmatch(r'\d+([mk]b?)?', sl, re.I)
            if match:
                # print(match.group())

                digits = re.match(r"[0-9]+", sl, re.I).group()
                digits = int(digits)

                letters = re.search(r"[a-z]+", sl, re.I)
                letters = letters.group().lower() if letters else None

                # print(digits, letters)

                if letters in ('k', 'kb', None):
                    sl = digits
                elif letters in ('m', 'mb'):
                    sl = digits * 1024
            else:
                sl = 0

            config.speed_limit = sl
            
            
        else:
            config.speed_limit = 0
            widgets.lineEdit_network.setEnabled(False)  # Disable editing

    def max_current_dl(self):
        config.max_concurrent_downloads = int(widgets.combo_max_downloads.currentText())

    def max_connection(self):
        config.max_connections = int(widgets.combo_max_connections.currentText())

    def proxy_settings(self):
        if widgets.checkBox_proxy.isChecked():
            widgets.lineEdit_proxy.setEnabled(True)
            widgets.combo_proxy_type.setEnabled(True)
            config.enable_proxy = True

            
            raw_proxy = widgets.lineEdit_proxy.text()
            config.raw_proxy = raw_proxy

            # proxy type
            config.proxy_type = widgets.combo_proxy_type.currentText()

            if raw_proxy and isinstance(raw_proxy, str):
                raw_proxy = raw_proxy.split('://')[-1]
                proxy = config.proxy_type + '://' + raw_proxy

                config.proxy = proxy
                widgets.label_proxy_info.setText(config.proxy)
            
        
        else:
            config.enable_proxy = False
            config.proxy = ""
            config.raw_proxy = ""
            widgets.label_proxy_info.setText(config.proxy)
            widgets.lineEdit_proxy.setEnabled(False)
            widgets.combo_proxy_type.setEnabled(False)

    # endregion

    # region update

    def change_cursor(self, cursor_type):
        """Change cursor to busy or normal."""
        if cursor_type == 'busy':
            QApplication.setOverrideCursor(Qt.WaitCursor)  # Busy cursor
        elif cursor_type == 'normal':
            QApplication.restoreOverrideCursor()  # Restore normal cursor

    def check_update_frequency(self):
        selected = int(widgets.combo_check_update.currentText())
        config.update_frequency = selected

    def update_available(self):
        self.change_cursor('busy')

        # check for update
        current_version = config.APP_VERSION
        info = update.get_changelog()

        if info:
            latest_version, version_description = info

            # compare with current application version
            newer_version = compare_versions(current_version, latest_version)  # return None if both equal
            print(newer_version, current_version, latest_version)

            if not newer_version or newer_version == current_version:
                self.new_version_available = False
                log("check_for_update() --> App. is up-to-date, server version=", latest_version)
            else:  # newer_version == latest_version
                self.new_version_available = True
                #self.show_information('Updates', '', 'Updates available')
                self.handle_update()
                

            # updaet global values
            config.APP_LATEST_VERSION = latest_version
            self.new_version_description = version_description
        else:
            self.new_version_description = None
            self.new_version_available = False

        self.change_cursor('normal')


    def check_for_update(self):
        self.change_cursor('busy')

        # check for update
        current_version = config.APP_VERSION
        info = update.get_changelog()

        if info:
            latest_version, version_description = info

            # compare with current application version
            newer_version = compare_versions(current_version, latest_version)  # return None if both equal
            print(newer_version, current_version, latest_version)

            if not newer_version or newer_version == current_version:
                self.new_version_available = False
                log("check_for_update() --> App. is up-to-date, server version=", latest_version)
            else:  # newer_version == latest_version
                self.new_version_available = True
                

            # updaet global values
            config.APP_LATEST_VERSION = latest_version
            self.new_version_description = version_description
        else:
            self.new_version_description = None
            self.new_version_available = False

        self.change_cursor('normal')

    def start_update(self):
      
        self.startupdate = UpdateAppThread()
        self.startupdate.app_update.connect(self.update_app)
        
        self.startupdate.start()

    def update_app(self, remote=True):
        """show changelog with latest version and ask user for update
        :param remote: bool, check remote server for update"""
        
        if remote:
            Thread(target=self.check_for_update, daemon=True).start()
            #self.check_for_update()
            

        if self.new_version_available:
            config.main_window_q.put(('show_update_gui', ''))
            # self.show_update_gui()
        else:
            self.show_information(title="App Update", inform=f"App. is up-to-date \n", msg=f"Current version: {config.APP_VERSION} \n Server version:  {config.APP_LATEST_VERSION} \n")
            if self.new_version_description:
                pass
            else:
                self.show_information(title="App Update", inform="Check your internet connection", msg="Couldnt check for update")
        
        
                
    def show_update_gui(self):
        # Create a QDialog (modal window)
        dialog = QDialog(self)
        dialog.setStyleSheet("background-color: rgb(33, 37, 43); color: white;")
        dialog.setWindowTitle('Update Application')
        dialog.setModal(True)  # Keep the window on top

        # Create the layout for the dialog
        layout = QVBoxLayout()

        # Add a label to indicate the new version
        label = QLabel('New version available:')
        layout.addWidget(label)

        # Add a QTextEdit to show the new version description (read-only)
        description_edit = QTextEdit()
        description_edit.setText(self.new_version_description)  # Assuming self.new_version_description is a string
        description_edit.setReadOnly(True)
        description_edit.setFixedSize(400, 200)  # Set the size similar to size=(50, 10) in PySimpleGUI
        layout.addWidget(description_edit)

        # Create buttons for "Update" and "Cancel"
        button_layout = QHBoxLayout()
        update_button = QPushButton('Update')
        cancel_button = QPushButton('Cancel')
        button_layout.addWidget(update_button)
        button_layout.addWidget(cancel_button)

        # Add the buttons to the layout
        layout.addLayout(button_layout)

        # Set the main layout of the dialog
        dialog.setLayout(layout)

        # Connect buttons to actions
        update_button.clicked.connect(self.handle_update)  # Call the update function when "Update" is clicked
        cancel_button.clicked.connect(dialog.close)  # Close the dialog when "Cancel" is clicked

        # Show the dialog
        dialog.exec()

    def handle_update(self):
        update.update()  # Call the update method


    def animate_update_note(self):
        # display word by word
        # values = 'new version available, click me for more info !'.split()
        # values = [' '.join(values[:i + 1]) for i in range(len(values))]

        # display character by character
        # values = [c for c in 'new version available, click me for more info !']
        # values = [''.join(values[:i + 1]) for i in range(len(values))]

        # normal on off display
        values = ['', 'new version available, click me for more info !']
        note = self.window['update_note']

        # add animation text property to note object
        if not hasattr(note, 'animation_index'):
            note.animation_index = 0

        if note.animation_index < len(values) - 1:
            note.animation_index += 1
        else:
            note.animation_index = 0

        new_text = values[note.animation_index]
        note(new_text)

    def check_for_ytdl_update(self):
        config.ytdl_LATEST_VERSION = update.check_for_ytdl_update()

    def update_ytdl(self):
        current_version = config.ytdl_VERSION
        latest_version = config.ytdl_LATEST_VERSION or update.check_for_ytdl_update()
        if latest_version:
            config.ytdl_LATEST_VERSION = latest_version
            log('youtube-dl update, latest version = ', latest_version, ' - current version = ', current_version)

            if latest_version != current_version:
                # select log tab
                self.change_page(btn=widgets.btn_new, btnName="btn_logs", page=widgets.new_page)

                msg = (f'Found new version of youtube-dl on github {latest_version}\n'
                    f'current version =  {current_version} \n'
                    'Install new version?')
                confirmation_box = QMessageBox(self)
                confirmation_box.setStyleSheet("background-color: rgb(33, 37, 43); color: white;")
                confirmation_box.setWindowTitle('yt-dlp module update')
                confirmation_box.setText(msg)
                confirmation_box.setIcon(QMessageBox.Question)
                confirmation_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                reply = confirmation_box.exec_()

                if reply == QMessageBox.Yes:
                    try:
                        Thread(target=update.update_youtube_dl).start()
                    except Exception as e:
                        log('failed to update youtube-dl module:', e)
            else:
                self.show_information('YT-DLP', msg=f'yt-dlp is up-to-date, current version = {current_version}')
              
    # endregion

    

class DownloadWindow(QWidget):
    def __init__(self, d=None):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(33, 37, 43);
                color: white;
                
            }
        """)
        self.d = d
        self.q = d.q
        self.timeout = 10
        self.timer = 0
        self._progress_mode = 'determinate'
        self.init_ui()
        self.resize(500, 250)  # Adjusted size to make it smaller

    @property
    def progress_mode(self):
        return self._progress_mode

    @progress_mode.setter
    def progress_mode(self, mode):
        """change progressbar mode (determinate / undeterminate)"""
        if self._progress_mode != mode:
            self.progress_bar.setFormat(mode)
            self._progress_mode = mode

    def set_progress_mode(self, mode):
        if mode == 'determinate':
            self.progress_bar.setRange(0, 100)
        else:
            self.progress_bar.setRange(0, 0)  # This makes it indeterminate


    def init_ui(self):
        # Create a frame to hold the layout
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame_layout = QVBoxLayout(self.frame)  # Create layout inside the frame
        
        # Output Label
        self.out_label = QLabel(self.frame)
        self.out_label.setFixedHeight(160)
        self.out_label.setStyleSheet("font-size: 11px; color: white;")
        self.frame_layout.addWidget(self.out_label)

        # Progress percentage
        self.percent_label = QLabel(self.frame)
        self.frame_layout.addWidget(self.percent_label)

        # Progress Bar
        self.progress_bar = QProgressBar(self.frame)
        self.progress_bar.setRange(0, 100)
        self.frame_layout.addWidget(self.progress_bar)

        # Status label and buttons (Hide/Cancel)
        self.button_layout = QHBoxLayout()
        self.status_label = QLabel(self.frame)
        self.button_layout.addWidget(self.status_label)

        self.hide_button = QPushButton('Hide', self.frame)
        self.hide_button.clicked.connect(self.hide)
        self.button_layout.addWidget(self.hide_button)

        self.cancel_button = QPushButton('Cancel', self.frame)
        self.cancel_button.clicked.connect(self.cancel)
        self.button_layout.addWidget(self.cancel_button)

        self.frame_layout.addLayout(self.button_layout)

        # Log display
        self.log_display = QTextEdit(self.frame)
        self.log_display.setReadOnly(True)
        self.log_display.setFixedHeight(60)
        #self.log_display.setStyleSheet("selection-color: rgb(255, 255, 255); selection-background-color: rgb(255, 121, 198); color: white;")
        self.frame_layout.addWidget(self.log_display)

        # Set the layout to the widget
        self.setLayout(self.frame_layout)  # Set the frame's layout as the window layout

        # Set a minimum size for the window
        self.setMinimumSize(700, 300)

        # Timer for periodic GUI updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(500)

    
    def update_gui(self):
        # Update the progress and display information
        name = truncate(self.d.name, 50)

        out = (f"\n File: {name} \n"
               
               f"\n Downloaded: {size_format(self.d.downloaded)} out of {size_format(self.d.total_size)} \n"

               f"\n Speed: {size_format(self.d.speed, '/s')}  {time_format(self.d.time_left)} left \n"

               f"\n Live connections: {self.d.live_connections} - Remaining parts: {self.d.remaining_parts} \n")

        self.out_label.setText(out)

        # Update progress bar mode and value
        if self.d.progress:
            self.set_progress_mode('determinate')
            self.progress_bar.setValue(int(self.d.progress))
        else:
            self.set_progress_mode('indeterminate')

        if self.d.status in (config.Status.completed, config.Status.cancelled, config.Status.error):
            self.cancel_button.setText('Done')
            self.cancel_button.setStyleSheet('background-color: green; color: black;')

        # Update log
        self.log_display.setPlainText(config.log_entry)

        # Update percentage position
        self.percent_label.setText(f"{self.d.progress}%")

        # Status update
        self.status_label.setText(f"{self.d.status}  {self.d.i}")

    

    def cancel(self):
        if self.d.status not in (config.Status.error, config.Status.completed):
            self.d.status = config.Status.cancelled
        self.close()

    def hide(self):
        self.close()

    def focus(self):
        self.show()  # Ensure the window is shown
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.raise_()  # Bring the window to the front
        self.activateWindow()  # Give focus to the window
        self.update_gui()



    def close(self):
        self.timer.stop()
        super().close()




class ScheduleDialog(QDialog):
    def __init__(self, msg='', parent=None):
        super().__init__(parent)
        self.setWindowTitle('Scheduling Download Item')
        self.resize(400, 180)
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(33, 37, 43);
                color: white;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: rgb(27, 29, 35);
                border-radius: 5px;
                border: 2px solid rgb(33, 37, 43);
                padding: 5px;
                padding-left: 10px;
                color: white;
            }
            QComboBox:hover {
                border: 2px solid rgb(64, 71, 88);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px; 
                border-left-width: 3px;
                border-left-color: rgba(39, 44, 54, 150);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;	
                background-image: url(:/icons/images/icons/cil-arrow-bottom.png);
                background-position: center;
                background-repeat: no-repeat;
            }
            QComboBox QAbstractItemView {
                color: white;	
                background-color: rgb(33, 37, 43);
                padding: 10px;
                selection-background-color: rgb(39, 44, 54);
            }
            QPushButton {
                background-color: rgb(33, 37, 43);
                border: 1px solid rgb(44, 49, 58);
                border-radius: 5px;
                padding: 5px 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgb(44, 49, 58);
                
            }
        """)

        # Create layout
        layout = QVBoxLayout(self)

        # Message label
        self.message_label = QLabel(msg)
        layout.addWidget(self.message_label)

        # Row layout for hours and minutes selection
        row_layout = QHBoxLayout()

        # Hour label and combo box
        self.hour_label = QLabel("Hours:")
        row_layout.addWidget(self.hour_label)
        self.hours_combo = QComboBox(self)
        self.hours_combo.addItems([str(i) for i in range(1, 13)])  # 1 to 12
        row_layout.addWidget(self.hours_combo)

        # Minute label and combo box
        self.minute_label = QLabel("Minutes:")
        row_layout.addWidget(self.minute_label)
        self.minutes_combo = QComboBox(self)
        self.minutes_combo.addItems([f"{i:02d}" for i in range(0, 60)])  # 0 to 59, formatted as two digits
        row_layout.addWidget(self.minutes_combo)

        # Add the row layout to the main layout
        layout.addLayout(row_layout)

        # AM/PM selection in the next row, centered
        am_pm_layout = QHBoxLayout()
        am_pm_layout.addStretch()  # Add space on the left
        self.am_pm_combo = QComboBox(self)
        self.am_pm_combo.addItems(['AM', 'PM'])
        am_pm_layout.addWidget(self.am_pm_combo)
        am_pm_layout.addStretch()  # Add space on the right
        layout.addLayout(am_pm_layout)

        # Ok and Cancel buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # Add the buttons to the layout
        layout.addLayout(button_layout)

        # Set default values
        self.hours_combo.setCurrentIndex(0)  # Default to 1
        self.minutes_combo.setCurrentIndex(0)  # Default to 0
        self.am_pm_combo.setCurrentIndex(0)  # Default to AM

    @property
    def response(self):
        # Return the selected hours and minutes as a tuple
        h = int(self.hours_combo.currentText())
        m = int(self.minutes_combo.currentText())
        am_pm = self.am_pm_combo.currentText()

        if am_pm == 'PM' and h != 12:
            h += 12
        elif am_pm == 'AM' and h == 12:
            h = 0

        return h, m

def ask_for_sched_time(msg=''):
    dialog = ScheduleDialog(msg)
    result = dialog.exec()  # Show the dialog as a modal

    if result == QDialog.Accepted:
        return dialog.response  # Return the (hours, minutes) tuple
    return None


# Define clipboard_listener and singleApp functions here

# def clipboard_listener():
#     old_data = ''
    
#     while True:
#         # Read from the clipboard
#         new_data = clipboard_read()
#         #print(f"Clipboard data: {new_data}")

#         # Check if a message is received from another instance
#         if new_data == 'any one there?':  
#             clipboard_write('yes')  # Reply to the instance
#             config.main_window_q.put(('visibility', 'show'))  # Request main window visibility

#         # Check if clipboard monitoring is active and the content has changed
#         if config.monitor_clipboard and new_data != old_data:
#             if new_data.startswith('http') and ' ' not in new_data:
#                 # Send the URL to the main window queue
#                 config.main_window_q.put(('url', new_data))
            
#             old_data = new_data
#             #print(f"Updated clipboard data: {old_data}")

#         # Stop the clipboard listener if needed
#         if config.terminate:
#             break

#         # Sleep briefly to avoid busy-waiting
#         time.sleep(0.2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    
    # Create the main window
    window = MainWindow(config.d_list)
    window.show()
    QTimer.singleShot(0, video.import_ytdl)

    
    # Start the event loop
    sys.exit(app.exec())