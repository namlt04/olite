

from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QSizePolicy, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFocusEvent, QMouseEvent
import textwrap
class OneMessage(QFrame): 
    def __init__(self, message,me,name, main_window):
         # (5, 'NV005', 1, 'Tôi vừa hoàn thành báo cáo.', '2024-02-27 08:20:00', 1, 0)
        super().__init__()
        print(message)
        
        self.message = message
        self.name = name
        self.main_window = main_window
        self.me = me
        self.setObjectName("one_message")
        style = """
        #one_message{
        border : none ;
        background-color: #f1f1f1;
        }
        """
      
        self.layout = QVBoxLayout()
        self.username_label = QLabel(self.name[message[1]] if message[1] != self.me else "You")

        self.time_label = QLabel(message[4])

        msg = textwrap.fill(message[3], width=50)
        self.message_label = QLabel(msg)
        self.message_label.setObjectName("message_label")
        style = style + """
        #message_label{
        background-color: #ffffff; 
        padding : 5px 5px;
        border: none; 
        border-radius: 8px;
        """
        if ( message[-1] == 1):     # NẾU CHỨA FILE, IN ĐẬM NỘI DUNG ( file_name )
            style = style + """
                font-weight: bold; 
                color : red;
                text-decoration : underline;
            """
            self.message_label.mousePressEvent = self.click_event
        
            
      
        
     
        self.message_label.setAlignment(Qt.AlignLeft)
        if ( message[1] == self.me): 
            style += "background: #5A86FA;"
            self.layout.setAlignment(Qt.AlignRight)
            self.username_label.setAlignment(Qt.AlignRight)
        else: 
            self.layout.setAlignment(Qt.AlignLeft)
            self.username_label.setAlignment(Qt.AlignLeft)
            
        self.message_label.setToolTip(self.time_label.text())
       
        self.message_label.adjustSize()
        self.message_label.setMaximumWidth(400)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.message_label)
        self.setLayout(self.layout) 
        style += "\n}"
        self.setStyleSheet(style)
        

    def click_event(self, event: QMouseEvent): 
            self.main_window.handle_download_file(self.message[0], self.message[3])
            


 

      
