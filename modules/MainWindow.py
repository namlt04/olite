
from modules import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget, QLabel, QVBoxLayout, QFrame, QFileDialog, QDialogButtonBox, QSpacerItem, QSizePolicy, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QSize, QTimer, QDateTime, QEvent
from PySide6.QtGui import QIcon
from network.Client.ChatClient import ChatClient
from modules.SystemTrayIcon import SystemTrayIcon

from modules.FriendRequest import FriendRequest
from modules.ItemContact import ItemContact
from modules.OneMessage import OneMessage
from modules.Profile import Profile
from datetime import datetime
import asyncio
import qasync
import sys
import os
class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__()
       
        self.setGeometry(100,100,800,600)
        self.setWindowIcon(QIcon("olite.ico"))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.button_event_handle()       
        # XỬ LÍ SỰ KIỆN CÁC NÚT BẤM
        self.state = True
        # KHỞI TẠO CÁC BIẾN
        self.conversation = {} # chứa các tin nhắn
        self.conversation_name = {} # conversation_id : (tên cuộc trò chuyện, is_group)
        self.name = dict() # username : tên của người đó
        self.index = None
        self.me = None
        self.email = None
        self.participant = dict()
        
    
        self.note = dict() # id : { id : (tuple[1], tuple[2])}
        self.friend = dict()

        # KHỞI TẠO XỬ LÍ MẠNG
        self.chatClient = ChatClient(self)
        asyncio.ensure_future(self.chatClient.create_connection())
        self.tray_icon = SystemTrayIcon(self)
        self.show()
    
   

    def button_event_handle(self): 
        self.ui.sign_in_page.sign_in_button.clicked.connect(self.handle_sign_in)
        self.ui.sign_in_page.sign_up_button.clicked.connect(lambda : self.handle_move(1))
        self.ui.sign_up_page.sign_up_button.clicked.connect(self.handle_sign_up)
        self.ui.sign_up_page.back_button.clicked.connect(lambda : self.handle_move(0))
        self.ui.forget_page.back_button.clicked.connect(lambda : self.handle_move(0))
        self.ui.new_password_page.confirm_button.clicked.connect(self.handle_change_password)

        self.ui.create_conversation_button.clicked.connect(self.handle_init)
        self.ui.notification_button.clicked.connect(self.handle_notification)
        self.ui.send_button.clicked.connect(self.handle_send_message)
        self.ui.open_button.clicked.connect(self.handle_open_file)
        self.ui.ok_button.clicked.connect(self.complete_create_conversation)
        self.ui.message_entry.installEventFilter(self)
        self.ui.detail_button.clicked.connect(self.hide_and_show)
        self.ui.search_entry.returnPressed.connect(self.handle_search_entry)
        self.ui.leave_conversation_button.clicked.connect(self.handle_leave_conversation)
        self.ui.delete_conversation_button.clicked.connect(self.handle_delete_log_conversation)
        
        self.ui.sign_out_button.clicked.connect(self.handle_sign_out)
        self.ui.change_password_button.clicked.connect(self.change_password)
        self.ui.scrollArea_1.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.ui.sign_in_page.forget_label.mousePressEvent = self.click_event

    @qasync.asyncSlot()
    async def on_scroll(self, value):
        if value == self.ui.scrollArea_1.verticalScrollBar().minimum():
            old_message_id = self.conversation[self.index][0][0]
            await self.chatClient.request_old_message(self.index, self.me, old_message_id)
    @qasync.asyncSlot()
    async def handle_sign_up(self): 
        username = self.ui.sign_up_page.username_entry.text()
        name = self.ui.sign_up_page.fullname_entry.text()
        email = self.ui.sign_up_page.email_entry.text()
        birthday = self.ui.sign_up_page.birth_entry.date().toString("yy/MM/yyyy")
        gender = "male" if self.ui.sign_up_page.male.isChecked() else "female"
        await self.chatClient.handle_account.sign_up(email, birthday, gender, name, username)
       
   
    
    def click_event(self, event):
        self.forget_password()
    @qasync.asyncSlot()
    async def handle_recieve_otp(self): 
        otp = self.ui.fp_otp_entry.text()
        await self.chatClient.verify_otp(otp)


    @qasync.asyncSlot()
    async def handle_change_password(self): 
        password = self.ui.new_password_page.password_entry.text()
        re_password = self.ui.new_password_page.re_password_entry.text()
        if (password == re_password and len(password) >= 6):
            await self.chatClient.handle_account.change_password(self.me, self.email, password)
            for i in range(3, -1, -1): 
                await asyncio.sleep(1)
                self.show_notification(f"QUAY TRO VE DANG NHAP SAU {i}s")
            self.ui.main_stacked.setCurrentIndex(0)
            # doi thanh thanh cong se chuyen thanh doi vai giay roi tro ve tin man hinh dang nhap
        else:
            if ( password != re_password): 
                self.show_notification("MAT KHAU LAP LAI KHONG KHOP")
            else: 
               
                self.show_notification("MAT KHAU PHAI CO TOI THIEU 6 KI TU")
        
    @qasync.asyncSlot()
    async def handle_leave_conversation(self):
        await self.chatClient.handle_conversation.leave_conversation(self.index)
        self.handle_delete_log_conversation()
        
    @qasync.asyncSlot()
    async def handle_delete_log_conversation(self):
        self.clear_layout(self.ui.verticalLayout_6)
        await self.chatClient.handle_conversation.delete_conversation(self.index)
        # XÓA ĐI WIDGET 
        for i in reversed(range(self.ui.verticalLayout_31.count())):
            widget = self.ui.verticalLayout_31.itemAt(i).widget()
            if ( widget and widget.get_index() == self.index ): 
                widget.deleteLater()
                break
        self.ui.chat_frame_right.hide()
        self.index = None 
      
    def handle_notification(self): 
        index = 0 if self.ui.extension_stacked.currentIndex() == 3 else 3
        self.ui.extension_stacked.setCurrentIndex(index)
    def handle_close_search(self): 
        self.ui.extension_stacked.setCurrentIndex(0)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def hide_and_show(self):
        if ( self.conversation_name[self.index][1] == 0):
            self.ui.leave_conversation_button.hide()
        if self.ui.chat_frame_right.isVisible(): 
            self.ui.chat_frame_right.hide()
        else: 
            self.ui.chat_frame_right.show()
    def slide_chat_stack(self): 
        index = self.ui.chat_stacked.currentIndex() 
        self.ui.chat_stacked.setCurrentIndex(0 if index == 1 else 1)
        path_icon_home = "icons/home.png"
        path_icon_chat = "icons/message.png"
        if ( index == 0):
            self.ui.slide_button.setIcon(QIcon(path_icon_home))
        else:
            self.ui.slide_button.setIcon(QIcon(path_icon_chat))
    def eventFilter(self, obj, event): 
        if ( obj == self.ui.message_entry and event.type() == QEvent.KeyPress):
            if event.key() == Qt.Key_Return and not (event.modifiers() & Qt.ShiftModifier): 
                self.handle_send_message()
                return True
        return super().eventFilter(obj, event)
    def handle_search_entry(self): 
        if self.state : 
            self.handle_search()
        else: 
            self.handle_create_conversation()
    @qasync.asyncSlot()
    async def handle_search(self): 
        text = self.ui.search_entry.text()
        if text: 
            await self.chatClient.send_to_search(text, "search")
            self.ui.search_entry.clear()
    def handle_result_search(self, result):

        self.clear_layout(self.ui.extension_stack_2_verticalLayout)

        result_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        profile = Profile(self.me ,  result[0], result,self, "search")
        self.ui.extension_stack_2_verticalLayout.addWidget(profile)
        self.close_search_button = QPushButton("<-")
        self.ui.extension_stack_2_verticalLayout.addWidget(self.close_search_button)
        self.close_search_button.clicked.connect(self.handle_close_search)
        self.ui.extension_stack_2_verticalLayout.addItem(result_vertical_spacer)
        self.ui.extension_stacked.setCurrentIndex(1)
    @qasync.asyncSlot()
    async def back_to_contact_list(self):
        text = self.ui.search_entry.text()
        # TRƯỜNG HỢP ĐÃ TÌM KIẾM, NHƯNG KHÔNG BẤM NÚT ĐỂ QUAY VỀ, MÀ BẤM NÚT TÌM KIẾM LẦN NỮA
        if text: 
            await self.chatClient.send_to_search(text, "search")
            self.ui.search_entry.clear()
        else: 
            self.clear_layout(self.ui.layout_extension_stack_2)
            self.ui.extension_stacked.setCurrentIndex(0)
          
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @qasync.asyncSlot()
    async def handle_create_conversation(self): 
        text = self.ui.search_entry.text()
        if text : 
            await self.chatClient.send_to_search(text, "create")
            self.ui.search_entry.clear()

    @qasync.asyncSlot()
    async def complete_create_conversation(self):
        name = self.ui.name_conversation_entry.text()
        # ok_button là phần nhập :D
        self.ui.name_conversation_entry.clear()

        l = []
        while self.ui.profile_scrollAreaWidgetContents_verticalLayout.count(): 
            widget = self.ui.profile_scrollAreaWidgetContents_verticalLayout.takeAt(0).widget()
            if (isinstance(widget, QFrame)): 
                information = widget.get_info()
                l.append(information)
        await self.chatClient.create_conversation(tuple(l), name)
        self.ui.extension_stacked.setCurrentIndex(0)
        self.state = True
        self.clear_layout(self.ui.profile_scrollAreaWidgetContents_verticalLayout)
        
    @qasync.asyncSlot()
    async def handle_init(self):
        self.clear_layout(self.ui.profile_scrollAreaWidgetContents_verticalLayout)
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.state = False
        self.ui.profile_scrollAreaWidgetContents_verticalLayout.addItem(vertical_spacer)
        self.ui.extension_stacked.setCurrentIndex(2)
        await self.chatClient.send_to_search(self.me, "create")
        await self.handle_create_conversation()

    # THÊM CLEAR BUTTON NGAY BÊN CẠNH NÚT OK
    def handle_cancel_create_conversation(self): 
        
        self.clear_layout(self.ui.profile_scrollAreaWidgetContents_verticalLayout)
        self.ui.extension_stacked.setCurrentIndex(0)

    def handle_result_add(self, result): 
        profile = Profile(self.me, result[0], result,  self, "create")
        self.ui.profile_scrollAreaWidgetContents_verticalLayout.insertWidget(0, profile)
     # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   
    @qasync.asyncSlot() 
    async def handle_open_file(self): 
     
        # KHÔNG SỬ DỤNG QFileDialog.getOpenFileName VÌ LÀ HÀM ĐỒNG BỘ, CHẶN ĐỨNG UI
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)

        future = asyncio.Future()

        dialog.fileSelected.connect(lambda file_path: future.set_result(file_path))
        dialog.show()
        file_path = await future
        if (file_path): 
            await self.chatClient.put_file_to_queue(self.index, file_path)
    
    @qasync.asyncSlot()
    async def handle_download_file(self, message_id, file_name):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)

        dialog.selectFile(file_name)
        future = asyncio.Future()
        dialog.fileSelected.connect(lambda file_path: future.set_result(file_path))
        dialog.show()
        file_path = await future
        if file_path: 
            await self.chatClient.request_file(file_path, message_id)

    @qasync.asyncSlot()
    async def handle_send_message(self):
        text = self.ui.message_entry.toPlainText().strip()
        if text :
            await self.chatClient.put_message_to_queue(self.index, text)
            self.ui.message_entry.clear()
        
    @qasync.asyncSlot()
    async def handle_item(self, item): 
        # CLICK VÀO VỊ TRÍ CỦA TỪNG CUỘC TRÒ CHUYỆN
        conversation_id = item.get_index()
        if self.index != conversation_id:
            self.index = conversation_id
            # cập nhật thông tin
            self.ui.name_conversation_label.setText(self.conversation_name[conversation_id][0])

            if self.ui.chat_frame_right.isVisible(): 
                self.ui.chat_frame_right.hide()

            #
            status = "No new message yet."
            value = self.conversation[conversation_id]
            if value: 
                status = value[-1][-3]
            item.update_status(status)
            
            self.update_participant()
            await self.chatClient.update_status_message(conversation_id)
            self.create_conversation_log()
    
    def update_participant(self): 
        # participant_widget_layout chứa thông tin
        self.clear_layout(self.ui.participant_widget_verticalLayout)
        self.participant_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        for x in self.participant[self.index]:
                self.label_person = QLabel(f"@{x}\n{self.name[x]}")
                self.ui.participant_widget_verticalLayout.addWidget(self.label_person)
        
        self.ui.participant_widget_verticalLayout.addItem(self.participant_verticalSpacer)
  
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def clear_layout(self, layout):
        # XÓA ĐI TẤT CẢ TIN NHẮN PHẦN CHAT, KHI CHUYỂN SANG 1 CUỘC TRÒ CHUYỆN KHÁC 
        while layout.count(): 
            widget = layout.takeAt(0).widget()
            if widget : 
                widget.deleteLater()

        if layout == self.ui.verticalLayout_31:
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)
   
   
    def create_conversation_log(self): 
        # KHI CHUYỂN SANG 1 CUỘC TRÒ CHUYỆN KHÁC, PHẢI XÓA TOÀN BỘ CUỘC TRÒ CHUYỆN CŨ ( CHỈ XÓA TRÊN UI)
        # (5, 'NV005', 1, 'Tôi vừa hoàn thành báo cáo.', '2024-02-27 08:20:00', 1, 0)
        # ĐẢM BẢO MỌI TIN NHẮN ĐỂU CÓ NỘI DUNG: 
        # NẾU LÀ TIN NHẮN THƯỜNG : CHỨA NỘI DUNG 
        # NẾU LÀ TIN NHẮN FILE : CHỨA TÊN FILE 
        self.ui.chat_frame_left.show()
        self.clear_layout(self.ui.verticalLayout_6)
        verticalSpacer_temp = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.ui.verticalLayout_6.addItem(verticalSpacer_temp)
        for message in self.conversation[self.index]: 
            one_message = OneMessage(message, self.me, self.name,  self)
            self.ui.verticalLayout_6.addWidget(one_message)
        # ĐẶT SCROLL BAR LUÔN Ở VỊ TRÍ TIN NHẮN MỚI NHẤT
        QApplication.processEvents()
        QTimer.singleShot(0, lambda: self.ui.scrollArea_1.verticalScrollBar().setValue(self.ui.scrollArea_1.verticalScrollBar().maximum()))

    def update_conversation_log(self, message): 
        # NẾU VẪN ĐANG Ở TRONG CUỘC TRÒ CHUYỆN, KHÔNG CẦN PHẢI VẼ LẠI TOÀN BỘ, CHỈ CẦN VẼ THÊM CÁC TIN NHẮN MỚI ĐẾN 
        # (5, 'NV005', 1, 'Tôi vừa hoàn thành báo cáo.', '2024-02-27 08:20:00', 1, 0)
        if self.index == int(message[2]):
            one_message = OneMessage(message,self.me,self.name ,self)
            self.ui.verticalLayout_6.addWidget(one_message)
        QApplication.processEvents()
        QTimer.singleShot(0, lambda: self.ui.scrollArea_1.verticalScrollBar().setValue(self.ui.scrollArea_1.verticalScrollBar().maximum()))

    def update_old_message(self, message): 
        # NẾU VẪN ĐANG Ở TRONG CUỘC TRÒ CHUYỆN, KHÔNG CẦN PHẢI VẼ LẠI TOÀN BỘ, CHỈ CẦN VẼ THÊM CÁC TIN NHẮN MỚI ĐẾN 
        # (5, 'NV005', 1, 'Tôi vừa hoàn thành báo cáo.', '2024-02-27 08:20:00', 1, 0)

        one_message = OneMessage(message,self.me,self.name ,self)
        self.ui.verticalLayout_6.insertWidget(1, one_message)
        QApplication.processEvents()

    def create_contact_list(self): 
        # contact_database = {"conversation_id" : [(tuple message)]}
        # conversation_name = {"conversation_id" : name}
    
        for key, value in self.conversation.items(): 
            information = None
            if not value : 
                information = "No new messages yet."
            elif value[-1][-2] == 0 : 
                information = "New message"
            else: 
                information = f"{value[-1][-3]}"
            item_contact = ItemContact(key , self.conversation_name[key][0], information, self)
            self.ui.verticalLayout_31.insertWidget(0,item_contact)
         
        
    def update_contact_list(self, conversation_id):
        # TIN NHẮN MỚI TỚI, HỘP THOẠI NÀY NHẢY LÊN ĐẦU TIÊN
        for i in range(self.ui.verticalLayout_31.count()): 
      
            item = self.ui.verticalLayout_31.itemAt(i)
            widget = item.widget()
            
            if ( isinstance(widget, QFrame) and widget.get_index() == conversation_id):
                widget.update_status("New message.") 
                self.ui.verticalLayout_31.takeAt(i)
                widget.setParent(None)
                self.ui.verticalLayout_31.insertWidget(0, widget)
                return
                
    def renew_contact_list(self, conversation_id):
        # verticalLayout_31
            information = "No new messages yet."
            item_contact = ItemContact(conversation_id , self.conversation_name[conversation_id][0], information, self)
            self.ui.verticalLayout_31.insertWidget(0, item_contact)
           
    
    def update_status(self, message): 
        conversation_id = message[2]
        self.update_contact_list(conversation_id)
        self.update_conversation_log(message)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @qasync.asyncSlot()
    async def handle_sign_out(self): 
       
        await self.chatClient.close_local_db()
        path = "./chat_db.db"
        if ( os.path.exists(path)): 
            os.remove(path)
        self.clear_layout(self.ui.verticalLayout_31)
        self.handle_move(0)


    @qasync.asyncSlot()
    async def handle_sign_in(self): 
        username = self.ui.sign_in_page.username_entry.text()
        password = self.ui.sign_in_page.password_entry.text()
        await self.chatClient.handle_account.sign_in(username, password)
        self.ui.sign_in_page.username_entry.clear()
        self.ui.sign_in_page.password_entry.clear()
        

    @qasync.asyncSlot()
    async def handle_otp(self): 
        this_otp = self.ui.otp_entry.text()
        await self.chatClient.verify_otp(this_otp)
        self.ui.otp_entry.clear()
       
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ note 

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ LỜI MỜI KẾT BẠN
    def screen_notification(self): 
        for key, value in self.friend.items(): 
            friend_rq = FriendRequest(key, value, self)
            self.ui.friend_request_scrollAreaWidgetContents_verticalLayout.addWidget(friend_rq)
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.ui.friend_request_scrollAreaWidgetContents_verticalLayout.addItem(vertical_spacer)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @qasync.asyncSlot()
    async def accept_event(self, relationship_id, item): 
        await self.chatClient.handle_friend.accept_event(relationship_id)
        self.del_event(item)
    @qasync.asyncSlot()
    async def deny_event(self, relationship_id, item): 
        await self.chatClient.handle_friend.deny_event(relationship_id)
        self.del_event(item)
    
    @qasync.asyncSlot()
    async def unfriend_event(self, relationship_id): 
        await self.chatClient.handle_friend.deny_event(relationship_id)
        
    def del_event(self, item):
        item.deleteLater()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ LỜI MỜI KẾT BẠN
    
    def update_note(self, note): 
        self.note = note
    def update_friend(self, friend): 
        self.friend = friend
    def update_conversation(self, conversation, conversation_name, name, participant):
        self.conversation = conversation
        self.conversation_name = conversation_name
        self.name = name
        self.participant = participant
    def closeEvent(self, event):
        event.ignore()
        self.hide()
    
   
    @qasync.asyncSlot()
    async def send_friend_request(self, username):
        await self.chatClient.handle_friend.sent_event(username)
        

    @qasync.asyncSlot()
    async def deny_friend_request(self, relationship_id):
        await self.chatClient.handle_friend.deny_event(relationship_id)
    
    @qasync.asyncSlot()
    async def accept_friend_request(self, relationship_id):
        await self.chatClient.handle_friend.accept_event(relationship_id)
    

    def handle_move(self, index):
        # 0 : màn hình đăng nhập
        # 1 : màn hình đăng kí
        # 2 màn hình quên mật khẩu 
        # 3 màn hình đổi mật khẩu
        # 4 màn hình app chat
        self.ui.main_stacked.setCurrentIndex(index)
    # TẠO TÀI KHOẢN
    @qasync.asyncSlot()
    async def finish_create_account(self):
        self.ui.forget_page.finish_create_account()
        await self.chatClient.handle_account.request_otp(self.me, None)
        self.ui.forget_page.authentication_button.clicked.connect(self.handle_create_account_otp)
        self.handle_move(2)
        
    @qasync.asyncSlot()
    async def handle_create_account_otp(self):
        otp = self.ui.forget_page.otp_entry.text()
        await self.chatClient.handle_account.verify_otp(self.me, None, otp, None)
    
    # QUÊN MẬT KHÂU 
    def forget_password(self):
        self.ui.forget_page.forget_password()
        self.ui.forget_page.authentication_button.clicked.connect(self.handle_verify_username_email)
        self.handle_move(2)

    @qasync.asyncSlot()
    async def handle_verify_username_email(self):
    
        username = None
        email = None
        text = self.ui.forget_page.email_entry.text()
        if "@" in text: 
            email = text
        else: 
            username = text
        self.me = username
        self.email = email
        await self.chatClient.handle_account.request_otp(self.me, self.email) 
        
   
    def handle_username_email_true(self):
        self.ui.forget_page.otp_frame.show()
        self.ui.forget_page.authentication_button.clicked.disconnect()
        self.ui.forget_page.authentication_button.clicked.connect(self.handle_verify_otp)
     
            

    @qasync.asyncSlot()
    async def handle_verify_otp(self): 
        otp = self.ui.forget_page.otp_entry.text()
        await self.chatClient.handle_account.verify_otp(self.me, self.email, otp, None)
        # KHI TRẢ VỀ KẾT QUẢ CỦA VERIFY_OTP, NẾU RESULT = NONE MẶC, NÓ SẼ TỰ ĐỘNG CHUYỂN SANG TRANG ĐỔI MẬT KHẨU
        # NGƯỢC LẠI IN RA MÀN HÌNH TERMINAL LÀ OTP SAI 

    # ĐỔI MẬT KHẨU
    @qasync.asyncSlot()
    async def change_password(self): 
        # YÊU CẦU GỬI OTP TRƯỚC, CHUYỂN SANG MÀN HÌNH XÁC THỰC, XÁC THỰC THÀNH CÔNG CHUYỂN SANG ĐỔI MẬT KHẨU
        await self.chatClient.handle_account.request_otp(self.me, None)
        self.ui.forget_page.change_password()
        self.handle_move(2)
        self.ui.forget_page.authentication_button.clicked.connect(self.change_password_otp)

    @qasync.asyncSlot()
    async def change_password_otp(self): 
        otp = self.ui.forget_page.otp_entry.text()
        old_password = self.ui.forget_page.password_entry.text()
        await self.chatClient.handle_account.verify_otp(self.me, None,otp, old_password)
        # CHUYỂN SANG MÀN HÌNH ĐỔI MẬT KHẨU 
        # KHI TRẢ VỀ KẾT QUẢ CỦA VERIFY_OTP, NẾU RESULT = NONE MẶC, NÓ SẼ TỰ ĐỘNG CHUYỂN SANG TRANG ĐỔI MẬT KHẨU
        # NGƯỢC LẠI IN RA MÀN HÌNH TERMINAL LÀ OTP SAI 

    @qasync.asyncSlot()
    async def show_notification(self, text): 
        self.ui.notification.setText(text)
        self.ui.notification.show()
        for i in range(1): 
            await asyncio.sleep(1)
        self.ui.notification.hide()
            
       

    

    

        
        



    
  



