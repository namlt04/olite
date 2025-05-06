from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

class ForgetPage(QWidget): 
    def __init__(self):
        super().__init__()
        self.createUI()
    def createUI(self): 
        self.setObjectName("forget_page")
        
    
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.left = QFrame(self)
        self.left.setFixedWidth(300)
        self.left.setObjectName("left")
        self.left_layout = QVBoxLayout(self.left)
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(0,0,0,0)
       
       

        self.right = QFrame(self)
        self.right.setObjectName("right")
        
       
        self.email_entry = QLineEdit(self.left)
        self.email_entry.setObjectName("email_entry")
        self.email_entry.setFixedWidth(250)
        self.email_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.email_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.email_entry.setPlaceholderText("Type your email or username")

        self.password_entry = QLineEdit(self.left)
        self.password_entry.setObjectName("password_entry")
        self.password_entry.setFixedWidth(250)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Type your old password...")

      
        self.authentication_button = QPushButton("Receiver OTP code", self.left) # sau khi xác thực thì nó sẽ chnyển sang dùng để xác thực otp
        self.authentication_button.setObjectName("authentication_button")
        self.authentication_button.setFixedWidth(250)


        self.otp_label = QLabel("Vui long nhap ma OTP ma ban nhan duoc", self.left)
        self.otp_label.setObjectName("otp_label")
        
        self.otp_frame = QFrame(self.left)
        self.otp_frame_horizontalLayout = QHBoxLayout(self.otp_frame)
        self.otp_frame_horizontalLayout.setSpacing(0)
        self.otp_frame_horizontalLayout.setContentsMargins(0,0,0,0)
        self.otp_frame.setFixedWidth(250)
        self.otp_entry = QLineEdit(self.otp_frame)
        self.otp_entry.setObjectName("otp_entry")
        self.otp_entry.setPlaceholderText("Type otp you received")

        self.resend_otp_button = QPushButton("Resend", self.otp_frame)
        self.resend_otp_button.setObjectName("resend_otp_button")
      
        self.otp_frame_horizontalLayout.addWidget(self.otp_entry)
        self.otp_frame_horizontalLayout.addWidget(self.resend_otp_button)

        self.spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.left_layout.addItem(self.spacer_top)

        self.left_layout.addWidget(self.email_entry, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.otp_label, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.otp_frame, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.password_entry, alignment=Qt.AlignCenter)
       
        
        self.left_layout.addWidget(self.authentication_button, alignment=Qt.AlignCenter)
        self.left_layout.addItem(self.spacer_bottom)
        self.layout.addWidget(self.left)

        self.right_layout = QHBoxLayout(self.right)
        self.right_layout.setContentsMargins(0,0,0,0)
        self.right_layout.setSpacing(0)
        self.back_button = QPushButton("Back to Sign in", self.right)
        self.back_button.setObjectName("back_button")
        self.right_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.right) 

    def finish_create_account(self): 
        self.email_entry.hide()
        self.otp_label.show()
        self.otp_frame.show()
        self.password_entry.hide()
        self.authentication_button.setText("CONFIRM")
    def change_password(self):
        self.email_entry.hide()
        self.otp_label.show()
        self.otp_frame.show()
        self.password_entry.show()
        self.authentication_button.setText("CONFIRM")
    def forget_password(self): 
        self.otp_label.hide()
        self.otp_frame.hide()
        self.password_entry.hide()
        self.authentication_button.setText("CONFIRM")





        