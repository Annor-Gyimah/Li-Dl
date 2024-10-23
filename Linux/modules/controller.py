"""
    PyIDM

    multi-connections internet download manager, based on "pyCuRL/curl", "youtube_dl", and "PySimpleGUI"

    :copyright: (c) 2019-2020 by Mahmoud Elshahat.
    :license: GNU LGPLv3, see LICENSE for more details.
"""
import sys
import webbrowser

import os
import re
import time
import copy
import subprocess
from threading import Thread, Barrier, Timer, Lock
from collections import deque

from .utils import *
from . import config
from .config import Status
from . import update
from .brain import brain
from . import video
from .video import Video, check_ffmpeg, download_ffmpeg, unzip_ffmpeg, get_ytdl_options
#from .about import about_notes
from .downloaditem import DownloadItem
from .iconsbase64 import *


from PyQt5.QtWidgets import QMessageBox
# todo: this module needs some clean up



class Controller:
    def __init__(self, d_list):
        """This is the main application user interface window"""

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

        # initial setup
        self.setup()

    def setup(self):
        """initial setup"""
        
        # download folder
        if not self.d.folder:
            self.d.folder = config.download_folder

        

        
    def read_q(self):
        # read incoming messages from queue
        for _ in range(config.main_window_q.qsize()):
            k, v = config.main_window_q.get()
    

            if k == 'url':
                self.window.Element('url').Update(v)
                self.url_text_change()

            elif k == 'monitor':
                self.window.Element('monitor').Update(v)





   # region General
    def url_text_change(self):
        url = self.window.Element('url').Get().strip()
        if url == self.d.url:
            return

        # Focus and select main app page in case text changed from script
        self.window.BringToFront()
        self.select_tab('Main')

        self.reset()
        try:
            self.d.eff_url = self.d.url = url

            # schedule refresh header func
            if isinstance(self.url_timer, Timer):
                self.url_timer.cancel()  # cancel previous timer

            self.url_timer = Timer(0.5, self.refresh_headers, args=[url])
            self.url_timer.start()  # start new timer

        except:
            pass

    def reset(self):
        # create new download item, the old one will be garbage collected by python interpreter
        self.d = DownloadItem()

        # reset some values
        self.set_status('')
        self.playlist = []
        self.video = None

        self.window['status_code']('')

    def set_status(self, text):
        """update status bar text widget"""
        try:
            self.window['status_bar'](text)
        except:
            pass