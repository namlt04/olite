import bcrypt
class HandleAccount: 
    def __init__(self, packet_queue,main_window,pem_public, chat_client): 
        # (self , packet_queue, me ,conn,note, main_window
        self.packet_queue = packet_queue
        self.pem_public = pem_public
        self.main_window = main_window
        self.chat_client = chat_client
       


    async def handle(self, message): 
        handle = message["handle"]
        if handle == "sign_in": 
            await self.handle_sign_in(message)
        elif handle == "sign_up" : 
            await self.handle_sign_up(message)
        elif handle == "request_otp": 
            self.handle_request_otp(message)
            # xác thực đúng otp thì sẽ luôn chuyển sang màn hình thay đổi mật khẩu  
        elif handle == "verify_otp":
            self.handle_verify_otp(message)
        
    

    def handle_verify_otp(self, message): 
        result = message["result"]
        if result: 
            self.main_window.show_notification("KHONG THE XAC THUC MA OTP")
         
        else: 
            self.main_window.handle_move(3)


    async def handle_sign_in(self, message): 
        result = message["result"]
        if result: 
            self.main_window.show_notification(result)
            # in ra thông báo là đăng nhập không thành công
        else:  
            await self.chat_client.create_local_database()
            await self.chat_client.request_data()
           
            self.main_window.handle_move(4)

    async def handle_sign_up(self, message): 
        result = message["result"]
        if result: 
            self.main_window.show_notification(result)
            # in ra thông báo là đăng ki không thành công
        else: 
            self.main_window.show_notification("DANG KI THANH CONG")
            self.main_window.finish_create_account()
             

    def handle_request_otp(self, message): 
        result = message["result"]
        # handle = request_otp
        if result:
            self.main_window.show_notification("EMAIL HOAC USERNAME KHONG TON TAI TRONG HE THONG")
        else: # result = None
            self.main_window.handle_username_email_true()
            

    async def sign_in(self, username, password): 
     
        # YÊU CẦU GỬI VỀ SERVER 1 TIN NHẮN ĐỂ XÁC THỰC USERNAME
        data = { "category" : "LOGIN_PROCESS", 
                "handle" : "sign_in",
                "username" : username,
                "password" : password,
                "public_key" : self.pem_public
                }

        self.chat_client.username = username
        self.main_window.me = username
        await self.packet_queue.put(data)
    async def sign_up(self, email, birth, gender, name, username): 
        message = {
            "category" : "LOGIN_PROCESS",
            "handle" : "sign_up",
            "username" : username,
            "email" : email,
            "name" : name,
            "birth" : birth,
            "gender" : gender
        }
   
        self.chat_client.username = username
        self.main_window.me = username
        await self.packet_queue.put(message)
    
    async def request_otp(self, username, email):
        # YÊU CẦU GỬI VỀ SERVER 1 TIN NHẮN ĐÊ BẮT ĐÀU GỬI OTP ĐẾN EMAIL
       
        data = {"category": "LOGIN_PROCESS",
                "handle" : "request_otp",
                "username" : username, 
                "email" : email
            
                }
       
        self.chat_client.username = username
        self.main_window.email = email
        self.main_window.me = username
        await self.packet_queue.put(data)

    
    async def verify_otp(self, username, email, otp, old_password):
    
        # SEND JSON AUTHENTICATION FOR OTP
        data = {"category": "LOGIN_PROCESS",
                "handle" : "verify_otp",
                "username" : username,
                "email" : email,
                "old_password" : old_password,
                "otp": otp
        }
        await self.packet_queue.put(data)
    
    async def change_password(self,username, email, password): 
      
        message = {
            "category" : "LOGIN_PROCESS",
            "handle" : "change_password",
            "username" : username,
            "email" : email,
            "password" : password
        }
        await self.packet_queue.put(message)
