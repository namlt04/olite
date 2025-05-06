
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction


class SystemTrayIcon : 
    def __init__(self, main_windows):
        self.main_windows = main_windows 
        self.tray_icon = QSystemTrayIcon(QIcon("icons\\olite.ico"), main_windows)
       
        self.tray_icon.setToolTip("QLite - Local chat")


        menu = QMenu(self.main_windows)
        restore_action = QAction("Mở", main_windows)
        restore_action.triggered.connect(self.handle_restore)
        exit_action = QAction("Thoát", main_windows)
        exit_action.triggered.connect(self.handle_exit)
        
        menu.addAction(restore_action)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.on_tray_icon_clicked)
        self.tray_icon.show()
    def on_tray_icon_clicked(self, reason): 
        if reason == QSystemTrayIcon.ActivationReason.Trigger : 
           self.handle_restore()
    
    def handle_restore(self):
        self.main_windows.showNormal()

    
    def handle_exit(self): 
        self.tray_icon.hide()
        QApplication.quit()