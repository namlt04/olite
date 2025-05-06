import websockets
import asyncio

import json

import sys
import datetime
import ssl
import aiofiles
import os
import aiomysql
from HandleFriend import HandleFriend
from HandleConversation import HandleConversation
from ChatServerQuery import ChatServerQuery
from HandleLogin import HandleLogin
# cursor : 1 đối tượng thực thi câu truy vấn sql

# KHI 1 NHÂN VIÊN ONLINE, TẢI TOÀN BỘ NHỮNG CUỘC TRÒ CHUYỆN CỦA NHÂN VIÊN VÀO TRONG SERVER

CHUNK_SIZE = 64 * 1024
class ChatServer: 
   def __init__(self):
      self.clients_ws = dict() #client_socket[username] = socket
      self.client_queue = dict() #client_queue[websocket] = queue
      self.clients_authentications = dict() # DICT() CHỨA MÃ OTP ĐỂ XÁC THỰC : username : random serect key 32bit
      self.cursor = None # KẾT NỐI VỚI DATABASE
      self.conn = None
      
      self.handle_conversation = None
      self.handle_friend = None   
   
   async def handle(self, websocket, path = None): 
      queue = asyncio.Queue()
      self.client_queue[websocket] = queue
      
      try:
         print("1 ket noi moi ")
         receive_task = asyncio.create_task(self.receive_packet(websocket))
         send_task = asyncio.create_task(self.send_packet(websocket))
         await asyncio.gather(receive_task, send_task)
      except Exception as e : 
         print(f"{e}")
      finally: 
         del self.client_queue[websocket]
   
   
   async def create_my_server(self): 
     await self.sqlConnections()
     ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
     ssl_context.load_cert_chain(certfile="network\\Server\\cert.pem", keyfile="network\\Server\\key.pem")
     server = await websockets.serve(self.handle, "127.0.0.1", 3101, ssl=ssl_context)
     await server.wait_closed()
         
      
   async def receive_packet(self, websocket): 
      while True: 
            message = await websocket.recv()
        
            # while (chunk := await websocket.recv()) != b"EOF": 
            #     message += chunk
           
         
            if message : 
               message = json.loads(message.decode())
               print(message)
               category = message["category"]

               if ( category == "SEND_FILE"): 
                  base_path = os.path.join("D:\\db\\", f"{message["file_id"]}.{message["file_extension"]}")
                  async with aiofiles.open(base_path, "wb") as file: 
                     while (chunk := await websocket.recv()) != b"EOF" : 
                        await file.write(chunk)

               await self.filter_message(message, websocket)    
   
        
           

   async def send_packet(self, websocket): 
      while True: 
         
            message = await self.client_queue[websocket].get()
            category = message["category"]
            path = ""
            if "file_path" in message: 
               path = message.pop("file_path") # XÓA FILE_URL NẾU LÀ SEND_FILE, CHỈ ĐỂ LẠI path_save
            print(message)
            data = json.dumps(message).encode() 
            await websocket.send(data)
            # for i in range(0, len(data), CHUNK_SIZE): 
            #    await websocket.send(data[i:i + CHUNK_SIZE])
            # await websocket.send(b"EOF")
            print("Gui message thanh cong")
            # # TIẾN HÀNH GỬI MESSAGE QUA TRƯỚC
       
            if category == "SEND_FILE": 
               async with aiofiles.open(path, "rb") as file: 
                     while chunk := await file.read(CHUNK_SIZE):
                        await websocket.send(chunk)
                     await websocket.send(b"EOF")
               print("Gui file thanh cong")

  
   async def sqlConnections(self): 
      # kết nối tới database ( MySQL ) lưu trữ thông tin người dùng 
      self.conn = await aiomysql.connect(
         host="localhost", 
         user="root",
         password="0000",
         db="csdl" 
      )
      # sử dụng biến toàn cục
      self.cursor = await self.conn.cursor()
      self.init_variable_func()
   
   def init_variable_func(self):
   
      self.handle_conversation = HandleConversation(self.client_queue, self.clients_ws, self.cursor, self.conn)
      self.handle_friend = HandleFriend(self.client_queue, self.clients_ws, self.cursor,self.conn, self.handle_conversation)
      self.handle_login = HandleLogin(self.client_queue, self.clients_ws, self.cursor, self.conn, self.clients_authentications)

   async def filter_message(self, message, websocket): 
       
      category = message["category"]
    
      if category == "LOGIN_PROCESS": 
            
            await self.handle_login.handle(message, websocket)

      elif category == "MESSAGE": 

         # LƯU VÀO DATABASE, NẾU client ONLINE, THÌ GỬI ĐƯA VÀO HÀNG ĐỢI CỦA client đó 
         # MESSAGE FILE : 1 TIN NHẮN CHỨA THÊM CÁC THÔNG TIN VỀ FILE
         # KHI PHÍA CLIENT GỬI 1 GÓI TIN MESSAGE_FIEL SẼ LUÔN GỬI KÈM FILE 
         await self.handle_message(message)
      elif category == "OLD_MESSAGE": 
         await self.handle_old_message(message)

      elif category == "REQUEST_DATA": 

         await self.init_data(message["username"], websocket)
     
      elif category == "UPDATE_IS_READ":

         await self.updateIsRead(message["list_message"])
      elif category == "REQUEST_FILE":
          
         await self.send_file(message)

      elif category == "AIO_FRIENDS":

         await self.handle_friend.handle(message)

      elif category == "AIO_CONVERSATION":

         await self.handle_conversation.handle(message)
      elif category == "SEARCH": 
         await self.handle_search(message)


   async def handle_old_message(self, message): 
      # XỬ LÍ KHI CÓ YÊU CẦU THÊM TIN NHẮN MỚI CỦA ĐOẠN CHAT
      # GỬI TIẾP TỤC 20 TIN NHẮN MỚI
      # MESSAGE
      query_mssg = """
      SELECT m.message_id, m.username, m.conversation_id, m. content, m.key_enc,m.time_stamp, m.is_read, m.has_file FROM messages m
      where conversation_id = %s AND message_id < %s and receiver = %s
      ORDER BY message_id DESC
      LIMIT 20;
      """
      await self.cursor.execute(query_mssg, (message["conversation_id"], message["old_message_id"], message["username"]))
      result = await self.cursor.fetchall() 
      list_mssg = list()
      for row in result:
         list_mssg.append(row)
      # FILE
      query_file = """
      WITH message_has_file AS (
      SELECT message_id FROM messages
      WHERE conversation_id = %s
      AND message_id < %s
      AND receiver = %s
      ORDER BY message_id DESC
      LIMIT 20
      )
      SELECT f.file_id, mhf.message_id
      FROM message_has_file mhf
      JOIN files f ON f.message_id = mhf.message_id;
      """
      await self.cursor.execute(query_file, (message["conversation_id"], message["old_message_id"], message["username"]))
      result = await self.cursor.fetchall() 
      list_file = []
      for row in result:
         list_file.append(row)
      data = {
         "category": "OLD_MESSAGE",
         "conversation_id" : message["conversation_id"],
         "list_mssg" : list_mssg,
         "list_file" : list_file
      }
      await self.client_queue[self.clients_ws[message["username"]]].put(data)


  
   
   async def handle_search(self, message): 
      # message = {
      #           "category" : "SEARCH",
      #           "content" : text, 
      #           "sender" : self.username
      #       }
      receiver = message["sender"]
      query = "select username, -1 as status_friend,  name, birth, \"add_friend\" as status_relationship from users where username = %s"
      await self.cursor.execute(query, (message["content"]))
      result = await self.cursor.fetchone()
      message = {
                "category" : "SEARCH",
                "result" : result, 
                "type" : message["type"]

      }
      await self.client_queue[self.clients_ws[receiver]].put(message)
   async def send_file(self, message): 
    
      """
       message = { 
          "category" : REQUEST_FILE, 
          "receiver" : username,
   
          "file_id" : id,
          "path_save" : path
       }
      """
      await self.cursor.execute(ChatServerQuery.INFO_FILE_QUERY, (message["file_id"], ))
      this_tuple = await self.cursor.fetchall()
      data = {
         "category" : "SEND_FILE",
         "receiver" : message["receiver"],
         "key_enc" :  this_tuple[0][-1],
         "file_id" : this_tuple[0][0],
         "file_path" : this_tuple[0][2],
         "path_save" : message["path_save"]

      }
      await self.client_queue[self.clients_ws[message["receiver"]]].put(data)
   async def handle_message(self, message):
      # print("OK")
      # ĐƯA TIN NHẮN VÀO BẢNG MESSAGES ĐỂLẤY message_id
      #  message = {
      #         "category" : "MESSAGE",
      #         "mssg" : (message_id, self.username, conversation_id, user, os.path.basename(path), key_encryption_rsa, str(datetime.datetime.now()), 0, 1),
      #         # sender, conversation_id, receiver, content( ở đây sẽ là tên file), key được mã hóa, time, is_read, has_file
      #         "file" : (file_id, os.path.basename(path), os.path.splitext(path)[1][1:], os.path.getsize(path))
      #         # file_id, file_name, file_extension, file_size
      # }


      await self.cursor.execute(ChatServerQuery.INSERT_MESSAGE_QUERY, message["mssg"])
      await self.conn.commit()

      mssg = message["mssg"]
      receiver = mssg[2]
      # THÊM MESSAGE_ID, LOẠI BỎ RECEIVER
      message["mssg"] = [self.cursor.lastrowid] + mssg[:2] + mssg[3:]

      # NẾU NÓ LÀ 1 TIN NHẮN CHỨA FILE, THÌ ĐƯA VÀO NÀY VÀO BẢNG file_attachment
     
      print(message)
      if message["file"] :
         file = message["file"]
         # ĐỊA CHỈ FILE LƯU VÀO, KHI CÓ YÊU CẦU TẢI FILE, NÓ SẼ GỬI YÊU CẦU TỚI HỆ SERVER, SERVER TRUY CẬP TỚI ĐỊA CHỈ NÀY ĐỂ GỬI 
         file_path = os.path.join("D:\\db", f"{file[0]}.{file[2]}")
         # LƯU FILE
         await self.cursor.execute(ChatServerQuery.INSERT_FILE_QUERY, (file[0], file_path, file[2], file[3], mssg[0]))
         await self.conn.commit()
      
      
      if receiver in self.clients_ws:
         await self.client_queue[self.clients_ws[receiver]].put(message)
        

   async def updateIsRead(self, list):
         lTuple = [(id, ) for id in list]
         await self.cursor.executemany(ChatServerQuery.UPDATE_READ_QUERY, lTuple) 
         await self.conn.commit()
   async def init_data(self, username, websocket):
      
      self.clients_ws[username] = websocket
      print(self.clients_ws)
      # SAU KHI XÁC THỰC XONG, HÀM NÀY THỰC HIỆN GỬI 1 (ĐỐNG) THÔNG TIN BAN ĐẦU CHO CLIENT
      data = dict()
      data["category"] = "INIT_DATA"
     
      data["users"] = await self.send_db_support(ChatServerQuery.CONTACT_QUERY, tuple([username]*4))

      # TRUY VẤN TẠO CÁC CUỘC TRÒ CHUYỆN CỦA USER
      data["conversations"] = await self.send_db_support(ChatServerQuery.CONVERSATION_QUERY, tuple([username]))
   
      # TRUY VẤN TỪNG TIN NHẮN TRONG HỘI THOẠI
      data["messages"] = await self.send_db_support(ChatServerQuery.MESSAGE_TABLE_QUERY, tuple([username]*2))

      data["participants"] = await self.send_db_support(ChatServerQuery.PARTICIPANT_QUERY, tuple([username]))
      
      data["files"] = await self.send_db_support(ChatServerQuery.FILE_QUERY, tuple([username]*2))

      await self.client_queue[websocket].put(data)

   async def send_db_support(self, query, param):
      await self.cursor.execute(query, param)
      l = [column[0] for column in self.cursor.description]
      return [dict(zip(l, row)) for row in await self.cursor.fetchall() ]


if __name__ == "__main__":
    server = ChatServer()
    print("Chat Server is running on wss://127.0.0.1:3101")
    asyncio.run(server.create_my_server())
  


