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

from modules.utils import clipboard_read, clipboard_write, size_format
from modules import config
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QTimer
class MainWindow(QMainWindow):
    def __init__(self, d_list):
        QMainWindow.__init__(self)


        # current download_item
        self.d = DownloadItem()

        

        # main window
        self.window = None

        # download windows
        self.download_windows = {}  # dict that holds Download_Window() objects --> {d.id: Download_Window()}

        # url
        self.url_timer = None  # usage: Timer(0.5, self.refresh_headers, args=[self.d.url])
        self.bad_headers = [0, range(400, 404), range(405, 418), range(500, 506)]  # response codes

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

        # download
        self.pending = deque()
        self.disabled = True  # for download button

        # download list
        self.d_headers = ['i', 'name', 'progress', 'speed', 'time_left', 'downloaded', 'total_size', 'status']
        self.d_list = d_list  # list of DownloadItem() objects
        self.selected_row_num = None
        self._selected_d = None

        # update
        self.new_version_available = False
        self.new_version_description = None

        # thumbnail
        self.current_thumbnail = None

        
        # Start the QTimer to poll the queue
        self.queue_timer = QTimer()
        self.queue_timer.timeout.connect(self.read_q)
        self.queue_timer.start(500)  # Check the queue every 500ms

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
        title = "Li-DL"
        description = "Li-DL"
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
        widgets.btn_save.clicked.connect(self.buttonClick)

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
        if btnName == "btn_settings":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

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

            if k == 'url':
                # Update the QLineEdit with the new URL
                widgets.home_link_lineEdit.setText(v)
                #print(f"Updated QLineEdit with URL: {v}")
                self.url_text_change()
                self.update_progress_bar()





   # region General
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
            
            # Trigger the progress bar update and GUI refresh
            self.update_progress_bar()
        except Exception as e:
            print(f"Error in url_text_change: {e}")

    def update_progress_bar(self):
        """Update the progress bar based on URL processing."""
        # Start a new thread for the progress updates
        Thread(target=self.process_url, daemon=True).start()

    
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

        # widgets
        # self.disable()
        # self.reset_video_controls()
        # self.window['status_code']('')

    # def change_cursor(self, cursor='default'):
    #     # todo: check if we can set cursor  for window not individual tabs
    #     if cursor == 'busy':
    #         cursor_name = 'watch'
    #     else:  # default
    #         cursor_name = 'arrow'

    #     self.window['Main'].set_cursor(cursor_name)
    #     self.window['Settings'].set_cursor(cursor_name)

    def set_status(self, text):
        """update status bar text widget"""
        try:
            self.window['status_bar'](text)
        except:
            pass
    
    def refresh_headers(self, url):
        if self.d.url != '':
            #self.change_cursor('busy')
            Thread(target=self.get_header, args=[url], daemon=True).start()

    def get_header(self, url):
        # curl_headers = get_headers(url)
        self.d.update(url)

        # update headers only if no other curl thread created with different url
        if url == self.d.url:

            # update status code widget
            try:
                self.window['status_code'](f'status: {self.d.status_code}')
                #
            except:
                pass
            # self.set_status(self.d.status_code_description)

            # enable download button
            if self.d.status_code not in self.bad_headers and self.d.type != 'text/html':
                widgets.DownloadButton.hide()

            # check if the link contains stream videos by youtube-dl
            # Thread(target=self.youtube_func, daemon=True).start()

        #self.change_cursor('default')

    def update_gui(self):
        """Update GUI elements with current download information."""
        try:
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
            
            # You can add more GUI updates here as needed
            
            print(f"Updated size label to: {size_text}")
            print(f"Updated type label to: {type_text}")
            print(f"Updated protocol label to {protocol_text}")
            print(f"Updated resumable label to :{resumable_text}")
        except Exception as e:
            print('MainWindow.update_gui() error:', e)
        
    



    






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

    # Start the clipboard listener in a separate thread
    Thread(target=clipboard_listener, daemon=True).start()

    # Start the event loop
    sys.exit(app.exec())
