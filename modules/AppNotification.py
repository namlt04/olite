from winotify import Notification, audio


class AppNotification :
    def __init__(self, msg): 
        self.noti = Notification("OLite", "Ban co 1 thong bao moi", msg, icon = "icons\\olite.ico")
        self.noti.set_audio(audio.Default, loop = False)
        self.run()
    
    def run(self): 
        self.noti.show() 