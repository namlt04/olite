from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

class SignInPage(QWidget): 
    def __init__(self):
        super().__init__()
        self.createUI()
    def createUI(self): 
     
        self.setObjectName("sign_in_page")
    
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.left = QFrame(self)
        self.left.setFixedWidth(300)
        self.left_layout = QVBoxLayout(self.left)
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(0,0,0,0)

        # self.username_label = QLabel("Username", self)
        self.username_entry = QLineEdit(self)
        self.username_entry.setObjectName("username_entry")
        self.username_entry.setFixedWidth(250)
        self.username_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.username_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.username_entry.setPlaceholderText("Username")

        # self.password_label = QLabel("Password", self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setObjectName("password_entry")
        self.password_entry.setFixedWidth(250)
        self.password_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.password_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.sign_in_button = QPushButton("SIGN IN", self)
        self.sign_in_button.setFixedWidth(250)
        self.sign_in_button.setObjectName("sign_in_button")

        self.forget_label = QLabel("Forget password?", self)
        self.sign_up_button = QPushButton("No account yet? Sign up", self)
        self.sign_up_button.setObjectName("sign_up_button")
        self.sign_up_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sign_up_button.adjustSize()
      

        self.left_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.left_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.left_layout.addItem(self.left_top)
        # self.left_layout.addWidget(self.username_label)
        self.left_layout.addWidget(self.username_entry, alignment=Qt.AlignCenter)
        # self.left_layout.addWidget(self.password_label)
        self.left_layout.addWidget(self.password_entry, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.sign_in_button, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.forget_label,alignment=Qt.AlignCenter)
        
        self.left_layout.addItem(self.left_bottom)

        self.layout.addWidget(self.left)

        self.right = QFrame(self)
        self.right.setObjectName("right")
        self.right_layout = QVBoxLayout(self.right)
        self.right_layout.setSpacing(0)
        self.right_layout.setContentsMargins(0,0,0,0)
        self.welcome_label = QLabel("  Welcome back!", self.right)
        self.welcome_label.setObjectName("welcome_label")
        self.welcome_label.setAlignment(Qt.AlignHCenter)
        self.text = """Welcome back! We are so happy to have you 
here. It's great to see you again. We hope you 
        had a safe enjoyable time away
        """

        self.thank_you_label = QLabel(self.text, self.right)
        self.thank_you_label.setObjectName("thank_you_label")
        self.thank_you_label.setAlignment(Qt.AlignHCenter)
        self.right_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.right_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.right_layout.addItem(self.right_top)
        self.right_layout.addWidget(self.welcome_label)
        self.right_layout.addWidget(self.thank_you_label)
        self.right_layout.addWidget(self.sign_up_button, alignment=Qt.AlignCenter)
        self.right_layout.addItem(self.right_bottom)

        self.layout.addWidget(self.right)

