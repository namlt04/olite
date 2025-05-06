# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledTvlWnp.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QVBoxLayout, QWidget)
from modules.NewPasswordPage import NewPasswordPage
from modules.ForgetPage import ForgetPage
from modules.SignUpPage import SignUpPage
from modules.SignInPage import SignInPage
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # MainWindow.(801, 600)
        MainWindow.setFixedSize(800,600)

        self.stylesheet = QWidget(MainWindow)
        self.stylesheet.setObjectName(u"stylesheet")
        self.stylesheet.setStyleSheet("""
        #extension_stacked{
            background-color: #ffffff;
        }
        #search_entry {
            border: none;
            font-weight : bold;
            background-color: #f1f1f1;
        }
        #list_content{
            background-color: #ffffff;
        }
        #create_conversation_button{ 
            border : none;
        }
        #notification_button{
            border : none;
        }
        #detail_button{
            border: none;
        }
        #sign_in_page #username_entry{
            font-size : 18px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #sign_in_page #password_entry{
            font-size : 18px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #sign_in_page #sign_up_button{
            background-color: #f1f1f1;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #sign_in_page #sign_in_button{
            background-color: #78aaff;
            color : white;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #sign_in_page #welcome_label{
            color: white;
            padding : 0px 0px;
            font-size:30px; 
            font-weight: bold;
        }
        #sign_in_page #thank_you_label{
            color: white;
            padding : 0px 0px;
            font-size: 20px; 
            font-weight: bold;
        }
        #sign_in_page #right{
            background-color : #78aaff;
        }
        #forget_page #email_entry{
            font-size : 12px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #forget_page #password_entry{
            font-size : 18px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #forget_page #otp_entry{
            font-size : 13px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #forget_page #resend_otp_button{
            background-color: #78aaff;
            color : white;
            padding : 10px 10px;
            border-radius : 15px;
        }
        
        #forget_page #authentication_button{
            background-color: #78aaff;
            color : white;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #forget_page #right{
            background-color : #78aaff;
        }
        #forget_page #back_button{
            background-color: #f1f1f1;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #sign_up_page #email_entry{
            font-size : 13px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #sign_up_page #fullname_entry{
            font-size : 13px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #sign_up_page #username_entry{
            font-size : 13px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #sign_up_page #sign_up_button{
            background-color: #78aaff;
            color : white;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #sign_up_page #right{
            background-color : #78aaff;
        }
        #sign_up_page #back_button{
            background-color: #f1f1f1;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #sign_up_page #birth_label{
            font-size: 13px
        }
        #new_password_page #password_entry{
            font-size : 18px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #new_password_page #re_password_entry{
            font-size : 18px;
            padding : 10px 10px;
            border-radius : 15px;
            background-color: #f1f1f1;
        }
        #new_password_page #confirm_button{
            background-color: #78aaff;
            color : white;
            padding : 10px 10px;
            border-radius : 15px;
        }
        #friend_request{
            border: none; 
            border-radius: 10 px; 
            background-color: #ffffff; 
        }
        #friend_request #label_name{
            font-weight:bold;
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
        #item_contact{
            border : solid 1px #f1f1f1;
            background-color: #ffffff;
        }
        #item_contact #name_label{ 
            font-weight: bold;
            font-size: 16px;
        }
        #item_contact #status_label{
            font-size:12px;
            color: gray;
        }
        #detail_button{
            border: none;
        }
        #name_conversation_label{
            font-size: 13px;
            font-weight: bold;    
        }
        #name_conversation_frame{
            border: none;
            background-color: #f1f1f1;
        }
        #send_button{
            font-size: 20px;
            border: none;
        }
        #open_button{
            font-size: 20px;
            border: none;
        }
        #notification{
            font-weight: bold; 
            border: none;
            border-radius: 10px;
            color : #ffffff;
            background-color: #111111;
        }
        #delete_conversation_button{
            border: none;
        }
        #leave_conversation_button{
            border: none;
        }
        #friend_request_scrollAreaWidgetContents{
            background-color : #ffffff;
        }
        #setting_frame{
            border: none;
        }
        #name_conversation_entry{
            border: none; 
        }
        #ok_button{
            border: none;
            background-color: #5A86FA
        }
        

        
                                      
        """)
        self.horizontalLayout = QHBoxLayout(self.stylesheet)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_stacked = QStackedWidget(self.stylesheet)
        self.main_stacked.setObjectName("main_stacked")
        self.main_stacked.setEnabled(True)
        font = QFont()
        font.setBold(True)
        self.main_stacked.setFont(font)
        self.main_stacked.setMouseTracking(False)
        self.main_stacked.setTabletTracking(True)
        self.main_stacked.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.main_stacked.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.main_stacked.setAutoFillBackground(False)
        self.main_stacked.setFrameShape(QFrame.Shape.Box)
        # MÀN HÌNH ĐĂNG NHẬP --------------------------------------------------------------------------------
        # sip = sign_in_page
        self.sign_in_page = SignInPage()
        self.main_stacked.addWidget(self.sign_in_page)
        # ---------------------------------------------------------------------------------------------------
        # MÀN HÌNH ĐĂNG KÍ
        # sup = sign_up_page
        self.sign_up_page = SignUpPage()
        self.main_stacked.addWidget(self.sign_up_page)
        # ---------------------------------------------------------------------------------------------------
        # MÀN HÌNH QUÊN MẬT KHẨU
        # fp = forget_page
        self.forget_page = ForgetPage()
        self.main_stacked.addWidget(self.forget_page)
        # ---------------------------------------------------------------------------------------------------
        # MÀN HÌNH NHẬP MẬT KHẨU MỚI
        # npp = new_password_page
        self.new_password_page = NewPasswordPage()
        self.main_stacked.addWidget(self.new_password_page)
        # ---------------------------------------------------------------------------------------------------
        # MÀN HÌNH CHÍNH

       
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_2 = QHBoxLayout(self.page_3)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.left_frame = QFrame(self.page_3)
        self.left_frame.setObjectName("left_frame")
        self.left_frame.setMinimumSize(QSize(250, 0))
        self.left_frame.setMaximumSize(QSize(250, 16777215))
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.left_frame_verticalLayout = QVBoxLayout(self.left_frame)
        self.left_frame_verticalLayout.setSpacing(0)
        self.left_frame_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.left_frame_verticalLayout.setObjectName(u"verticalLayout")
        self.extension_stacked = QStackedWidget(self.left_frame)
        self.extension_stacked.setObjectName("extension_stacked")


        self.extension_stack_1 = QWidget()
        self.extension_stack_1.setObjectName("extension_stack_1")
        self.extension_stack_1_verticalLayout = QVBoxLayout(self.extension_stack_1)
        self.extension_stack_1_verticalLayout.setSpacing(0)
        self.extension_stack_1_verticalLayout.setObjectName(u"verticalLayout_11")
        self.extension_stack_1_verticalLayout.setContentsMargins(0, 0, 0, 0)
       
        self.list_contact = QScrollArea(self.extension_stack_1)
        self.list_contact.setObjectName("list_contact")
        self.list_contact.setWidgetResizable(True)
        self.list_content = QWidget(self.list_contact)
        self.list_content.setObjectName("list_content")
        self.verticalLayout_31 = QVBoxLayout(self.list_content)
        
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_31.addItem(self.verticalSpacer_3)
        self.list_contact.setWidget(self.list_content)

        # font2 = QFont()
        # font2.setPointSize(40)
        # font2.setKerning(False)
        # self.list_contact.setFont(font2)
        # self.list_contact.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#if QT_CONFIG(tooltip)
        # self.list_contact.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        # self.list_contact.setStatusTip(u"")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        # self.list_contact.setWhatsThis(u"")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        # self.list_contact.setAccessibleName(u"")
