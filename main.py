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

from modules.utils import clipboard_read, clipboard_write, size_format, validate_file_name, log, log_recorder
from modules import config
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PySide6.QtCore import QTimer, Qt
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
        # self.queue_timer = QTimer()
        # self.queue_timer.timeout.connect(self.read_q)
        # self.queue_timer.start(500)  # Check the queue every 500ms

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

        log('Starting PyIDM version:', config.APP_VERSION, 'Frozen' if config.FROZEN else 'Non-Frozen')
        # log('starting application')
        log('operating system:', config.operating_system_info)
        log('current working directory:', config.current_directory)
        os.chdir(config.current_directory)




       


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
                    print(e)

                self.set_status(v.strip('\n'))

            elif k == 'url':
                # Update the QLineEdit with the new URL
                widgets.home_link_lineEdit.setText(v)
                #print(f"Updated QLineEdit with URL: {v}")
                self.url_text_change()
                self.update_progress_bar()
            
            elif k == "download":
                self.start_download(*v)

                

            


    def run(self):
        """Handle the event loop."""
        try:

            # if self.retry_button_clicked:  # Check if the retry button was clicked
            #     print("Retry Executed")
            #     self.retry()  # Call the retry function when the retry event is detected
            #     self.retry_button_clicked = False  # Reset it back to False after processing

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
            self.d.update(url)
            
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
            # Thread(target=self.youtube_func, daemon=True).start()

        #self.change_cursor('default')


    # region download folder
    def open_folder_dialog(self):
        """Open a dialog to select a folder and update the line edit."""
        # Open a folder selection dialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")

        # If a folder is selected, update the line edit with the absolute path
        if folder_path:
            widgets.home_folder_path_lineEdit.setText(folder_path)
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

            
                
        except Exception as e:
            print('MainWindow.update_gui() error:', e)
    
    def on_download_button_clicked(self, downloader=None):
        """Handle DownloadButton click event."""
        # Check if the download button is disabled
        if self.d.url == "":
            # Use QMessageBox to display the popup in PyQt
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Download Error')
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

        



    # region Start download
    def start_download(self, d, silent=False, downloader=None):
        if d is None:
            return
        
        if d.name == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Download Error')
            msg.setText('File name is invalid')
            msg.setInformativeText('Please enter a valid filename')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return
        
        print("Yes Downloads")
    
        
    

    

    






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
    # Start logging
    Thread(target=log_recorder, daemon=True).start()


    # Start the event loop
    sys.exit(app.exec())
