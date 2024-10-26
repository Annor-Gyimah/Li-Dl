# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maingnxZcz.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from . resources_rc import *
from .retrans import retranslateUi

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(18"
                        "9, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb("
                        "189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_info.svg);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border"
                        "-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-sty"
                        "le: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-co"
                        "lor: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QMessageBox */\n"
"QMessageBox {\n"
"    background-color: rgb(33, 37, 43);\n"  
"    color: rgb(221, 221, 221);\n"           
"    border: 1px solid rgb(44, 49, 58);\n"
"}\n"

"QMessageBox QLabel {\n"
"    color: rgb(221, 221, 221);\n"            
"    font: 10pt 'Segoe UI';\n"                
"}\n"

"QMessageBox QPushButton {\n"
"    background-color: rgb(40, 44, 52);\n"    
"    color: rgb(221, 221, 221);\n"            
"    border: 1px solid rgb(44, 49, 58);\n"    
"    padding: 5px 15px;\n"                    
"}\n"

"QMessageBox QPushButton:hover {\n"
"    background-color: rgb(189, 147, 249);\n" 
"    color: rgb(255, 255, 255);\n"            
"}\n"

"QMessageBox QPushButton:pressed {\n"
"    background-color: rgb(111, 66, 193);\n"  
"    color: rgb(255, 255, 255);\n"            
"}\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-c"
                        "olor: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
""
                        "QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     su"
                        "bcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	back"
                        "ground-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subco"
                        "ntrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    h"
                        "eight: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLi"
                        "nkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamily(u"Segoe UI Semibold")
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_downloads")
        sizePolicy.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-data-transfer-down.png);")

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_logs")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-terminal.png);")

        self.verticalLayout_8.addWidget(self.btn_new)

        # self.btn_save = QPushButton(self.topMenu)
        # self.btn_save.setObjectName(u"btn_save")
        # sizePolicy.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        # self.btn_save.setSizePolicy(sizePolicy)
        # self.btn_save.setMinimumSize(QSize(0, 45))
        # self.btn_save.setFont(font)
        # self.btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_save.setLayoutDirection(Qt.LeftToRight)
        # self.btn_save.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-save.png)")

        # self.verticalLayout_8.addWidget(self.btn_save)

        # self.btn_exit = QPushButton(self.topMenu)
        # self.btn_exit.setObjectName(u"btn_exit")
        # sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        # self.btn_exit.setSizePolicy(sizePolicy)
        # self.btn_exit.setMinimumSize(QSize(0, 45))
        # self.btn_exit.setFont(font)
        # self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        # self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        # self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_info.svg);")
        #self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/intt1.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        # self.btn_share = QPushButton(self.extraTopMenu)
        # self.btn_share.setObjectName(u"btn_share")
        # sizePolicy.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        # self.btn_share.setSizePolicy(sizePolicy)
        # self.btn_share.setMinimumSize(QSize(0, 45))
        # self.btn_share.setFont(font)
        # self.btn_share.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_share.setLayoutDirection(Qt.LeftToRight)
        # self.btn_share.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")

        # self.verticalLayout_11.addWidget(self.btn_share)

        # self.btn_adjustments = QPushButton(self.extraTopMenu)
        # self.btn_adjustments.setObjectName(u"btn_adjustments")
        # sizePolicy.setHeightForWidth(self.btn_adjustments.sizePolicy().hasHeightForWidth())
        # self.btn_adjustments.setSizePolicy(sizePolicy)
        # self.btn_adjustments.setMinimumSize(QSize(0, 45))
        # self.btn_adjustments.setFont(font)
        # self.btn_adjustments.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_adjustments.setLayoutDirection(Qt.LeftToRight)
        # self.btn_adjustments.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-equalizer.png);")

        # self.verticalLayout_11.addWidget(self.btn_adjustments)

        # self.btn_more = QPushButton(self.extraTopMenu)
        # self.btn_more.setObjectName(u"btn_more")
        # sizePolicy.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        # self.btn_more.setSizePolicy(sizePolicy)
        # self.btn_more.setMinimumSize(QSize(0, 45))
        # self.btn_more.setFont(font)
        # self.btn_more.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_more.setLayoutDirection(Qt.LeftToRight)
        # self.btn_more.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-layers.png);")

        # self.verticalLayout_11.addWidget(self.btn_more)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setStyleSheet("color: white;")
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
#         self.home.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula_vertical.png);\n"
# "background-position: center;\n"
# "background-repeat: no-repeat;")

        self.home.setStyleSheet(u"b")
        self.home_verticalLayout = QVBoxLayout(self.home)
        self.home_verticalLayout.setSpacing(10)
        self.home_verticalLayout.setObjectName(u"home_verticalLayout")
        self.home_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.home_verticalLayout.setSpacing(5)  # Reduce the spacing between widgets
        self.home_verticalLayout.setAlignment(Qt.AlignTop)

        self.home_row_1 = QFrame(self.home)
        self.home_row_1.setFrameShape(QFrame.StyledPanel)
        self.home_row_1.setFrameShadow(QFrame.Raised)

        # Create a vertical layout for the frame
        self.home_verticalLayout_row_1 = QVBoxLayout(self.home_row_1)
        self.home_verticalLayout_row_1.setSpacing(15)  # Add spacing between elements
        self.home_verticalLayout_row_1.setContentsMargins(10, 10, 10, 10)  # Set margins

        # Create title label directly within the layout (no extra frame needed)
        self.home_link_label = QLabel("LINK",self.home_row_1)
        self.home_link_label.setFont(font)
        self.home_verticalLayout_row_1.addWidget(self.home_link_label)

        # Create a horizontal layout for QLineEdit and QPushButton
        self.home_horizontalLayout_row_1 = QHBoxLayout()
        self.home_horizontalLayout_row_1.setSpacing(10)  # Add spacing between the widgets

        # Add First QLineEdit with larger size
        self.home_link_lineEdit = QLineEdit(self.home_row_1)
        self.home_link_lineEdit.setMinimumSize(QSize(0, 30))  # Increased width to make it larger
        self.home_link_lineEdit.setPlaceholderText("Place download link here")
        self.home_link_lineEdit.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.home_horizontalLayout_row_1.addWidget(self.home_link_lineEdit)

        # Add QPushButton
        self.home_retry_pushbutton = QPushButton("Retry",self.home_row_1)
        self.home_retry_pushbutton.setMinimumSize(QSize(150, 30))
        self.home_retry_pushbutton.setFont(font)
        self.home_retry_pushbutton.setObjectName(u"btn_retry")
        self.home_retry_pushbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.home_retry_pushbutton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.home_retry_pushbutton.setIcon(icon1)
        self.home_horizontalLayout_row_1.addWidget(self.home_retry_pushbutton)

        self.home_verticalLayout_row_1.addLayout(self.home_horizontalLayout_row_1)
        

        


        
        ##########################################################################################
        
        # Create the main frame for home_row_2
        self.home_row_2 = QFrame(self.home)
        self.home_row_2.setObjectName(u"row_2")
        self.home_row_2.setFrameShape(QFrame.StyledPanel)
        self.home_row_2.setFrameShadow(QFrame.Raised)

        # Create a vertical layout for the frame
        self.home_verticalLayout_2 = QVBoxLayout(self.home_row_2)
        self.home_verticalLayout_2.setSpacing(0)
        self.home_verticalLayout_2.setObjectName(u"verticalLayout_16")
        self.home_verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        # Add other widgets (e.g., labels, buttons) to the layout as needed
        # Example: Adding a label
        # self.label_example = QLabel("Example Label", self.home_row_2)
        # self.home_verticalLayout_2.addWidget(self.label_example)


        # Create the progress bar
        self.progressBar = QProgressBar(self.home_row_2)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setRange(0, 100)  # Set range if needed
        self.progressBar.setValue(0)  # Set the current value (for example, 50%)

        # Set a fixed width for the progress bar
        self.progressBar.setFixedWidth(400)  # Set the desired width

        # Add the progress bar to the layout with margins
        self.home_verticalLayout_2.addWidget(self.progressBar, 0, Qt.AlignHCenter | Qt.AlignTop)

        # Set margins directly on the layout for spacing
        self.home_verticalLayout_2.setContentsMargins(20, 0, 20, 0)  # Left and right margins set to 20 pixels

        # Optional: Style the progress bar
        self.progressBar.setStyleSheet("""
        QProgressBar {
                border: 2px solid #ff79c6;
                border-radius: 5px;
                text-align: center;
        }
        QProgressBar::chunk {
                background-color: #bd93f9;
                width: 10px;
                margin: 1px;
        }
        """)


        ##################################################################################################
        
        # Create the main frame for home_row_3
        self.home_row_3 = QFrame(self.home)
        self.home_row_3.setFrameShape(QFrame.StyledPanel)
        self.home_row_3.setFrameShadow(QFrame.Raised)

        # Create a vertical layout for the frame
        self.home_verticalLayout_row_3 = QVBoxLayout(self.home_row_3)
        self.home_verticalLayout_row_3.setSpacing(15)  # Add spacing between elements
        self.home_verticalLayout_row_3.setContentsMargins(10, 10, 10, 10)  # Set margins

        # Create title label directly within the layout (no extra frame needed)
        self.home_choose_folder_label = QLabel("CHOOSE FOLDER",self.home_row_3)
        self.home_choose_folder_label.setFont(font)
        self.home_verticalLayout_row_3.addWidget(self.home_choose_folder_label)

        # Create a horizontal layout for QLineEdit and QPushButton
        self.home_horizontalLayout_row_3 = QHBoxLayout()
        self.home_horizontalLayout_row_3.setSpacing(10)  # Add spacing between the widgets

        # Add First QLineEdit with larger size
        self.home_folder_path_lineEdit = QLineEdit(self.home_row_3)
        self.home_folder_path_lineEdit.setMinimumSize(QSize(300, 30))  # Increased width to make it larger
        self.home_folder_path_lineEdit.setPlaceholderText("Folder Path")
        self.home_folder_path_lineEdit.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.home_horizontalLayout_row_3.addWidget(self.home_folder_path_lineEdit)

        # Add QPushButton
        self.home_open_pushButton = QPushButton("Open",self.home_row_3)
        self.home_open_pushButton.setMinimumSize(QSize(150, 30))
        self.home_open_pushButton.setFont(font)
        self.home_open_pushButton.setObjectName(u"btn_browse")
        self.home_open_pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.home_open_pushButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.home_open_pushButton.setIcon(icon4)
        self.home_horizontalLayout_row_3.addWidget(self.home_open_pushButton)


        

        # Create a horizontal layout for QLineEdit and QPushButton
        self.home_filename_row = QVBoxLayout()
        self.home_filename_row.setSpacing(15)  # Add spacing between the widgets

        # Create title label directly within the layout (no extra frame needed)
        self.home_filename_label = QLabel("FILENAME",self.home_row_3)
        self.home_filename_label.setFont(font)
        self.home_filename_row.addWidget(self.home_filename_label)


        # Add Second QLineEdit with larger size
        self.home_filename_lineEdit = QLineEdit(self.home_row_3)
        self.home_filename_lineEdit.setMinimumSize(QSize(300, 30))  # Increased width to make it larger
        self.home_filename_lineEdit.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.home_filename_lineEdit.setPlaceholderText("Filename goes here")
        self.home_filename_row.addWidget(self.home_filename_lineEdit)

        # Add horizontal layout to the main vertical layout
        self.home_verticalLayout_row_3.addLayout(self.home_horizontalLayout_row_3)
        self.home_verticalLayout_row_3.addLayout(self.home_filename_row)
       

        ###############################################################################################################
        

        # Create the main frame for home_row_4
        self.home_row_4 = QFrame(self.home)
        self.home_row_4.setFrameShape(QFrame.StyledPanel)
        self.home_row_4.setFrameShadow(QFrame.Raised)

        # Create a horizontal layout for the frame
        self.home_horizontalLayout_4 = QHBoxLayout(self.home_row_4)
        self.home_horizontalLayout_4.setObjectName(u"horizontalLayout_11")
        self.home_horizontalLayout_4.setContentsMargins(60, 20, 60, 60)  # Adjust margins for overall spacing
        self.home_horizontalLayout_4.setSpacing(20)  # Space between different label-value pairs

        # Function to create a label-value pair and add it to the layout
        def add_label_value_pair(label_text, value_text, layout):
                pair_layout = QHBoxLayout()  # Nested layout for label and value
                pair_layout.setSpacing(1)    # Small spacing between label and its value
                pair_layout.setContentsMargins(20, 0, 20, 0)

                label = QLabel(label_text, self.home_row_4)
                value_label = QLabel(value_text, self.home_row_4)

                pair_layout.addWidget(label)
                pair_layout.addWidget(value_label)

                layout.addLayout(pair_layout)

                return value_label  # Return the QLabel for the value


        # Add the label-value pairs to the horizontal layout

        # Size and Size_value
        self.size_value_label = add_label_value_pair("Size:", "Size_value", self.home_horizontalLayout_4)
        # Type and Type_value
        self.type_value_label = add_label_value_pair("Type:", "Type_value", self.home_horizontalLayout_4)
        # Protocol and Protocol_value
        self.protocol_value_label = add_label_value_pair("Protocol:", "Protocol_value", self.home_horizontalLayout_4)
        # Resumable and Resumable_value
        self.resumable_value_label = add_label_value_pair("Resumable:", "Resumable_value", self.home_horizontalLayout_4)



        ##############################################################################################################
        # Create the main frame for home_row_4
        self.home_row_5 = QFrame(self.home)
        self.home_row_5.setFrameShape(QFrame.StyledPanel)
        self.home_row_5.setFrameShadow(QFrame.Raised)


        # Create a vertical layout for the frame
        self.home_verticalLayout_5 = QVBoxLayout(self.home_row_5)
        self.home_verticalLayout_5.setSpacing(0)
        self.home_verticalLayout_5.setObjectName(u"verticalLayout_16")
        self.home_verticalLayout_5.setContentsMargins(0, 0, 0, 0)


        self.DownloadButton = QPushButton("Download",self.home_row_5)
        self.DownloadButton.setObjectName(u"DownloadButton")
        self.DownloadButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.DownloadButton.setStyleSheet(u"")
        self.DownloadButton.setMinimumSize(QSize(150, 50))
        icon8 = QIcon()
        icon8.addFile(u":/icons/images/icons/cil-data-transfer-down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.DownloadButton.setIcon(icon8)
        
        # self.combo_setting_c = QComboBox(self.home_row_5)
        # self.combo_setting_c.setObjectName(u"combo_setting")
        
        # self.stream_combo = QComboBox(self.home_row_5)
        #self.combo_setting_c.addItems])
        
        



        # Add the progress bar to the layout with margins
        self.home_verticalLayout_5.addWidget(self.DownloadButton, 0, Qt.AlignHCenter | Qt.AlignTop)

        # Set margins directly on the layout for spacing
        self.home_verticalLayout_5.setContentsMargins(20, 0, 20, 0)  # Left and right margins set to 20 pixels



        # Create the main frame for home_row_6
        self.home_row_6 = QFrame(self.home)
        self.home_row_6.setFrameShape(QFrame.StyledPanel)
        self.home_row_6.setFrameShadow(QFrame.Raised)
        self.home_row_6.setMinimumHeight(50)  # Adjusted height
        self.home_row_6.setMaximumHeight(120)  # Set a reasonable height to avoid overlap

        # Create a horizontal layout for the frame
        self.home_horizontalLayout_row_6 = QHBoxLayout(self.home_row_6)
        self.home_horizontalLayout_row_6.setSpacing(10)  # Reduced spacing for padding
        self.home_horizontalLayout_row_6.setContentsMargins(40, 10, 40, 10)  # Adjust margins to add padding on left and right

        # First layout: for the video thumbnail
        self.home_video_thumbnail_layout = QVBoxLayout()
        self.home_video_thumbnail_layout.setSpacing(0)

        # Add QLabel to represent the video thumbnail
        self.home_video_thumbnail_label = QLabel(self.home_row_6)
        self.home_video_thumbnail_label.setFixedSize(150, 100)  # Fixed size for thumbnail
        self.home_video_thumbnail_label.setPixmap(QPixmap(":/icons/images/icons/thumbnail-default.png").scaled(150, 150, Qt.KeepAspectRatio))
        self.home_video_thumbnail_label.setAlignment(Qt.AlignCenter)
        #self.home_video_thumbnail_label.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.home_video_thumbnail_layout.addWidget(self.home_video_thumbnail_label)

        

        # Add the thumbnail layout to the horizontal layout
        self.home_horizontalLayout_row_6.addStretch(1)  # Add stretch to left for centering
        self.home_horizontalLayout_row_6.addLayout(self.home_video_thumbnail_layout)

        # Layout for combo boxes
        self.home_combobox_layout = QVBoxLayout()
        self.home_combobox_layout.setSpacing(10)  # Space between combo boxes

        # Add the first combo box
        self.combo_setting_c = QComboBox(self.home_row_6)
        self.combo_setting_c.setMinimumSize(QSize(120, 30))  # Adjust width here
        self.combo_setting_c.setStyleSheet("""
        QComboBox {
                background-color: rgb(33, 37, 43);  /* Background of the combo box */
                color: white;  /* Text color */
                border: 1px solid gray;  /* Border */
                padding: 5px;
        }
        QComboBox QAbstractItemView {
                background-color: rgb(33, 37, 43);  /* Background of drop-down list */
                color: white;  /* Text color in the drop-down list */
                selection-background-color: rgb(85, 170, 255);  /* Color of the selected item */
        }
        """)
        # self.combo_setting_c.addItems(["Local", "Global"])
        self.home_combobox_layout.addWidget(self.combo_setting_c)

        # Add the second combo box
        self.stream_combo = QComboBox(self.home_row_6)
        self.stream_combo.setMinimumSize(QSize(120, 30))  # Adjust width here
        self.stream_combo.setStyleSheet("""
        QComboBox {
                background-color: rgb(33, 37, 43);  /* Background of the combo box */
                color: white;  /* Text color */
                border: 1px solid gray;  /* Border */
                padding: 5px;
        }
        QComboBox QAbstractItemView {
                background-color: rgb(33, 37, 43);  /* Background of drop-down list */
                color: white;  /* Text color in the drop-down list */
                selection-background-color: rgb(85, 170, 255);  /* Color of the selected item */
        }
        """)
        self.home_combobox_layout.addWidget(self.stream_combo)

        self.playlist_button = QPushButton("Playlist",self.home_row_6)
        
        self.playlist_button.setObjectName(u"PlayList")
        self.playlist_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.playlist_button.setStyleSheet(u"")
        self.playlist_button.setMinimumSize(QSize(150, 50))
        self.home_combobox_layout.addWidget(self.playlist_button)

        # Add the combo box layout to the horizontal layout
        self.home_horizontalLayout_row_6.addSpacing(10)  # Add space between thumbnail and combo boxes
        self.home_horizontalLayout_row_6.addLayout(self.home_combobox_layout)
        self.home_horizontalLayout_row_6.addStretch(1)  # Add stretch to the right for centering


       

        self.home_verticalLayout.addWidget(self.home_row_1)
        self.home_verticalLayout.addWidget(self.home_row_2)
        self.home_verticalLayout.addWidget(self.home_row_3)
        self.home_verticalLayout.addWidget(self.home_row_6)
        self.home_verticalLayout.addWidget(self.home_row_4)
        self.home_verticalLayout.addWidget(self.home_row_5)



        


        self.stackedWidget.addWidget(self.home)

        
        # Create new page for the application
        # Create new page for the application
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")  # Placeholder style (can be customized)

        # Set vertical layout for the page
        self.verticalLayout = QVBoxLayout(self.widgets)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        # First Frame to hold 10 buttons (5 on each row)
        self.frame1 = QFrame(self.widgets)
        self.frame1.setObjectName("frame1")
        self.frame1.setFrameShape(QFrame.StyledPanel)

        # Vertical layout for buttons (will contain 2 rows of buttons)
        self.buttonsLayout = QVBoxLayout(self.frame1)
        self.buttonsLayout.setSpacing(10)
        self.buttonsLayout.setObjectName("buttonsLayout")

        # First row (Horizontal layout)
        self.row1Layout = QHBoxLayout()
        self.row1Layout.setSpacing(10)
        self.row1Layout.setObjectName("row1Layout")

        # First 5 buttons in the first row
        self.resume = QPushButton("Resume", self.frame1)
        self.resume.setMinimumSize(QSize(150, 50))
        self.resume.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resume.setIcon(icon9)
        ###################################################################################################
        self.cancel = QPushButton("Cancel", self.frame1)
        self.cancel.setMinimumSize(QSize(150, 50))
        self.cancel.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/icons/cil-cancel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.cancel.setIcon(icon10)
        ###################################################################################################
        self.refresh = QPushButton("Refresh", self.frame1)
        self.refresh.setMinimumSize(QSize(150, 50))
        self.refresh.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon11 = QIcon()
        icon11.addFile(u":/icons/images/icons/cil-refresh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.refresh.setIcon(icon11)
        ###################################################################################################
        # self.folder = QPushButton("Folder", self.frame1)
        # self.folder.setMinimumSize(QSize(150, 50))
        # self.folder.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        # icon12 = QIcon()
        # icon12.addFile(u":/icons/images/icons/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        # self.folder.setIcon(icon12)
        ###################################################################################################
        self.d_window = QPushButton("D. Window", self.frame1)
        self.d_window.setMinimumSize(QSize(150, 50))
        self.d_window.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon13 = QIcon()
        icon13.addFile(u":/icons/images/icons/cil-d_window.png", QSize(), QIcon.Normal, QIcon.Off)
        self.d_window.setIcon(icon13)
        ####################################################################################################

        # Add first 5 buttons to the first row
        self.row1Layout.addWidget(self.resume)
        self.row1Layout.addWidget(self.cancel)
        self.row1Layout.addWidget(self.refresh)
        #self.row1Layout.addWidget(self.folder)
        self.row1Layout.addWidget(self.d_window)

        # Second row (Horizontal layout)
        self.row2Layout = QHBoxLayout()
        self.row2Layout.setSpacing(10)
        self.row2Layout.setObjectName("row2Layout")

        # Next 5 buttons in the second row
        self.resume_all = QPushButton("Resume All", self.frame1)
        self.resume_all.setMinimumSize(QSize(150, 50))
        self.resume_all.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon14 = QIcon()
        icon14.addFile(u":/icons/images/icons/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resume_all.setIcon(icon14)
        self.stop_all = QPushButton("Stop All", self.frame1)
        self.stop_all.setMinimumSize(QSize(150, 50))
        self.stop_all.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon15 = QIcon()
        icon15.addFile(u":/icons/images/icons/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_all.setIcon(icon15)
        self.schedule_all = QPushButton("Schedule All", self.frame1)
        self.schedule_all.setMinimumSize(QSize(150, 50))
        self.schedule_all.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon16 = QIcon()
        icon16.addFile(u":/icons/images/icons/cil-schedule.png", QSize(), QIcon.Normal, QIcon.Off)
        self.schedule_all.setIcon(icon16)
        self.delete = QPushButton("Delete", self.frame1)
        self.delete.setMinimumSize(QSize(150, 50))
        self.delete.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon17 = QIcon()
        icon17.addFile(u":/icons/images/icons/cil-delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.delete.setIcon(icon17)
        self.delete_all = QPushButton("Delete All", self.frame1)
        self.delete_all.setMinimumSize(QSize(150, 50))
        self.delete_all.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon18 = QIcon()
        icon18.addFile(u":/icons/images/icons/cil-delete_all.png", QSize(), QIcon.Normal, QIcon.Off)
        self.delete_all.setIcon(icon18)

        # Add the next 5 buttons to the second row
        self.row2Layout.addWidget(self.resume_all)
        self.row2Layout.addWidget(self.stop_all)
        self.row2Layout.addWidget(self.schedule_all)
        self.row2Layout.addWidget(self.delete)
        self.row2Layout.addWidget(self.delete_all)

        # Add both rows to the buttons layout
        self.buttonsLayout.addLayout(self.row1Layout)  # Add first row to the layout
        self.buttonsLayout.addLayout(self.row2Layout)  # Add second row to the layout

        # Add the first frame (buttons frame) to the main vertical layout
        self.verticalLayout.addWidget(self.frame1)

        # Adjusting the frame2 where the table will reside
        self.frame2 = QFrame(self.widgets)
        self.frame2.setObjectName(u"frame2")
        self.frame2.setMinimumSize(QSize(0, 300))  # Adjust as necessary
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Raised)

        # Layout for the table widget
        self.horizontalLayout_12 = QHBoxLayout(self.frame2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)

        # Table widget setup


        

        self.tableWidget = QTableWidget(self.frame2)
        self.tableWidget.setObjectName(u"tableWidget")

        # Set 8 columns and 3 rows
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(90)

        # Set the horizontal header labels
        headers = ["ID", "Name", "Progress", "Speed", "Left", "Done", "Size", "Status", "I"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        # Enable row selection
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # or MultiSelection for multiple rows

        # # Set the table widget's size policy to expand
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       

        

        # Make the horizontal header visible and ensure columns resize appropriately
        #self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)  # Adjust column size if needed

        # Vertical header can be hidden (optional)
        self.tableWidget.verticalHeader().setVisible(False)

        

        # Add the table widget to the frame's layout
        self.horizontalLayout_12.addWidget(self.tableWidget)

        # Add the second frame (table frame) to the main vertical layout
        self.verticalLayout.addWidget(self.frame2)


        # Add the new page to the stacked widget
        self.stackedWidget.addWidget(self.widgets)

        # Apply style sheet to change context menu background to black
        self.tableWidget.setStyleSheet("""

        QTableWidget QMenu {
                background-color: black;
                color: white;
        }
        QTableWidget QMenu::item:selected {
                background-color: rgb(53, 57, 63);
                color: white;
        }
        """)





        
        ###############################################################################################################
        
        
        # Create a new page (QWidget)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")

        # Main layout for the page (QVBoxLayout)
        self.verticalLayout_20 = QVBoxLayout(self.new_page)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")

        # First frame for the "Detailed events" label
        self.frame1 = QFrame(self.new_page)
        self.frame1.setObjectName(u"frame1")
        self.frame1.setFrameShape(QFrame.StyledPanel)
        self.frame1.setFrameShadow(QFrame.Raised)
        self.frame1.setMinimumSize(QSize(0, 50))  # Set a minimum size for the label frame

        # Layout for the first frame
        self.horizontalLayout_1 = QHBoxLayout(self.frame1)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")

        # "Detailed events" label
        self.detailedEventsLabel = QLabel(self.frame1)
        self.detailedEventsLabel.setObjectName(u"detailedEventsLabel")
        self.detailedEventsLabel.setText("Detailed events")
        font = QFont()
        font.setPointSize(12)  # Adjust the font size for visibility
        font.setBold(True)
        self.detailedEventsLabel.setFont(font)

        # Add the label to the frame's layout
        self.horizontalLayout_1.addWidget(self.detailedEventsLabel)

        # Add the first frame to the page layout
        self.verticalLayout_20.addWidget(self.frame1)

        # Second frame for the terminal/log display
        self.frame2 = QFrame(self.new_page)
        self.frame2.setObjectName(u"frame2")
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Raised)
        self.frame2.setStyleSheet("background-color: black;")  # Set the background to black
        self.frame2.setMinimumSize(QSize(0, 200))  # Adjust the minimum size for the terminal

        # Layout for the second frame (Terminal-style display)
        self.verticalLayout_terminal = QVBoxLayout(self.frame2)
        self.verticalLayout_terminal.setObjectName(u"verticalLayout_terminal")

        # Text edit or label for displaying logs (simulating a terminal)
        self.logDisplay = QTextEdit(self.frame2)
        #self.logDisplay.insertPlainText("This is me")
        self.logDisplay.setObjectName(u"logDisplay")
        self.logDisplay.setReadOnly(True)  # Make it read-only since it's a log display
        self.logDisplay.setStyleSheet("color: white; background-color: black;")  # White text on black background

        # Add the log display to the second frame
        self.verticalLayout_terminal.addWidget(self.logDisplay)

        # Add the second frame to the page layout
        self.verticalLayout_20.addWidget(self.frame2)


        self.stackedWidget.addWidget(self.new_page)

        ##############################################################################################################





        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        # Start with your existing frame and layout setup
        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)

        # # Add the top detail separator
        # self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        # self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        # self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        # self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        # self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        # self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        # Clear any existing widgets and layouts in the right sidebar
        # for i in reversed(range(self.verticalLayout_7.count())): 
        #         widget = self.verticalLayout_7.itemAt(i).widget()
        #         if widget is not None: 
        #                 widget.deleteLater()

        # FIRST FRAME: General Settings
        self.generalFrame = QFrame(self.extraRightBox)
        self.generalFrame.setObjectName(u"generalFrame")
        self.generalFrame.setFrameShape(QFrame.NoFrame)
        self.generalFrame.setFrameShadow(QFrame.Raised)

        self.generalLayout = QVBoxLayout(self.generalFrame)
        self.generalLayout.setSpacing(10)
        self.generalLayout.setContentsMargins(10, 10, 10, 10)

        # General Label
        self.label_general = QLabel(self.generalFrame)
        self.label_general.setObjectName(u"label_general")
        self.label_general.setText("General")
        self.label_general.setFont(QFont("Arial", 12, QFont.Bold))

        self.generalLayout.addWidget(self.label_general)

        # QLabel and QComboBox on one row
        self.generalSettingsRow = QFrame(self.generalFrame)
        self.generalSettingsRow.setObjectName(u"generalSettingsRow")
        self.generalRowLayout = QHBoxLayout(self.generalSettingsRow)
        self.generalRowLayout.setSpacing(10)
        self.generalRowLayout.setContentsMargins(0, 0, 0, 0)

        # Label for combo box
        self.label_setting = QLabel(self.generalSettingsRow)
        self.label_setting.setObjectName(u"label_setting")
        self.label_setting.setText("Choose Setting:")

        # Combo box for settings
        self.combo_setting = QComboBox(self.generalSettingsRow)
        self.combo_setting.setObjectName(u"combo_setting")
        self.combo_setting.addItems(["Local", "Global"])

        # Add to row layout
        self.generalRowLayout.addWidget(self.label_setting)
        self.generalRowLayout.addWidget(self.combo_setting)

        # Add row to general layout
        self.generalLayout.addWidget(self.generalSettingsRow)

        # Four Checkboxes for general settings
        self.monitor_clipboard = QCheckBox("Monitor Copied Urls", self.generalFrame)
        # Set default value (checked or unchecked)
        # self.monitor_clipboard.setChecked(True)  # This will set it as checked by default

        self.checkBox2 = QCheckBox("Show Download Window", self.generalFrame)
        self.checkBox3 = QCheckBox("Auto close DL Window", self.generalFrame)
        self.checkBox4 = QCheckBox("Show Thumbnail", self.generalFrame)

        self.generalLayout.addWidget(self.monitor_clipboard)
        self.generalLayout.addWidget(self.checkBox2)
        self.generalLayout.addWidget(self.checkBox3)
        self.generalLayout.addWidget(self.checkBox4)


        # QLabel and QComboBox on one row
        self.generalSegmentRow = QFrame(self.generalFrame)
        self.generalSegmentRow.setObjectName(u"generalSegmentRow")
        self.generalSegRowLayout = QHBoxLayout(self.generalSegmentRow)
        self.generalSegRowLayout.setSpacing(10)
        self.generalSegRowLayout.setContentsMargins(0, 0, 0, 0)

        # Label for combo box
        self.label_segment = QLabel("Segment",self.generalSegmentRow)
        self.label_segment.setObjectName(u"label_segment")

        # Combo box for segment settings
        self.segment_combo_setting = QComboBox(self.generalSegmentRow)
        self.segment_combo_setting.setObjectName(u"segment_combo_setting")
        self.segment_combo_setting.addItems(["KB", "MB"])

        # Line edit for segment settings
        self.lineEdit_segment = QLineEdit(self.generalSegmentRow)
        self.lineEdit_segment.setPlaceholderText("")
        self.lineEdit_segment.setMinimumSize(QSize(20, 30))


        # Add to row layout
        self.generalSegRowLayout.addWidget(self.label_segment)
        self.generalSegRowLayout.addWidget(self.lineEdit_segment)
        self.generalSegRowLayout.addWidget(self.segment_combo_setting)
        

        # Add row to general layout
        self.generalLayout.addWidget(self.generalSegmentRow)

        
        
        # Add the first frame to the right sidebar layout
        self.verticalLayout_7.addWidget(self.generalFrame)

        
        # SECOND FRAME: Connection and Network Settings
        self.connectionFrame = QFrame(self.extraRightBox)
        self.connectionFrame.setObjectName(u"connectionFrame")
        self.connectionFrame.setFrameShape(QFrame.NoFrame)
        self.connectionFrame.setFrameShadow(QFrame.Raised)

        self.connectionLayout = QVBoxLayout(self.connectionFrame)
        self.connectionLayout.setSpacing(10)
        self.connectionLayout.setContentsMargins(10, 10, 10, 10)

        # Connection and Network Settings Label
        self.label_connection = QLabel(self.connectionFrame)
        self.label_connection.setObjectName(u"label_connection")
        self.label_connection.setText("Connection / Network")
        self.label_connection.setFont(QFont("Arial", 12, QFont.Bold))

        self.connectionLayout.addWidget(self.label_connection)

        # QCheckBox and QLineEdit on one row (for network settings)
        self.connectionSettingsRow = QFrame(self.connectionFrame)
        self.connectionSettingsRow.setObjectName(u"connectionSettingsRow")
        self.connectionRowLayout = QHBoxLayout(self.connectionSettingsRow)
        self.connectionRowLayout.setSpacing(10)
        self.connectionRowLayout.setContentsMargins(0, 0, 0, 0)

        # Checkbox for network
        self.checkBox_network = QCheckBox("Speed Limit", self.connectionSettingsRow)

        # QLineEdit for network input
        self.lineEdit_network = QLineEdit(self.connectionSettingsRow)
        self.lineEdit_network.setPlaceholderText("e.g., 50k, 10kb, 2m, 2mb")
        self.lineEdit_network.setMinimumSize(QSize(20, 30))

        # Add to row layout
        self.connectionRowLayout.addWidget(self.checkBox_network)
        self.connectionRowLayout.addWidget(self.lineEdit_network)

        # Add row to connection layout
        self.connectionLayout.addWidget(self.connectionSettingsRow)

        # --- First new row: Max Concurrent Downloads ---
        self.concurrentDownloadsRow = QFrame(self.connectionFrame)
        self.concurrentDownloadsRow.setObjectName(u"concurrentDownloadsRow")
        self.concurrentRowLayout = QHBoxLayout(self.concurrentDownloadsRow)
        self.concurrentRowLayout.setSpacing(10)
        self.concurrentRowLayout.setContentsMargins(0, 0, 0, 0)

        # Label for Max Concurrent Downloads
        self.label_max_downloads = QLabel(self.concurrentDownloadsRow)
        self.label_max_downloads.setText("Max Concurrent \n Downloads:")

        # Combo box for Max Concurrent Downloads (1 to 100)
        self.combo_max_downloads = QComboBox(self.concurrentDownloadsRow)
        self.combo_max_downloads.addItems([str(i) for i in range(1, 101)])  # Values from 1 to 100

        # Add to row layout
        self.concurrentRowLayout.addWidget(self.label_max_downloads)
        self.concurrentRowLayout.addWidget(self.combo_max_downloads)

        # Add row to connection layout
        self.connectionLayout.addWidget(self.concurrentDownloadsRow)

        # --- Second new row: Max Connection Settings ---
        self.connectionSettingsRow2 = QFrame(self.connectionFrame)
        self.connectionSettingsRow2.setObjectName(u"connectionSettingsRow2")
        self.connectionRowLayout2 = QHBoxLayout(self.connectionSettingsRow2)
        self.connectionRowLayout2.setSpacing(10)
        self.connectionRowLayout2.setContentsMargins(0, 0, 0, 0)

        # Label for Max Connection Settings
        self.label_max_connections = QLabel(self.connectionSettingsRow2)
        self.label_max_connections.setText("Max Connection \n Settings:")

        # Combo box for Max Connection Settings (1 to 100)
        self.combo_max_connections = QComboBox(self.connectionSettingsRow2)
       
        self.combo_max_connections.addItems([str(i) for i in range(1, 101)])  # Values from 1 to 100

        # Add to row layout
        self.connectionRowLayout2.addWidget(self.label_max_connections)
        self.connectionRowLayout2.addWidget(self.combo_max_connections)

        # Add row to connection layout
        self.connectionLayout.addWidget(self.connectionSettingsRow2)

        # --- Third new row: Proxy Settings ---
        self.proxySettingsRow = QFrame(self.connectionFrame)
        self.proxySettingsRow.setObjectName(u"proxySettingsRow")
        self.proxyRowLayout = QVBoxLayout(self.proxySettingsRow)  # Changed to QVBoxLayout for the new line
        self.proxyRowLayout.setSpacing(10)
        self.proxyRowLayout.setContentsMargins(0, 0, 0, 0)

        # First row layout for the checkbox, line edit, and combo box
        self.proxyTopRowLayout = QHBoxLayout()
        self.proxyTopRowLayout.setSpacing(10)
        self.proxyTopRowLayout.setContentsMargins(0, 0, 0, 0)

        # Checkbox for enabling/disabling proxy settings
        self.checkBox_proxy = QCheckBox("Proxy", self.proxySettingsRow)

        # QLineEdit for Proxy Address Input
        self.lineEdit_proxy = QLineEdit(self.proxySettingsRow)
        self.lineEdit_proxy.setPlaceholderText("Enter Proxy IP or Domain")
        self.lineEdit_proxy.setMinimumSize(QSize(70, 30))

        # Combo box for Proxy Types (HTTP, HTTPS, SOCKS5)
        self.combo_proxy_type = QComboBox(self.proxySettingsRow)
        self.combo_proxy_type.addItems(['http', 'https', 'socks4', 'socks5'])

        # Add widgets to the first row layout
        self.proxyTopRowLayout.addWidget(self.checkBox_proxy)
        self.proxyTopRowLayout.addWidget(self.lineEdit_proxy)
        self.proxyTopRowLayout.addWidget(self.combo_proxy_type)

        # Add the first row layout to the main proxy settings layout
        self.proxyRowLayout.addLayout(self.proxyTopRowLayout)

        # Add a spacer to create separation between the rows
        self.proxyRowLayout.addSpacerItem(QSpacerItem(10, 2, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Label for additional information, added below the combo box
        self.label_proxy_info = QLabel(self.proxySettingsRow)

        # Add the label to the main layout, after the first row
        self.proxyRowLayout.addWidget(self.label_proxy_info)

        # Add the entire proxy settings row to the connection layout
        self.connectionLayout.addWidget(self.proxySettingsRow)


        # Add the second frame to the right sidebar layout
        self.verticalLayout_7.addWidget(self.connectionFrame)


        # THIRD FRAME: Updates
        self.updateFrame = QFrame(self.extraRightBox)
        self.updateFrame.setObjectName(u"updateFrame")
        self.updateFrame.setFrameShape(QFrame.NoFrame)
        self.updateFrame.setFrameShadow(QFrame.Raised)

        self.updateLayout = QVBoxLayout(self.updateFrame)
        self.updateLayout.setSpacing(10)
        self.updateLayout.setContentsMargins(10, 10, 10, 10)

        # Updates Label
        self.label_updates = QLabel(self.updateFrame)
        self.label_updates.setObjectName(u"label_updates")
        self.label_updates.setText("Updates")
        self.label_updates.setFont(QFont("Arial", 12, QFont.Bold))

        self.updateLayout.addWidget(self.label_updates)

        # --- First new row: Check for updates ---
        
        self.checkforupdateRow = QFrame(self.updateFrame)
        self.checkforupdateRow.setObjectName(u"concurrentDownloadsRow")
        self.checkupdateRowLayout = QHBoxLayout(self.checkforupdateRow)
        self.checkupdateRowLayout.setSpacing(10)
        self.checkupdateRowLayout.setContentsMargins(0, 0, 0, 0)

        # Label for Max Concurrent Downloads
        self.label_check_every = QLabel(self.checkforupdateRow)
        self.label_check_every.setText("Check for update \n every:")

        # Combo box for Max Concurrent Downloads (1 to 100)
        self.combo_check_update = QComboBox(self.checkforupdateRow)
        self.combo_check_update.addItems(['1', '7', '30'])  # Values from 1 to 100

        # Add to row layout
        self.checkupdateRowLayout.addWidget(self.label_check_every)
        self.checkupdateRowLayout.addWidget(self.combo_check_update)

        # Add row to connection layout
        self.updateLayout.addWidget(self.checkforupdateRow)



        # --- Second new row: Update button --------
        self.updatebuttonRow = QFrame(self.updateFrame)
        self.updatebuttonRowLayout = QHBoxLayout(self.updatebuttonRow)
        self.updatebuttonRowLayout.setSpacing(10)
        self.updatebuttonRowLayout.setContentsMargins(0, 0, 0, 0)

        # Version label
        self.version_label = QLabel(self.updateFrame)
        self.updateLayout.addWidget(self.version_label)

        self.update_button = QPushButton('Check for update', self.updatebuttonRow)
        self.update_button.setMinimumSize(QSize(80, 25))
        self.update_button.setFont(font)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        
        self.updatebuttonRowLayout.addWidget(self.update_button)
        self.updateLayout.addWidget(self.updatebuttonRow)

        # # --- Third new row: YT-DLP Update button --------
        # self.ytdlp_updatebuttonRow = QFrame(self.updateFrame)
        # self.ytdlp_updatebuttonRowLayout = QHBoxLayout(self.ytdlp_updatebuttonRow)
        # self.ytdlp_updatebuttonRowLayout.setSpacing(10)
        # self.ytdlp_updatebuttonRowLayout.setContentsMargins(0, 0, 0, 0)

        # # Version label
        # self.ytdlp_version_label = QLabel(self.updateFrame)
        # self.updateLayout.addWidget(self.ytdlp_version_label)

        # self.ytdlp_update_button = QPushButton('Check for update', self.ytdlp_updatebuttonRow)
        # self.ytdlp_update_button.setMinimumSize(QSize(80, 25))
        # self.ytdlp_update_button.setFont(font)
        # self.ytdlp_update_button.setCursor(QCursor(Qt.PointingHandCursor))
        # self.ytdlp_update_button.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        
        # self.ytdlp_updatebuttonRowLayout.addWidget(self.ytdlp_update_button)
        # self.updateLayout.addWidget(self.ytdlp_updatebuttonRow)



        # Add the third frame to the right sidebar layout
        self.verticalLayout_7.addWidget(self.updateFrame)

        # Finally, add the sidebar to the main layout
        self.horizontalLayout_4.addWidget(self.extraRightBox)




        #self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)

        # Layout for the bottom bar
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        # Credits label
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setBold(False)
        font5.setItalic(False)
        self.creditsLabel.setFont(font5)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        # New frame for status code and total speed
        self.statusSpeedFrame = QFrame(self.bottomBar)
        self.statusSpeedFrame.setObjectName(u"statusSpeedFrame")
        self.statusSpeedFrame.setMinimumSize(QSize(0, 22))
        self.statusSpeedFrame.setMaximumSize(QSize(16777215, 22))
        self.statusSpeedFrame.setFrameShape(QFrame.NoFrame)
        self.statusSpeedFrame.setFrameShadow(QFrame.Raised)

        # Horizontal layout for the status code and total speed
        self.horizontalLayout_statusSpeed = QHBoxLayout(self.statusSpeedFrame)
        self.horizontalLayout_statusSpeed.setSpacing(10)  # Adjust spacing between labels
        self.horizontalLayout_statusSpeed.setObjectName(u"horizontalLayout_statusSpeed")
        self.horizontalLayout_statusSpeed.setContentsMargins(0, 0, 0, 0)

        # Label for Status Code
        self.statusCodeLabel = QLabel(self.statusSpeedFrame)
        self.statusCodeLabel.setObjectName(u"statusCodeLabel")
        self.statusCodeLabel.setText("Status Code:")
        self.horizontalLayout_statusSpeed.addWidget(self.statusCodeLabel)

        # Value for Status Code
        self.statusCodeValue = QLabel(self.statusSpeedFrame)
        self.statusCodeValue.setObjectName(u"statusCodeValue")
        #self.statusCodeValue.setStyleSheet(u"background-color: white;")
        #self.statusCodeValue.setText("200")  # Default value
        self.horizontalLayout_statusSpeed.addWidget(self.statusCodeValue)

        # Label for Total Speed
        self.totalSpeedLabel = QLabel(self.statusSpeedFrame)
        self.totalSpeedLabel.setObjectName(u"totalSpeedLabel")
        self.totalSpeedLabel.setText("Total Speed:")
        self.horizontalLayout_statusSpeed.addWidget(self.totalSpeedLabel)

        # Value for Total Speed
        self.totalSpeedValue = QLabel(self.statusSpeedFrame)
        self.totalSpeedValue.setObjectName(u"totalSpeedValue")
        self.totalSpeedValue.setText("⬇ 0 bytes/s")  # Default value
        #self.totalSpeedValue.setStyleSheet(u"background-color: white;")
        self.horizontalLayout_statusSpeed.addWidget(self.totalSpeedValue)

        # Add the statusSpeedFrame to the bottom bar's layout
        self.horizontalLayout_5.addWidget(self.statusSpeedFrame)

        # Version label
        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.horizontalLayout_5.addWidget(self.version)

        # Frame size grip (resize control)
        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5.addWidget(self.frame_size_grip)

        # Add the bottom bar to the vertical layout
        self.verticalLayout_6.addWidget(self.bottomBar)

        self.verticalLayout_2.addWidget(self.contentBottom)

        self.appLayout.addWidget(self.contentBox)

        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

      # Inside your Ui_MainWindow class
    def retranslateUi(self, MainWindow):
        # Simply call the imported method here and pass MainWindow as a parameter
      retranslateUi(self, MainWindow)

