

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

import qasync
class FriendRequest(QFrame): 
    def __init__(self, id, user, main_window):
        super().__init__()
        # user = (element["username"], element["relationship_id"], element["name"], element["birth"], element["status"], element["status_relationship"])
        self.setObjectName("friend_request")

        self.user = user 
        self.relationship_id = id
        self.main_window = main_window
        # self.setFixedHeight(35)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.button_frame = QFrame(self)
        self.button_frame_layout = QHBoxLayout(self.button_frame)
        """
        #friend_request{
            border: none; 
            border-radius: 10 px; 
            background-color: #111111; 
        }
        #friend_request #label_name{
        }
        #friend_request #deny_button{
            font-weight:bold;
            border: none; 
            border-radius: 10px;
            background-color : #eff3fe; 
            padding: 2px 2px;
        }
        #friend_request #accept_button{
            font-weight:bold;
            border: none; 
            border-radius: 10px;
            background-color : #5A86FA; 
            padding: 2px 2px;
        }
        """
        self.label_name = QLabel(f"{self.user[2]} - {self.user[3]}")
        self.label_name.setObjectName("label_name")
       
        self.deny_button = QPushButton("Deny")
        self.deny_button.setObjectName("deny_button")
       
      
        self.accept_button = QPushButton("Accept")
        self.accept_button.setObjectName("accept_button")
       

        self.button_frame_layout.addWidget(self.accept_button)
        self.button_frame_layout.addWidget(self.deny_button)

        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.button_frame)
       
        self.accept_button.clicked.connect(self.accept_event) 
        self.deny_button.clicked.connect(self.deny_event)

    @qasync.asyncSlot()
    async def accept_event(self): 
        await self.main_window.accept_event(self.relationship_id, self)
    @qasync.asyncSlot()
    async def deny_event(self):
        await self.main_window.deny_event(self.relationship_id, self)
    





        
        
