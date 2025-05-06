

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
import qasync
class Profile(QFrame): 
    def __init__(self, me, id, user, main_window, type):
        super().__init__()
        
        # user = (element["username"], element["relationship_id"], element["name"], element["birth"], element["status"], element["status_relationship"])
        self.me = me
        self.user = list(user)
        self.relationship_id = id
        self.main_window = main_window
        
        
        
        self.label_username = QLabel(self.user[0])
        self.label_name = QLabel(f"{self.user[2]} - {self.user[3]}")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.type = self.user[-1]
        self.status_button_1 = { 
            "pending" : "Cancel friend request", # mình chờ người ta chấp nhận lời mời kết bạn
            "friend" : "Friend",
            "sent" : "Accept", # người ta gửi lời mới kết bạn cho mình
            "add_friend" : "Add friend"
        }
        self.status_button_2 = { 
            "sent" : "Deny"
        }
        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.label_name)
        
        if type == "search" and self.user[0] != self.me:
            self.button_frame = QFrame() 
            self.layout_button_frame = QHBoxLayout(self.button_frame) 

            self.accept_button = QPushButton()
    
            self.layout_button_frame.addWidget(self.accept_button)
    
            self.deny_button = QPushButton()
        
            self.layout_button_frame.addWidget(self.deny_button)

            self.accept_button.clicked.connect(self.accept_event)
            self.deny_button.clicked.connect(self.deny_event)

            self.button_frame.setLayout(self.layout_button_frame)
            self.layout.addWidget(self.button_frame)
            self.refresh_button()
            self.setFixedHeight(70)
        else: 
            self.setFixedHeight(50)
        self.setLayout(self.layout)
     
      
        
        
   
   


    @qasync.asyncSlot()
    async def accept_event(self):
        if self.type == "pending":
            self.type = "add_friend"
           # HỦY LOI MOI KET BAN
            await self.main_window.deny_friend_request(self.user[1])
        elif self.type == "sent":
            self.type = "friend"
            await self.main_window.accept_friend_request(self.user[1])
        elif self.type == "add_friend":
            self.type = "pending" #
            await self.main_window.send_friend_request(self.user[0])
        elif self.type == "friend":
            self.type = "add_friend"
            await self.main_window.unfriend_event(self.user[1])
        self.refresh_button()

    @qasync.asyncSlot()
    async def deny_event(self):
        if self.type == "friend":
            print("CHUYEN SANG MAN HINH NHAN TIN")
            await self.main_window.back_to_main_chat(self)
        else:
            self.type = "add_friend"
            await self.main_window.deny_event(id, self)

        
        self.refresh_button()
       
    # cập nhật id bạn bè
    def update_relationship_id(self): 
        return 0
    
    def refresh_button(self):
        self.accept_button.setText(self.status_button_1[self.type])
        
        if self.type in self.status_button_2: 
            self.deny_button.setText(self.status_button_2[self.type])
            self.deny_button.show()
        else: 
            self.deny_button.hide()


    def get_info(self): 
        return (self.user[0], self.user[2])
    def get_index(self): 
        return 0 # trả về conversation_id với người này ( nếu đã kết bạn )
    def update(self, relationship_id):
        self.relationship_id = relationship_id 
        self.user[1] = self.relationship_id
        self.user[-1] = self.type

  


        