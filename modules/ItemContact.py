

from PySide6.QtWidgets import QVBoxLayout, QLabel,  QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
class ItemContact(QFrame): 
    def __init__(self, conversation_id, conversation_name, information, main_window):
        super().__init__()
        self.setObjectName("item_contact")
        self.conversation_id = conversation_id
        self.setFixedHeight(50)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.main_window = main_window
        # l, t, r, b
        self.layout.setContentsMargins(8,0,0,0)
        
        self.name_label = QLabel(f"{conversation_name}", self)
        self.name_label.setObjectName("name_label")
        self.status_label = QLabel(information, self) 
        self.status_label.setObjectName("status_label")
        """
        
        """
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.status_label)
    
        self.mousePressEvent = self.click_event
    
    def update_status(self, status): 
        self.status_label.setText(status)
    def click_event(self, event: QMouseEvent): 
        self.main_window.handle_item(self)
    def get_index(self):
        return self.conversation_id
    
        
 
        
      
