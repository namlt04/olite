

import json
import random
import datetime
import aiofiles
import aiosqlite
import os
import asyncio
import websockets 
import ssl
import hashlib
import base64

from network.Client.HandleFriend import HandleFriend
from network.Client.HandleConversation import HandleConversation
from network.Client.HandleAccount import HandleAccount
from modules.AppNotification import AppNotification

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


from cryptography.hazmat.primitives import hashes, serialization, padding as sym_padding # sym : đối xứng : aes 
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding # rsa

from cryptography.hazmat.backends import default_backend

CHUNK_SIZE = 64 * 1024
class ChatClient: 
    def __init__(self, main_window): 
        self.host = "wss://127.0.0.1:3101"
        self.packet_queue = asyncio.Queue() # TẠO PACKET QUEUE, ĐỂ XỬ GỬI XỬ LÍ TỪNG TIN NHẮN 1
        self.username = None
        self.conversation =  {}
        self.pubkey = {} # username : public_key để mã hóa  
        self.conn = None
        self.conversation_name = {} # id : name,is_group
        self.friend = dict()

        self.name = dict()
        self.participant = dict()
        self.main_window = main_window
        
        
        
        
       
        
        
     
    async def create_connection(self): 
            await self.handle_local_database()
            self.handle_account = HandleAccount(self.packet_queue, self.main_window, self.pem_public, self)
        # old : BỊ LỖI KHI ĐANG CHỌN NƠI TẢI FILE, VÌ WEBSOCKET VẪN CẦN KẾT NỐI, DO VẬY PHẢI CHO WEBSOCKET CHẠY TRÊN 1 TASK
            ssl_context = ssl._create_unverified_context()
            async with websockets.connect(self.host, ssl=ssl_context) as websocket: 
                receive_task = asyncio.create_task(self.receive_packet(websocket))
                send_task = asyncio.create_task(self.send_packet(websocket))
                await asyncio.gather(receive_task, send_task)
        # fix khi gọi đến create_connection() cho nó chạy riêng trên 1 task

    async def receive_packet(self, websocket): 
        # nhận được thì giải mã
        while True:
            message = await websocket.recv()
            # while (chunk := await websocket.recv()) != b"EOF": 
            #     message += chunk
            if message : 
                message = json.loads(message.decode())
                print(message)
                category = message["category"]
                if ( category == "SEND_FILE"):
                    key = message["key_enc"]
                    key_decryption = self.decryption_rsa(key)
        
                    path_save = message["path_save"]
                    full_cipher = b""
                    while True:
                        chunk = await websocket.recv()
                        if chunk == b"EOF":
                            break
                        full_cipher = full_cipher + chunk
                    # lưu lại file
                    await self.decryption_aes_file(key_decryption, full_cipher, path_save)

                await self.filter_message(message)    
 

    async def send_packet(self, websocket): 
        while True: 
        
            # KÍCH THƯỚC 1 TIN NHẮN THỪA ĐỂ ĐI QUA websocket.recv()
            # SEND_DB, HOẶC SEND_FILE MỚI CÓ KÍCH THƯỚC LƠN, ( CẦN TỚI GÓI TIN SYN )
        
            message = await self.packet_queue.get()
            category = message["category"]

            # for i in range(0, len(data), CHUNK_SIZE): 
            #     await websocket.send(data[i:i + CHUNK_SIZE])
            # await websocket.send(b"EOF")

            
            
            if category == "SEND_FILE": 
                path = message["file_url"]
                key = message["key_enc"]
                conversation_id = message["conversation_id"]
                full_cipher = message["full_cipher"]
                file_id = message["file_id"]
                message.pop("full_cipher")
                message.pop("key_enc")
                message.pop("conversation_id")
                message.pop("file_url")
                
                await self.put_message_file_to_queue(path,conversation_id,file_id, key)
                data = json.dumps(message).encode() 
                await websocket.send(data)

                for i in range(0, len(full_cipher), CHUNK_SIZE):
                    chunk = full_cipher[i:i+CHUNK_SIZE]
                    await websocket.send(chunk)
                await websocket.send(b"EOF")
            else:
                print(message)
                data = json.dumps(message).encode() 
                await websocket.send(data)

                   

    async def create_local_database(self):
        # ĐƯỢC KHỞI TẠO KHI XÁC THỰC OTP THÀNH CÔNG ( TỨC ĐĂNG NHẬP THÀNH CÔNG )
        self.conn = await aiosqlite.connect(self.local_db, check_same_thread=False)
   
        await self.conn.execute("PRAGMA foreign_keys = ON;" ) 

        
        await self.conn.execute("""
        create table if not exists users(
        user_id text primary key,
        relationship_id integer,
        name text,
        birth integer,
        status_relationship text);
        """)
       
        await self.conn.execute("""create table if not exists  conversations( 
                                conversation_id integer primary key, 
                                conversation_name text, 
                                is_group integer);
                              """)
        await self.conn.execute(""" 
        create table if not exists messages( 
        message_id integer primary key, 
        sender text, 
        conversation_id integer, 
        content text,
        key text, 
        time_stamp text, 
        is_read integer,
        has_file integer,
        foreign key (conversation_id) references conversations(conversation_id) on delete cascade
        );
        """)
        await self.conn.execute("""
        create table if not exists participants (
        conversation_id integer,
        username text,
        primary key (conversation_id, username),
        foreign key (conversation_id) references conversations(conversation_id) on delete cascade
        );
        """)
        await self.conn.execute("""
        create table if not exists files (
        file_id text,
        message_id integer, 
        primary key (file_id)
        );
        """)
        
        self.init_handle_variable()
        await self.conn.commit()
        

   

    async def request_file(self, path, message_id): 
        # YÊU CẦU GỬI FILE
        file_id = None
        query = "select file_id from files where message_id = ?"
        this_tuple = ()
        async with self.conn.execute(query, (message_id, )) as cursor: 
           this_tuple = await cursor.fetchall()
        file_id = this_tuple[0][0]
        # REQUEST_FILE: CLICK VÀO 1 TIN NHẮN MÀ ĐÓ LÀ TIN NHẮN CÓ CHỨA FILE
        # GỬI YÊU CẦU VỀ PHÍA SERVER, CLICK VÀO NÓ TỨC LÀ NÓ ĐÃ CÓ KEY VÀ IV 
        # ĐẶT KEY, IV
        message = {
           "category" : "REQUEST_FILE",
           "receiver" : self.username, 
           "file_id" : file_id, 
           "path_save" : path
        }
        # BẰNG CÁCH ĐẶT BIẾN TOÀN CỤC VỀ KEY VÀ IV CHO PHÉP NÓ GIẢI MÃ NGAY 
    
        await self.packet_queue.put(message)
    
    

    async def filter_message(self, message):
       
        category = message["category"]
        if ( category == "LOGIN_PROCESS"):

            await self.handle_account.handle(message) 

        elif (category == "MESSAGE"):
            await self.handle_message(message)
        elif category == "OLD_MESSAGE": 
            await self.handle_old_message(message)
        elif ( category == "INIT_DATA"):
            # KHI NHẬN ĐƯỢC DB, BƯỚC CUỐI TRONG QUÁ TRÌNH KẾT NỐI,
            await self.init_data(message)  
            self.main_window.screen_notification()
            self.main_window.create_contact_list()
           
        elif ( category == "AIO_FRIENDS"): 
            await self.handle_friend.handle(message)
        elif (category == "AIO_CONVERSATION"):
            await self.handle_conversation.handle(message)
        elif (category == "SEARCH"): 
            await self.handle_search(message)
    def init_handle_variable(self): 
     
        self.handle_friend = HandleFriend(self.packet_queue, self.username, self.conn, self.friend,self.main_window)
        self.handle_conversation = HandleConversation(self.packet_queue, self.username, self.conn,self.name,  self.conversation, self.conversation_name, self.friend, self.participant, self.main_window)
       
        self.handle_friend.update_friend()
        self.handle_conversation.update_conversation()
            
    async def create_conversation(self, member_tuple, name): 
        message = {
            "category" : "AIO_CONVERSATION",
            "handle" : "create_conversation",  
            "conversation_name" : name, 
            "member_tuple" : member_tuple
        }
        await self.packet_queue.put(message)
    async def handle_message(self, message): 
        

      
        #  message = {
        #         "category" : "MESSAGE",
        #         "mssg" : (self.message_id, self.username, conversation_id, os.path.basename(path), key_encryption_rsa, str(datetime.datetime.now()), 0, 1),
        #         # sender, conversation_id, receiver, content( ở đây sẽ là tên file), key được mã hóa, time, is_read, has_file
        #         "file" : (file_id, os.path.basename(path), os.path.splitext(path)[1][1:], os.path.getsize(path))
        #         # file_id, file_name, file_extension, file_size
        # }
           

        mssg = message["mssg"]
        if message["file"]: 
            file = message["file"]
            query = "insert into files values (?, ?)"
            await self.conn.execute(query, (file[0], mssg[0]))
            content = mssg[3]
        else: 
            key = self.decryption_rsa(mssg[4])
            content = self.decryption_aes_mesg(key, mssg[3])
        
        tuple_mssg = tuple(mssg[:3] + [content] + mssg[4:])
      


        self.conversation[mssg[2]].append(tuple_mssg)
        
        query = "insert into messages values (?,?,?,?,?,?,?,?);"
        await self.conn.execute(query, tuple_mssg)
        await self.conn.commit()

        self.main_window.update_status(tuple_mssg)
        if ( mssg[1] != self.username): 
            AppNotification("Ban nhan duoc 1 tin nhan moi")










        # if ( message["category"] == "MESSAGE_FILE"): # NẾU LÀ MESSAGE_FILE THÌ THÊM CẢ VÀO BẢNG
        #     query = "insert into files values (?, ?)"
        #     await self.conn.execute(query, (message["file_id"], message["message_id"]))
        #     content = message["content"]
        # else: 
        #     key = self.decryption_rsa(message["key_enc"])
        #     content = self.decryption_aes_mesg(key, message["content"])
        
        # tuple_message = (message["message_id"], message["sender"], message["conversation_id"], content ,message["key_enc"], message["time_stamp"],message["is_read"], message["has_file"])
        #     # THÊM TIN NHẮN VÀO TRONG DBDICT <=> TỰ ĐỘNG CẬP NHẬT contact_dbDict
        # self.conversation[message["conversation_id"]].append(tuple_message)
        
        # query = "insert into messages values (?,?,?,?,?,?,?,?);"
        #     # THÊM TIN NHẮN VÀO TRONG LOCAL DATABASE
        # await self.conn.execute(query, tuple_message)
    
        # await self.conn.commit()
        # self.main_window.update_status(tuple_message)
        # if ( message["sender"] != self.username): 
        #     AppNotification("Ban nhan duoc 1 tin nhan moi")
   
    async def handle_search(self, message):
        if ( message["result"] ):
            if ( message["type"] == "search"):
                self.main_window.handle_result_search(message["result"])
            else:
                self.main_window.handle_result_add(message["result"])
    async def send_to_search(self, text, type): 
        # TRUY VẤN TRONG LOCAL DATABASE TRƯỚC, KHÔNG CÓ THÌ MỚI GỬI ĐI 
        query = "select * from users where user_id = ?"
        async with self.conn.execute(query, (text,)) as cursor:
            result = await cursor.fetchone()
      
        if result:
            if ( type == "create" ): 
                self.main_window.handle_result_add(result)
            else : 
                self.main_window.handle_result_search(result)

        else:
            message = {
                "category" : "SEARCH",
                "content" : text, 
                "sender" : self.username,
                "type" : type
            }
            await self.packet_queue.put(message)        

    
    async def init_data(self, message): 
        # KHỞI TẠO DỮ LIỆU LẦN ĐẦU KẾT NỐI, THỰC HIỆN TẠO CÁC DỮ LIỆU CẦN THIẾT
        query = "insert into users values (?, ?, ?, ?,?);"
        for element in message["users"]:
            user = (element["username"], element["relationship_id"], element["name"], element["birth"],  element["status_relationship"])
            #  u.username, u.name, u.birth, u.status ,ut.relationship_id, ut.status as status_relationship
            await self.conn.execute(query, user)
            if (element["status_relationship"] == "sent"):
                self.friend[element["relationship_id"]] = list(user) # TẠO CÁC THÔNG BÁO YÊU CẦU KẾT BẠN
             
       
        query = "insert into conversations values (?, ?, ?);"
        for element in message["conversations"]:
            await self.conn.execute(query,(element["conversation_id"], element["conversation_name"],element["is_group"])  )
            #KHỞI TẠO CONVERSATION NAME
            self.conversation_name[element["conversation_id"]] = ("" if (element["is_group"] == 0) else element["conversation_name"], element["is_group"])
            self.conversation[element["conversation_id"]] = []

        query = "insert into messages values (?, ?, ?, ?, ?, ?, ?, ?);"
        for element in message["messages"]:
            content = element["content"] 
            if element["has_file"] == 0:
                key = self.decryption_rsa(element["key_enc"])
                content = self.decryption_aes_mesg(key, element["content"])
            one_message = (element["message_id"], element["username"], element["conversation_id"], content, element["key_enc"], element["time_stamp"], element["is_read"], element["has_file"])
            
            await self.conn.execute(query, one_message)
            self.conversation[element["conversation_id"]].append(one_message) 
    

        query = "insert into participants values (?, ?);"
        for element in message["participants"]:
            # YÊU CẦU PHÍA SERVER GỬI CẢ TÊN CỦA TỪNG THÀNH VIÊN NHÓM CHAT 
            await self.conn.execute(query, (element["conversation_id"], element["username"]))
            if ( self.conversation_name[element["conversation_id"]][1] == 0 and self.username != element["username"]): 
                self.conversation_name[element["conversation_id"]] = (element["name"], 0)
            self.name[element["username"]] = element["name"]
            if element["name"] not in self.pubkey: 
                self.pubkey[element["username"]] = element["public_key"]
            # conversation_id : list() has username
            if element["conversation_id"] not in self.participant: 
                self.participant[element["conversation_id"]] = list()
            self.participant[element["conversation_id"]].append(element["username"]) 
            
            

        # THÊM DỮ LIỆU BẢNG files (file_id, message_id)
        query = "insert into files values (?, ?)"
        for element in message["files"]: 
            await self.conn.execute(query, (element["file_id"], element["message_id"]))
        
       

        self.handle_conversation.update_conversation()
        self.handle_friend.update_friend()
     
        await self.conn.commit()
    
        
    
    # XỬ LÍ GÓI TIN NHẬN ĐƯỢC 
    
  
    
    async def request_data(self): 
        # GỬI 1 YÊU CẦU SERVER GỬI DỮ LIỆU CẦN THIẾT CHO USER
        data = { 
            "category" : "REQUEST_DATA",
            "username" : self.username
        }
        await self.packet_queue.put(data)

    
    # handle : check_forget
    # handle : check_signup

    async def init_database_dict(self): 
        
        query = """
             select conversation_id, conversation_name, is_group
             from conversations;
          """
        # TRẢ VỀ CONVERSATION_ID
        async with self.conn.execute(query) as cursor: 
          l = [x for x in await cursor.fetchall()]
        # ĐƯA VÀO LIST
        # for element in l: 
        #     if element[2] == 1: 
        #         self.conversation_name[element[0]] = element[1]
        #     else: 
        #         self.conversation_name[element[0]] = "Private"
        for element in l:
            # TRUY VẤN TIN NHẮN TRONG NHÓM
            queryUser = """
            select * 
            from messages m
            where m.conversation_id = ?
            order by m.time_stamp ;
            """
            async with self.conn.execute(queryUser, (element[0], )) as cursor: 
              self.conversation[element[0]] = [x for x in await cursor.fetchall()]
            # TRẢ VỀ 1 DICT VỚI KEY LÀ ID NHÓM, VALUE LÀ 1 LIST CÁC TIN NHẮN
    async def request_old_message(self, conversation_id, username, old_message_id):
        message = {
            "category" : "OLD_MESSAGE", 
            "conversation_id" : conversation_id, 
            "username" : username,
            "old_message_id" : old_message_id # TÌM THEO  MESSAGE_ID  NHỎ HƠN
        }
        await self.packet_queue.put(message)
    async def handle_old_message(self, message): 
        """
        message = {
            "category" : "MESSAGE", 
            "conversation_id": conversation_id, 
            "list_mssg" : [] or None : 1 chuỗi các message 
            "list_file" : nếu như message này có file
        }
        """
        
        #  message = {
        #         "category" : "MESSAGE",
        #         "mssg" : (self.message_id, self.username, conversation_id, os.path.basename(path), key_encryption_rsa, str(datetime.datetime.now()), 0, 1),
        #         # self.message_id, sender, conversation_id, receiver, content( ở đây sẽ là tên file), key được mã hóa, time, is_read, has_file
        #         "file" : (file_id, os.path.basename(path), os.path.splitext(path)[1][1:], os.path.getsize(path))
        #         # file_id, file_name, file_extension, file_size
        # }

        conversation_id = message["conversation_id"]
        query = "insert into messages values (?,?,?,?,?,?,?,?);"

        for one_message in message["list_mssg"]: 
            if one_message[-1] == 1: 
                content = one_message[3]
            else: 
                key = self.decryption_rsa(one_message[4])
                content = self.decryption_aes_mesg(key, one_message[3])
            # TỪNG TIN NHẮN LƯU DƯỚI DẠNG TUPLE
            tuple_mssg = tuple(one_message[:3] + [content] + one_message[4:])
            await self.conn.execute(query, one_message)
        
            self.conversation[conversation_id].insert(0, tuple_mssg)
            self.main_window.update_old_message(tuple_mssg)
        print(self.conversation[conversation_id])
        for one_file in message["list_file"]: 
            query_file = "insert into files values(?,?)"
            await self.conn.execute(query_file,(one_file[0], one_file[1]))
        
        self.handle_conversation.update_conversation()
        await self.conn.commit() 
    

    
    async def put_file_to_queue(self, conversation_id, path): 
        # ĐƯA CÁC TIN NHẮN VÀO HÀNG ĐỢI, SAU ĐÓ GỬI FILE ĐI
        
        # === MÃ HÓA BẰNG AES ===

        key, full_cipher = await self.encryption_aes_file(path) 
        
        # === TẠO ID CHO FILE === từ full_cipher
        sha256 = hashlib.sha256()
        sha256.update(full_cipher)
        id = sha256.hexdigest() 

        message = {
            "category" : "SEND_FILE",
            "file_id" : id, 
            "file_extension" : os.path.splitext(path)[1][1:],
            "size" : os.path.getsize(path),
            "file_url" : path, 
            "conversation_id" : conversation_id,
            "key_enc" : key,
            "full_cipher" : full_cipher
        }
        await self.packet_queue.put(message)
    async def put_message_file_to_queue(self, path, conversation_id,file_id, key):

        query = "select username from participants where conversation_id = ?; "
        async with self.conn.execute(query, (conversation_id, )) as cursor: 
           l = [row[0] for row in await cursor.fetchall()]
       
        for user in l: 
            key_encryption_rsa = self.encryption_rsa(key, user)
            message = {
                "category" : "MESSAGE",
                "mssg" : (self.username, conversation_id, user, os.path.basename(path), key_encryption_rsa, str(datetime.datetime.now()), 0, 1),
                # sender, conversation_id, receiver, content( ở đây sẽ là tên file), key được mã hóa, time, is_read, has_file
                "file" : (file_id, os.path.basename(path), os.path.splitext(path)[1][1:], os.path.getsize(path))
                # file_id, file_name, file_extension, file_size
            }
           
            await self.packet_queue.put(message)


    async def put_message_to_queue(self, conversation_id, text): 
        # NHẬN THÔNG TIN TỪ ENTRY ( PHẦN NHẬP TIN NHẮN ) ĐỂ TẠO CÁC TIN NHẮN VÀ ĐƯA VÀO HÀNG ĐỢI 

        # THAY ĐỔI RECIVER ( TỚI CÁC THÀNH VIÊN TRONG NHÓM )
        query = """
        select username 
        from participants
        where conversation_id = ?;
        """
        async with self.conn.execute(query, (conversation_id, )) as cursor: 
        # LIST CÁC THÀNH VIÊN TRONG NHÓM
            l = [row[0] for row in await cursor.fetchall()]

        
        # === MÃ HÓA BẰNG AES ===
        key, ciphertext = self.encryption_aes_mesg(text)
        
        for user in l: 
            # === MÃ HÓA KEY ===
            key_encryption_rsa = self.encryption_rsa(key, user)

            message = {
                "category" : "MESSAGE", 
                "mssg" : (self.username, conversation_id, user, ciphertext, key_encryption_rsa, str(datetime.datetime.now()), 0, 0),
                # sender, conversation_id,, receiver, content, key_enc, time_stamp, is_read, has_file
                "file" : None
            }

            await self.packet_queue.put(message)
    
    
    async def update_status_message(self, conversation_id):
        # GỬI TIN NHẮN : CHỨA ID TIN NHẮN CẦN UPDATE TRẠNG THÁI
        query_update = """
        select message_id
        from messages 
        where conversation_id = ? and is_read = 0;
        """
        async with self.conn.execute(query_update, (conversation_id, )) as cursor:
          lId = [x[0] for x in await cursor.fetchall()]
        message = {
            "category" : "UPDATE_IS_READ", 
            "list_message" : lId 
        }
        await self.packet_queue.put(message)
        

        # UPDATE TOÀN BỘ TIN NHẮN CHƯA ĐỌC CỦA CONVERSATION_ID ĐÓ THÀNH ĐÃ ĐỌC 
       
        query_update = """
        update messages
        set is_read = 1
        where conversation_id = ? and is_read = 0;
         """
        await self.conn.execute(query_update, (conversation_id,))
        await self.conn.commit()
   
        
    async def close_local_db(self): 
        if self.conn: 
           await self.conn.close()
    
    async def encryption_aes_file(self, file_path): 

        key = os.urandom(32)
        iv = os.urandom(16)
        async with aiofiles.open(file_path, "rb") as f : 
            file_data = await f.read()
        

        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        full_cipher = iv + ciphertext
        return key, full_cipher
    
    def encryption_aes_mesg(self, text):
    
        key = os.urandom(32)
        iv = os.urandom(16)
    
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(text.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return key, base64.b64encode(iv + ciphertext).decode()


    
    def encryption_rsa(self, key, users):
        public_key = serialization.load_pem_public_key(self.pubkey[users].encode())
        encrypted_aes_key = public_key.encrypt(key, asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm= hashes.SHA256(), label = None))
        return  base64.b64encode(encrypted_aes_key).decode()
    

    def decryption_rsa(self, key_encryption_rsa): 
        # Đọc private key từ file PEM
        with open(self.local_private_key, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(),password=None )

        encrypted_key_bytes = base64.b64decode(key_encryption_rsa)
        
        key = private_key.decrypt(encrypted_key_bytes,asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return key  
    


    def decryption_aes_mesg(self, key, full_cipher):
        full_cipher = base64.b64decode(full_cipher)
        iv = full_cipher[:16]
        ciphertext = full_cipher[16:]
        # === GIẢI MÃ AES ===
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # BỎ PADDING
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
       
        return plaintext.decode()
    
    async def decryption_aes_file(self, key, full_cipher, path_save):
        # === GIẢI MÃ AES ===
       
        iv = full_cipher[:16]
        ciphertext = full_cipher[16:]

        # === GIẢI MÃ AES ===
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # BỎ PADDING
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        # PLAINTEXT
        async with aiofiles.open(path_save, "wb") as f: 
            await f.write(plaintext)
    
    async def handle_local_database(self): 
        app_name = "OLite"
        file_db = "chat_db.db"
        file_private_key = "private_key.pem"

        local_appdata = os.getenv("LOCALAPPDATA")

        local_folder = os.path.join(local_appdata, app_name)

        self.local_db = os.path.join(local_folder, file_db)
        self.local_private_key = os.path.join(local_folder, file_private_key)


        # NẾU CHƯA CÓ FOLDER LƯU TRỮ FOLDER
        if not os.path.exists(local_folder): 
            os.makedirs(local_folder)

        # LUÔN XÓA HOÀN TOÀN LOCAL DB CŨ ( ĐẢM BẢO ĐƯỢC RẰNG, KHI MỚI KHỞI ĐỘNG ỨNG DỤNG, NÓ SẼ LUÔN GỬI 1 DỮ LIỆU LỚN MỚI)
        if os.path.exists(self.local_db):
            os.remove(self.local_db)
        if not os.path.exists(self.local_private_key): 
            private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
            pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
            public_key = private_key.public_key()
            pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

   
            async with aiofiles.open(self.local_private_key, "wb") as f:
                await f.write(pem_private)

            
        async with aiofiles.open(self.local_private_key, "rb") as f:
            current_private = await f.read()

        private_key = serialization.load_pem_private_key(current_private, password= None)
        public_key = private_key.public_key()
        pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        self.pem_public = pem_public.decode()
    

    



        

    
 
   

    

    
       

