#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys

DEBUG_PORT = '5588'
DEBUG_URL = 'http://127.0.0.1:%s' % DEBUG_PORT
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT
inspector = False

class Zer(QMainWindow):

    def __init__(self, *args, **kwargs ):

        super(Zer, self).__init__(*args, **kwargs)

        self.homepage = 'http://www.bing.com'

        self.inspector = None
        if inspector:
            self.create_inspector()

        self.create_toolbar()
        self.create_tabs()
        self.show()
        self.setWindowTitle( 'Zer' )

    def create_inspector( self ):
        self.inspector = QWebEngineView()
        self.inspector.setWindowTitle('Web Inspector')
        self.inspector.load(QUrl(DEBUG_URL))
        self.inspector.show()

    def create_toolbar( self ):
        self.toolbar =  QToolBar( 'ToolBar' )
        self.addToolBar( self.toolbar )
        self.home_btn = QAction( QIcon( './home.png' ), 'Home', self )
        self.home_btn.triggered.connect( self.home )
        self.toolbar.addAction( self.home_btn )

        self.toolbar.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect( self.to_url )
        self.toolbar.addWidget( self.urlbar )

        self.toolbar.addSeparator()
        self.close_btn = QAction( QIcon( './close.png' ), 'Close', self )
        self.close_btn.triggered.connect( self.close )
        self.toolbar.addAction( self.close_btn )

    def create_tabs( self ):
        self.tabs = QTabWidget();
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.new_tab_by_click)
        self.tabs.currentChanged.connect(self.switch_tab)
        self.setCentralWidget(self.tabs)
        self.new_tab( label='Homepage' )

    def to_url( self ):
        url = QUrl( self.urlbar.text() )
        if url.scheme() == '':
            url.setScheme( 'http' )
        self.tabs.currentWidget().setUrl(url)

    def close_tab( self, i ):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def new_tab_by_click( self, i ):
        self.new_tab()

    def new_tab( self, url=None, label = 'Blank' ):
        if url is None:
            url = self.homepage
        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        browser.setUrl( QUrl(url) )
        i = self.tabs.addTab( browser, label )
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect( lambda _, i = i, browser = browser: self.update( i, browser ) )
        browser.loadFinished.connect( lambda _, i = i, browser = browser: self.update( i, browser ) )

    def switch_tab( self, i ):
        self.urlbar.setText( self.tabs.currentWidget().url().toString() )
        self.setWindowTitle( "[Zer] %s"%self.tabs.currentWidget().page().title() )

        if self.inspector is not None:
            self.tabs.currentWidget().page().setDevToolsPage(self.inspector.page())

    def update( self, i, browser ):
        self.tabs.setTabText( i, browser.page().title() )
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText( browser.url().toString() )

    def home( self ):
        self.tabs.currentWidget().setUrl( QUrl( self.homepage ) )

    def close( self ):
        super().close()
        if self.inspector is not None:
            self.inspector.close()

if "--zer-tool" in sys.argv or "-zer-tool" in sys.argv:
    inspector = True

app = QApplication(sys.argv)
app.setApplicationName('Zer')
zer = Zer()
app.exec_()
