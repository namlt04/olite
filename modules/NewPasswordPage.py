from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

class NewPasswordPage(QWidget): 
    def __init__(self):
        super().__init__()
        self.createUI()
    def createUI(self): 
     
        self.setObjectName("new_password_page")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0,20,0,0)

        
        self.password_entry = QLineEdit(self)
        self.password_entry.setObjectName("password_entry")
        self.password_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.password_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setFixedWidth(250)


    
        self.re_password_entry = QLineEdit(self)
        self.re_password_entry.setObjectName("re_password_entry")
        self.re_password_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.re_password_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.re_password_entry.setPlaceholderText("Password again")
        self.re_password_entry.setEchoMode(QLineEdit.Password)
        self.re_password_entry.setFixedWidth(250)

        self.confirm_button = QPushButton("CONFIRM", self)
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.setFixedWidth(250)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout.addWidget(self.password_entry, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.re_password_entry, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)
        self.layout.addItem(self.spacer)
