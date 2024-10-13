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
        widgets.delete.clicked.connect(self.delete_btn)
        widgets.resume.clicked.connect(self.resume_btn)
        widgets.resume_all.clicked.connect(self.resume_all_downloads)
        widgets.cancel.clicked.connect(self.cancel_btn)
        widgets.refresh.clicked.connect(self.refresh_link_btn)
        widgets.d_window.clicked.connect(self.download_window)
        widgets.schedule_all.clicked.connect(self.schedule_all)
        widgets.stop_all.clicked.connect(self.stop_all_downloads)
        widgets.delete_all.clicked.connect(self.delete_all_downloads)
        #widgets.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
        # Enable custom context menu on the table widget
        widgets.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        widgets.tableWidget.customContextMenuRequested.connect(self.show_table_context_menu)
        
        

        widgets.version.setText(f"{config.APP_VERSION}")
        widgets.titleLeftApp.setText(f"{config.APP_NAME}")
        widgets.titleLeftDescription.setText(f"{config.APP_DEC}")

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
        #widgets.label_proxy_info.setText(config.proxy == '' if config.enable_proxy)
        

        #widgets.checkBox_network.stateChanged.connect(self.speed_limit_set)
        # import youtube-dl in a separate thread
        Thread(target=video.import_ytdl, daemon=True).start()
        
     


    # BUTTONS CLICK
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        pass

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

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
                Thread(target=self.youtube_func, daemon=True).start()
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
            
            # widgets.stackedWidget.setCurrentWidget(widgets.widgets)
        #widgets.size_value_label.setText(size_format(self.d.protocol))
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

            # enable download button
            if self.d.status_code not in self.bad_headers and self.d.type != 'text/html':
                widgets.DownloadButton.setEnabled(False)  # Disables the button
            


            # check if the link contains stream videos by youtube-dl
            Thread(target=self.youtube_func, daemon=True).start()

        #self.change_cursor('default')


    # region download folder
    
    
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
            self.show_thumb_nail()
            self.segment_size_set()
            self.speed_limit_set()
            self.max_current_dl()
            self.max_connection()
            self.proxy_settings()

                
        except Exception as e:
            log('MainWindow.update_gui() error:', e)
    
    

        



    # region Start download
    @property
    def active_downloads(self):
        # update active downloads
        _active_downloads = set(d.id for d in self.d_list if d.status == config.Status.downloading)
        config.active_downloads = _active_downloads

        return _active_downloads
    
    def start_download(self, d, silent=False, downloader=None):
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
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            
    # endregion

    # region youtube
    
    def youtube_func(self):
        """Fetch metadata from YouTube and process it."""
        # Initialization code...
        
        try:
            # Ensure youtube-dl is loaded
            if video.ytdl is None:
                log('youtube-dl module still loading, please wait')
                while not video.ytdl:
                    time.sleep(0.1)

            # Extract information with youtube-dl
            with video.ytdl.YoutubeDL(get_ytdl_options()) as ydl:
                info = ydl.extract_info(self.d.url, download=False, process=False)
                log('Media info:', info, log_level=3)

                # Check if it's a playlist
                if info.get('_type') == 'playlist' or 'entries' in info:
                    pl_info = list(info.get('entries'))
                    self.playlist = [Video(item.get('url') or item.get('webpage_url') or item.get('id')) for item in pl_info]

                    # Make sure the first video is valid
                    if self.playlist and self.playlist[0]:
                        self.d = self.playlist[0]
                        self.update_pl_menu()
                    else:
                        log("Error: No valid videos found in playlist")
                        return

                else:
                    # Single video case
                    self.playlist = [Video(self.d.url, vid_info=None)]
                    if self.playlist[0]:
                        self.d = self.playlist[0]
                        self.update_pl_menu()
                        log('YESS', self.d, log_level=3)
                        self.update_stream_menu()
                    else:
                        log("Error: Single video extraction failed")
                        return

        except Exception as e:
            log('youtube_func()> error:', e)
            log('Error occurred on line:', sys.exc_info()[-1].tb_lineno)
            #self.reset_video_controls()

        



    def update_pl_menu(self):
        """Update the playlist combobox after processing."""
        try:
            # Set the playlist combobox with video titles
            num = len(self.playlist)
            widgets.combo_setting_c.clear()  # Clear existing items
            widgets.combo_setting_c.addItems([f'{i + 1} - {video.title}' for i, video in enumerate(self.playlist)])

            # Automatically select the first video in the playlist
            self.playlist_OnChoice(self.playlist[0])

        except Exception as e:
            log(f"Error updating playlist menu: {e}")


    def update_stream_menu(self):
        """Update the stream combobox after selecting a video."""
        try:
            if self.video is None:
                log(f"Error: self.video is None'")
                return
            if not hasattr(self.video, 'stream_names'):
                log("Error: self.video is missing 'stream_names'.")
                return

            # Ensure that self.video is valid and has streams
            # if not self.video or not hasattr(self.video, 'stream_names'):
            #     log(f"Error: self.video is None or missing 'stream_names'")
            #     return

            # Check if streams exist
            if not self.video.stream_names:
                log("Error: No streams available for this video")
                return

            # Set the stream combobox with available stream options
            widgets.stream_combo.clear()  # Clear existing items
            widgets.stream_combo.addItems(self.video.stream_names)

            # Automatically select the first stream
            selected_stream = self.video.stream_names[0]
            widgets.stream_combo.setCurrentText(selected_stream)
            self.stream_OnChoice(selected_stream)

        except Exception as e:
            log(f"Error updating stream menu: {e}")



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
        self.update_gui()


    def stream_OnChoice(self, selected_stream):
        """Handle stream selection."""
        if selected_stream not in self.video.stream_names:
            selected_stream = self.video.stream_names[0]  # Default to the first stream

        self.video.selected_stream = self.video.streams[selected_stream]  # Set the selected stream
        self.update_gui()  # Update the GUI to reflect the selected stream

   
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
    

    # endregion

    # region downloads functions


        
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
        widgets.stackedWidget.setCurrentWidget(widgets.home)

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

   
    

    # endregion

    # region settings
    def settings_folder(self):
        pass
    

    






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
    # Start the clipboard listener in a separate thread
    Thread(target=clipboard_listener, daemon=True).start()
    # Start logging
    Thread(target=log_recorder, daemon=True).start()
    
    # Start the event loop
    sys.exit(app.exec())
