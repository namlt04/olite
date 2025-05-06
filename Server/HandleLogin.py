from ChatServerQuery import ChatServerQuery
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyotp
import bcrypt
class HandleLogin: 

    def __init__(self, client_queue, clients_ws, cursor, conn, clients_authentications):
        self.client_queue = client_queue
        self.clients_ws = clients_ws
        self.cursor = cursor
        self.conn = conn
        self.clients_authentications = clients_authentications


    async def handle(self, message, websocket): 
        handle = message["handle"]
        if ( handle == "sign_in"): 
            await self.handle_sign_in(message["username"], message["password"], message["public_key"], websocket)
        elif (handle == "sign_up"): 
            await self.handle_sign_up(message, websocket)
        elif (handle == "change_password"):
            await self.handle_change_password(message)
        elif handle == "request_otp":
            await self.handle_request_otp(message["username"], message["email"], websocket)
        elif handle == "verify_otp" : 
            await self.handle_verify_otp(message, websocket)
        await self.conn.commit()
    async def handle_sign_in(self, username, password, public_key, websocket):
        query = "select password from users where username = %s"
        await self.cursor.execute(query, (username,))
        message = {
            "category" : "LOGIN_PROCESS", 
            "handle" : "sign_in", 
            "result" : None
        }
        result = await self.cursor.fetchone()

        if result : 
            if ( bcrypt.checkpw( password.encode(), result[0].encode()) ): 
                message["result"] = None
                await self.public_key_replace(public_key, username)

            else: 
                message["result"] = "Wrong password"
        else: 
            message["result"] = "Wrong username"
            
        await self.client_queue[websocket].put(message)
    async def public_key_replace(self, public_key, username):
        query = "select public_key from users where username = %s"
        await self.cursor.execute(query, (username,))
        result = await self.cursor.fetchone()
        if ( result != public_key):
            query = " update users set public_key = %s where username = %s"
            await self.cursor.execute(query, (public_key, username))
            await self.conn.commit()

    async def handle_sign_up(self, message, websocket):
        data = {
                "category" : "LOGIN_PROCESS",
                "handle" : "sign_up",
                "result" : "The account or email has already been used by another account."
        }
        # đã kiểm tra username , email tồn tại hay chưa
        verified = await self.verify_username(message["username"], message["email"])
        if verified : # nếu kết quả không phải none
           pass
        else: 
            data["result"] = None
         
            username = message["username"]
            email = message["email"]
            query = "insert into users(username, name, email, birth, gender) values(%s, %s, %s, %s, %s) "
            await self.cursor.execute(query, (message["username"], message["name"], message["email"], message["birth"], message["gender"]))
            await self.conn.commit()
            await self.client_queue[websocket].put(data)

    async def handle_request_otp(self, username, email, websocket): 
        # CLIENT YÊU CẦU SERVER GỬI OTP
        # NẾU USERNAME, EMAIL TỒN TẠI TRONG HỆ THỐNG THÌ GỬI OTP 
        # NẾU KHÔNG THÌ TRẢ VỀ GIÁ TRỊ FALSE
        data = { 
            "category" : "LOGIN_PROCESS",
            "handle" : "request_otp",
            "result" : None
        }
        verified = await self.verify_username(username, email)
        if verified : # nếu kết quả không phải none
            username, email = verified
            await self.send_otp(username, email, websocket)
        else: 
            data["result"] = "False"
        await self.client_queue[websocket].put(data)
    async def handle_change_password(self, message):

        username = message["username"]
        email = message["email"]
        if not username: 
            query = "select username from users where email = %s"
            await self.cursor.execute(query, (email, ))
            result = await self.cursor.fetchone()
            username = result[0]
        query = "update users set password = %s where username = %s "
        await self.cursor.execute(query, (bcrypt.hashpw(message["password"].encode(), bcrypt.gensalt()).decode(), username))
        await self.conn.commit()
        

    async def send_otp(self, username, email, websocket): 
        self.clients_authentications[username] = pyotp.random_base32() 
        totp = pyotp.TOTP(self.clients_authentications[username],interval=300 )
        otp_send = totp.now()
        sender_email = "namlt04.nb@gmail.com" # email@example.com
        sender_passwd =  "sjki jrza efrb tawq" # app password
        if email:
            receiver = email
        else:
            email_query = "select email from users where username =%s"
            await self.curor.execute(email_query, (username, ))
            receiver = list(self.cursor.fetchall())[0]

        msg = MIMEMultipart()
        msg['From'] = sender_email 
        msg['To'] = receiver 
        msg['Subject'] = 'Xac thuc dang nhap - Internal Chat GUI'
        # BODY CUA EMAIL 
        body =  f"{otp_send}" 
        # DINH KEM NOI DUNG EMAIL DANG PLAINTEXT
        msg.attach(MIMEText(body,'plain'))
        try : 
            server = smtplib.SMTP("smtp.gmail.com", 587)
            # MỞ MÃ HÓA TLS
            server.starttls() 
            server.login(sender_email, sender_passwd)
            # MSG -> STRING
            text = msg.as_string()
            # GUI EMAIL 
            server.sendmail(sender_email, receiver, text)
            server.quit()
            print(f"Gui ma Xac thuc OTP toi {username} thanh cong ")
        except: 
            print("Gui email xac thuc khong thanh cong")


    async def handle_verify_otp(self, message, websocket): 
        otp = message["otp"]
        old_password = message["old_password"]
        username = message["username"]
        email = message["email"]

        if not username : 
            # nếu username = None
            query = "select username from users where email = %s"
            await self.cursor.execute(query, (email, ))
            result = await self.cursor.fetchone()
            username = result[0]

        check = True
        if old_password : 
            # nếu có old_password : tức là đang đổi mật khẩu
            query = "select password from users where username = %s"
            self.cursor.execute(query, (username, ))
            result = self.cursor.fetchone()
            result = result[0]
            if bcrypt.checkpw(old_password.encode(), result.encode()) :
                check = False

        # Xác thực OTP: TRẢ VỀ TRUE, FALSE ĐỂ GỬI LẠI BẢN GHI CHO PHÍA GUI CHO PHÉP ĐĂNG NHẬP
        totp = pyotp.TOTP(self.clients_authentications[username], interval=300) # 300 seconds
        # BỎ TEST NÀY 


        result = "False"
        if (totp.verify(otp) and check):
            result = None
       
        data = {
            "category" : "LOGIN_PROCESS",
            "handle" : "verify_otp",
            "result" : result
        }
        await self.client_queue[websocket].put(data)

    async def verify_username(self, username, email):
        await self.cursor.execute(ChatServerQuery.VERIFY_USER_QUERY, (username,email))
        result = await self.cursor.fetchone()
        if result: 
            return result[0], result[1]
        return None
    
   

   
  
    