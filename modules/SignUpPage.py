from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QDateEdit, QFrame, QButtonGroup, QRadioButton
from PySide6.QtCore import Qt

class SignUpPage(QWidget): 
    def __init__(self):
        super().__init__()
        self.createUI()
    def createUI(self): 
     
        self.setObjectName("sign_up_page")
        
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.left = QFrame(self)
        self.left.setFixedWidth(300)
        self.right = QFrame(self)
        self.right.setObjectName("right")
    
        self.left_layout = QVBoxLayout(self.left)
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(0,0,0,0)
       
        self.fullname_entry = QLineEdit(self.left)
        self.fullname_entry.setObjectName("fullname_entry")
        self.fullname_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.fullname_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fullname_entry.setPlaceholderText("Type your full name")
        self.fullname_entry.setFixedWidth(250)
      
        self.email_entry = QLineEdit(self.left)
        self.email_entry.setObjectName("email_entry")
        self.email_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.email_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.email_entry.setPlaceholderText("Type your email")
        self.email_entry.setFixedWidth(250)


       
        self.username_entry = QLineEdit(self.left)
        self.username_entry.setObjectName("username_entry")
        self.username_entry.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.username_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.username_entry.setPlaceholderText("Type your username ")
        self.username_entry.setFixedWidth(250)

        self.birth_frame = QFrame(self.left)
        self.birth_frame_layout = QHBoxLayout(self.birth_frame)
        self.birth_label = QLabel("Choose your birth", self.birth_frame)
        self.birth_label.setObjectName("birth_label")
        self.birth_entry = QDateEdit(self.birth_frame)
        self.birth_entry.setObjectName("birth_entry")
        self.birth_entry.setCalendarPopup(True)
        self.birth_entry.setDisplayFormat("dd/MM/yyyy")

        self.birth_frame_layout.addWidget(self.birth_label)
        self.birth_frame_layout.addWidget(self.birth_entry)

        self.gender_frame = QFrame(self)
        self.gender_frame_layout = QHBoxLayout(self.gender_frame)
        self.gender_frame_layout.setSpacing(15)
        self.male = QRadioButton(self.gender_frame)
        self.male_label = QLabel("Male", self.gender_frame)
        self.male_label.adjustSize()
        self.female = QRadioButton(self.gender_frame)
        self.female_label = QLabel("Female", self.gender_frame)
        self.female_label.adjustSize()
        
        self.gender_frame_layout.addWidget(self.male)
        self.gender_frame_layout.addWidget(self.male_label)
        self.gender_frame_layout.addWidget(self.female)
        self.gender_frame_layout.addWidget(self.female_label)

        self.sign_up_button = QPushButton("SIGN UP", self.left)
        self.sign_up_button.setObjectName("sign_up_button")
        self.sign_up_button.setFixedWidth(250)

        self.spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        self.left_layout.addItem(self.spacer_top)
        self.left_layout.addWidget(self.fullname_entry, alignment = Qt.AlignCenter)
        self.left_layout.addWidget(self.username_entry, alignment = Qt.AlignCenter)
        
        self.left_layout.addWidget(self.email_entry, alignment = Qt.AlignCenter)
        self.left_layout.addWidget(self.birth_frame, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.gender_frame,alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.sign_up_button, alignment = Qt.AlignCenter)

        self.left_layout.addItem(self.spacer_bottom)

        self.layout.addWidget(self.left)

        self.right_layout = QHBoxLayout(self.right)
        self.right_layout.setContentsMargins(0,0,0,0)
        self.right_layout.setSpacing(0)
        self.back_button = QPushButton("Back to Sign in", self.right)
        self.back_button.setObjectName("back_button")
        self.right_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.right) 