#endif // QT_CONFIG(accessibility)
        # self.list_contact.setStyleSheet(u"")
        # self.list_contact.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.list_contact.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.list_contact.setProperty(u"showDropIndicator", True)

        self.extension_stack_1_verticalLayout.addWidget(self.list_contact)

        self.extension_stacked.addWidget(self.extension_stack_1)

        self.extension_stack_2 = QWidget()
        self.extension_stack_2.setObjectName(u"extension_stack_2")
        self.extension_stacked.addWidget(self.extension_stack_2)
        self.extension_stack_2_verticalLayout = QVBoxLayout(self.extension_stack_2)
     
        self.extension_stack_3 = QWidget()
        self.extension_stack_3.setObjectName("extension_stack_3")
        self.extension_stack_3_verticalLayout = QVBoxLayout(self.extension_stack_3)
        self.extension_stack_3_verticalLayout.setSpacing(0)
        self.extension_stack_3_verticalLayout.setContentsMargins(0,0,0,0)

        self.extension_stack_4 = QWidget()
        self.extension_stack_4.setObjectName("extension_stack_4")
        self.extension_stack_4_verticalLayout = QVBoxLayout(self.extension_stack_4)
        self.extension_stack_4_verticalLayout.setObjectName("extension_stack_4_verticalLayout")
        

        self.extension_stacked.addWidget(self.extension_stack_1)
        self.extension_stacked.addWidget(self.extension_stack_2)
        self.extension_stacked.addWidget(self.extension_stack_3)
        self.extension_stacked.addWidget(self.extension_stack_4)

        # FRAME CHỨA PHẦN NHẬP VÀ NÚT LƯU TÊN NHÓM >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.save_frame = QFrame(self.extension_stack_3)
        self.save_frame.setObjectName("save_frame")
        self.save_frame.setFixedHeight(30)
        self.save_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.save_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.save_frame_horizontalLayout = QHBoxLayout(self.save_frame)
        self.save_frame_horizontalLayout.setSpacing(0)
        self.save_frame_horizontalLayout.setObjectName("save_frame_horizontalLayout")
        self.save_frame_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ok_button = QPushButton(self.save_frame)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.setFixedSize(QSize(20,20))
        # self.name_conversation_entry.setIconSize(QSize(17, 17))

        
        self.name_conversation_entry = QLineEdit(self.save_frame)
        self.name_conversation_entry.setObjectName("name_conversation_entry")

        self.save_frame_horizontalLayout.addWidget(self.name_conversation_entry)
        self.save_frame_horizontalLayout.addWidget(self.ok_button)

        
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # scrollArea chứa các profile
        self.profile_scrollArea = QScrollArea(self.extension_stack_3)
        self.profile_scrollArea.setObjectName(u"profile_scrollArea")
        self.profile_scrollArea.setWidgetResizable(True)
        self.profile_scrollAreaWidgetContents = QWidget()
        self.profile_scrollAreaWidgetContents.setObjectName("profile_scrollAreaWidgetContents")
        self.profile_scrollAreaWidgetContents_verticalLayout = QVBoxLayout(self.profile_scrollAreaWidgetContents)
        self.profile_scrollAreaWidgetContents.setGeometry(QRect(0, 0, 224, 506))
        self.profile_scrollArea.setWidget(self.profile_scrollAreaWidgetContents)

        self.extension_stack_3_verticalLayout.addWidget(self.save_frame) # thêm khung tìm lưu đoạn chat
        self.extension_stack_3_verticalLayout.addWidget(self.profile_scrollArea) # thêm khung người đỉnh thêm vào đoạn chat
   
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        # extension_stack_4
        # KHUNG HIỂN THỊ LỜI MỜI KẾT BẠN
        self.friend_request_scrollArea = QScrollArea(self.extension_stack_4)
        self.friend_request_scrollArea.setObjectName("friend_request_scrollArea")
        self.friend_request_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.friend_request_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.friend_request_scrollArea.setWidgetResizable(True)
        self.friend_request_scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.friend_request_scrollAreaWidgetContents = QWidget()
        self.friend_request_scrollAreaWidgetContents.setObjectName("friend_request_scrollAreaWidgetContents")
        self.friend_request_scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.friend_request_scrollAreaWidgetContents_verticalLayout = QVBoxLayout(self.friend_request_scrollAreaWidgetContents)
        self.friend_request_scrollAreaWidgetContents_verticalLayout.setSpacing(0)
        self.friend_request_scrollAreaWidgetContents_verticalLayout.setObjectName("friend_request_scrollAreaWidgetContents_verticalLayout")
        self.friend_request_scrollAreaWidgetContents_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.friend_request_scrollArea.setWidget(self.friend_request_scrollAreaWidgetContents)
        self.extension_stack_4_verticalLayout.addWidget(self.friend_request_scrollArea)

        # SEARCH FRAME
       
        
        self.search_entry = QLineEdit(self.left_frame)
        self.search_entry.setObjectName("search_entry")
        self.search_entry.setFixedHeight(25) 
        self.search_entry.setPlaceholderText("Search...")

        # SETTING_FRAME 
        self.setting_frame = QFrame(self.left_frame)
        self.setting_frame.setObjectName("setting_frame")
        self.setting_frame_layout = QHBoxLayout(self.setting_frame)
        self.setting_frame_layout.setSpacing(0)
        self.setting_frame_layout.setContentsMargins(0,0,0,0)
        self.setting_frame.setFixedHeight(30)


        self.create_conversation_button = QPushButton(self.setting_frame)
        self.create_conversation_button.setObjectName("create_conversation_button")
        self.create_conversation_button.setFixedSize(QSize(30,30))

        self.notification_button = QPushButton("Noti", self.setting_frame)
        self.notification_button.setObjectName("notification_button")
        self.notification_button.setFixedSize(QSize(30,30))

        self.sign_out_button = QPushButton("Exit", self.setting_frame)
        self.sign_out_button.setObjectName("sign_out_button")
        self.sign_out_button.setFixedSize(QSize(30,30))

        self.change_password_button = QPushButton("ChgP", self.setting_frame)
        self.change_password_button.setObjectName("sign_out_button")
        self.change_password_button.setFixedSize(QSize(30,30))
       

        self.setting_frame_layout.addWidget(self.change_password_button)
        self.setting_frame_layout.addWidget(self.create_conversation_button)
        self.setting_frame_layout.addWidget(self.notification_button)
        self.setting_frame_layout.addWidget(self.sign_out_button)
        

        
        # --------------------------------------------------------------------------------------------------
        # self.notification_frame = 
        self.left_frame_verticalLayout.addWidget(self.search_entry)
        self.left_frame_verticalLayout.addWidget(self.extension_stacked)
        self.left_frame_verticalLayout.addWidget(self.setting_frame)

        self.horizontalLayout_2.addWidget(self.left_frame)
        # left_frame, right frame
        # right_frame : chat_frame, noti_frame
        self.right_frame = QFrame(self.page_3)
        self.right_frame.setObjectName("right_frame")
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_right_frame = QVBoxLayout(self.right_frame)
        self.horizontalLayout_right_frame.setSpacing(0)
        self.horizontalLayout_right_frame.setContentsMargins(0,0,0,0)

        

        
        self.chat_frame = QFrame() # CHỨA TIN NHẮN
        self.horizontalLayout_chat_frame = QHBoxLayout(self.chat_frame)
        self.horizontalLayout_right_frame.addWidget(self.chat_frame)
        self.horizontalLayout_chat_frame.setSpacing(0)
        self.horizontalLayout_chat_frame.setContentsMargins(0,0,0,0)


    
        # -------------------------------------------------------------------------------------
        
        # HIỂN THỊ ĐOẠN CHAT
        self.chat_frame_left = QFrame() # HIỂN THỊ TIN NHẮN VÀ KHUNG NHẬP TIN NHẮN
        self.verticalLayout_chat_frame_left = QVBoxLayout(self.chat_frame_left)
        self.verticalLayout_chat_frame_left.setSpacing(0)
        self.verticalLayout_chat_frame_left.setContentsMargins(0,0,0,0)

        self.chat_frame_right = QFrame() # HIỂN THỊ CHI TIẾT CUỘC HỘI THOẠI VÀ CÁC CHỨC NĂNG KHÁC
        self.chat_frame_right.setFixedWidth(200)
        self.verticalLayout_chat_frame_right = QVBoxLayout(self.chat_frame_right)
        self.verticalLayout_chat_frame_right.setSpacing(0)
        self.verticalLayout_chat_frame_right.setContentsMargins(0,0,0,0)
        

        # THANH TÊN CỦA GROUP CHAT
        self.name_conversation_frame = QFrame(self.chat_frame_left)
        self.name_conversation_frame.setObjectName("name_conversation_frame")
        self.name_conversation_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.name_conversation_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.name_conversation_frame.setFixedHeight(25)
        self.horizontalLayout_name_conversation_frame = QHBoxLayout(self.name_conversation_frame)
        self.horizontalLayout_name_conversation_frame.setSpacing(0)
        self.horizontalLayout_name_conversation_frame.setContentsMargins(4, 0, 0, 0)
        self.name_conversation_label = QLabel(self.name_conversation_frame)
        self.name_conversation_label.setObjectName("name_conversation_label")
        self.detail_button = QPushButton(self.name_conversation_frame)
        self.detail_button.setObjectName("detail_button")
        self.detail_button.setMinimumSize(QSize(30, 0))
        self.detail_button.setMaximumSize(QSize(30, 16777215))
       

        self.horizontalLayout_name_conversation_frame.addWidget(self.name_conversation_label)
        self.horizontalLayout_name_conversation_frame.addWidget(self.detail_button)

        self.verticalLayout_chat_frame_left.addWidget(self.name_conversation_frame)
        # PHẦN CHỨA TIN NHẮN
        self.scrollArea_1 = QScrollArea(self.chat_frame_left)
        self.scrollArea_1.setObjectName("scrollArea_1")
        self.scrollArea_1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea_1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollAreaWidgetContents_1 = QWidget()
        self.scrollAreaWidgetContents_1.setObjectName("scrollAreaWidgetContents_1")
        self.scrollAreaWidgetContents_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_1)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)

        # pixmap = QPixmap("background.jpg")  # <--- Đường dẫn ảnh bạn muốn dùng


        # palette = self.scrollAreaWidgetContents_1.palette()
        # palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.scrollAreaWidgetContents_1.size(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)))
        # self.scrollAreaWidgetContents_1.setPalette(palette)
        # self.scrollAreaWidgetContents_1.setAutoFillBackground(True)
        self.verticalLayout_chat_frame_left.addWidget(self.scrollArea_1)
        # PHẦN CHỨA NHẬP, GỬI VÀ MỞ FILE
        self.input_frame = QFrame(self.chat_frame_left)
        self.input_frame.setObjectName("input_frame")
        self.input_frame.setFixedHeight(50)
        self.input_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.input_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_input_frame = QHBoxLayout(self.input_frame)
        self.horizontalLayout_input_frame.setSpacing(0)
        self.horizontalLayout_input_frame.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_input_frame.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_input_frame.setContentsMargins(0, 0, 0, 0)

        self.message_entry = QPlainTextEdit(self.input_frame)
        self.message_entry.setObjectName(u"entry_message")
        # self.message_entry.setMinimumSize(QSize(400, 35))
        # self.message_entry.setMaximumSize(QSize(400, 35))
        self.message_entry.setLineWidth(-1)

        self.send_button = QPushButton(self.input_frame)
        self.send_button.setObjectName("send_button")
        self.send_button.setFixedSize(QSize(50, 50))

        self.open_button = QPushButton(self.input_frame)
        self.open_button.setObjectName("open_button")
        self.open_button.setFixedSize(QSize(50,50))

        self.horizontalLayout_input_frame.addWidget(self.message_entry)
        self.horizontalLayout_input_frame.addWidget(self.open_button)
        self.horizontalLayout_input_frame.addWidget(self.send_button)
     
        self.verticalLayout_chat_frame_left.addWidget(self.input_frame)
        self.chat_frame_left.hide()
        # ----------------------------------------------------------------------------------
        self.horizontalLayout_chat_frame.addWidget(self.chat_frame_left)
        self.horizontalLayout_chat_frame.addWidget(self.chat_frame_right)
        self.horizontalLayout_right_frame.addWidget(self.chat_frame)
        self.chat_frame_right.show()
        self.chat_frame_right.hide()
        # ----------------------------------------------------------------------------------
        # rời nhóm, xóa cuộc trò chuyện, thêm thành viên vào nhóm, hiển thị tên nhóm
      
        self.delete_conversation_button = QPushButton("🗑️  CLEAR CHAT")
        self.delete_conversation_button.setObjectName("delete_conversation_button")

        self.leave_conversation_button = QPushButton("👋  LEAVE GROUP") # nếu nó là nhóm
        self.leave_conversation_button.setObjectName("leave_conversation_button")
        self.verticalLayout_chat_frame_right.addWidget(self.delete_conversation_button)
        self.verticalLayout_chat_frame_right.addWidget(self.leave_conversation_button)

        # rời nhóm, xóa cuộc trò chuyện
        

        
        # hiển thị thông tin thành viên trong nhóm 
        self.participants_label = QLabel("PARTICIPANTS", self.chat_frame_right)
        self.participants_label.setObjectName("participant_label")
        self.verticalLayout_chat_frame_right.addWidget(self.participants_label)

        self.participant_scroll = QScrollArea(self.chat_frame_right)
        self.participant_scroll.setObjectName(u"participant_scroll")
        self.participant_scroll.setWidgetResizable(True)
        self.participant_widget = QWidget()
        self.participant_widget.setObjectName(u"participant_widget")
        self.participant_widget_verticalLayout = QVBoxLayout(self.participant_widget)
        self.participant_scroll.setWidget(self.participant_widget)
        self.verticalLayout_chat_frame_right.addWidget(self.participant_scroll)
        
        
        
        



      

        # THÔNG BÁO
        self.notification = QLabel(MainWindow)
        self.notification.setObjectName("notification")
        self.notification.setGeometry(0, MainWindow.height() - 50, MainWindow.width(), 40)
        self.notification.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.notification.setText("")
        self.notification.hide()




        self.horizontalLayout_2.addWidget(self.right_frame)

        self.main_stacked.addWidget(self.page_3)
        self.horizontalLayout.addWidget(self.main_stacked)
        MainWindow.setCentralWidget(self.stylesheet)

        self.retranslateUi(MainWindow)
        self.main_stacked.setCurrentIndex(0)
        self.extension_stacked.setCurrentIndex(0)
      
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OLite", None))
        self.name_conversation_entry.setText(QCoreApplication.translate("MainWindow","", None))
        self.create_conversation_button.setIcon(QIcon("icons/add.png"))
        # self.exit_button.setIcon(QIcon("icons/logout.png"))
        self.detail_button.setIcon(QIcon("icons/info.png"))
        self.send_button.setText(QCoreApplication.translate("MainWindow", u"🚀", None))
        self.open_button.setText(QCoreApplication.translate("MainWindow", u"📂", None))
    # retranslateUi

