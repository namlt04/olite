from ChatServerQuery import ChatServerQuery
import asyncio
"""
sent : người gửi lời mời kết bạn
pending: người được gửi lời mời kết bạn
friend: đã là bạn bè 
gửi những user tới user2 chọn status theo cột của uesr còn lại 
trong 1 mối quan hệ: ví dụ user2 và user3
nếu ta là user2, thì gửi trạng thái của user3 đến localdatabase của chúng ta
như vậy : nếu user3 : sent : đang gửi 1 lời mời kết bạn tới chúng ta chơ chấp nhận
pending : chúng ta đang gửi 1 lời mời kết bạn đến người này
"""
class HandleFriend: 

    def __init__(self, client_queue, clients_ws, cursor, conn, handle_conversation):
        self.client_queue = client_queue
        self.clients_ws = clients_ws
        self.cursor = cursor
        self.conn = conn
        self.handle_conversation = handle_conversation

    async def handle(self, message): 
        handle = message["handle"]
        try: 
            relationship_id = message["relationship_id"]
        except : 
            pass
        if ( handle == "deny"): 
            await self.handle_deny(relationship_id, message)
        elif (handle == "accept"): 
            await self.handle_accept(relationship_id, message)
        elif (handle == "sent"):
            await self.handle_sent(message)
        await self.conn.commit()
    async def handle_deny(self, relationship_id, message):
        """
        message = {
            "category" = "AIO_FRIENDS", 
            "handle" = "deny",
            "relationship_id" = id
           
        }
        """
        # TÌM NGƯỜI BỊ TỪ CHỐI KẾT BẠN
        await self.cursor.execute(ChatServerQuery.FRIEND_RECEIVER_QUERY, ("sent", relationship_id))
        result_tuple = await self.cursor.fetchall()
        receiver = result_tuple[0][0]
        print(f"sai o day {receiver}")
        # XÓA KHỎI DATABASE
        await self.cursor.execute(ChatServerQuery.DENY_REQUEST_QUERY, (relationship_id, ))
        await self.conn.commit()
    

        # GỬI 1 GÓI TIN ĐỂ XÓA ĐI TRONG LOCAL DATABASE ( VIỆC NÀY GIÚP NGƯỜI GỬI CÓ THỂ GỬI TIẾP TIN NHẮN )
        if receiver in self.clients_ws:
            await self.client_queue[self.clients_ws[receiver]].put(message)

    async def handle_accept(self, relationship_id, message):
        
        """
        message = {
            "category" = "AIO_FRIENDS", 
            "handle" = "accept",
            "relationship_id" = id,
            "username" : username
        }
        """
        # TÌM NGƯỜI ĐANG CHỜ CHẤP NHẬN KẾT BẠN
        receiver = message["username"]
        
        # NẾU ĐƯỢC CHẤP NHẬN KẾT BẠN THÌ TẠO 1 THÔNG BÁO, SAU ĐÓ GỬI TỚI receiver
        # GỬI GÓI TIN PHÍA NGƯỜI GỬI KẾT BẠN ĐỂ THÔNG BÁO : ĐƯỢC CHẤP NHẬN KẾT BẠN, VÀ TỰ ĐỘNG TẠO 1 CONVERSATION
        if ( receiver in self.clients_ws ): 
            await self.client_queue[self.clients_ws[receiver]].put(message)
        # content = f"Da chap nhan loi moi ket ban cua ban"
        await self.cursor.execute(ChatServerQuery.ACCEPT_REQUEST_QUERY, (relationship_id, )) # CẬP NHẬT TRẠNG THÁI TRONG DATABASE
        await self.cursor.execute(ChatServerQuery.YM_QUERY, (relationship_id, ))
        result_tuple = await self.cursor.fetchall()
   
        member_tuple = (result_tuple[0][0:2], result_tuple[0][2:4])
       

        #
        await self.handle_conversation.create_conversation("" ,member_tuple)

    async def handle_sent(self, message):
        # ĐƯA VÀO DATABASE ĐỂ LẤY ID, SAU ĐÓ GỬI TỚI CHO NGƯỜI CẦN KẾT BẠN

        # YÊU CẦU KẾT BẠN
        id = await self.handle_to_database(message) # ĐƯA VÀO DATABASE, ĐỂ LẤY ID RA TRƯỚC
        
        # GỬI TỚI CLIENT ( cả người gửi và cả người nhận)
        await self.handle_to_receiver(message, id)

    async def handle_to_receiver(self,message, id):
        receiver = None
        sender = None
        if ( message["user1_status"] == "pending"):
            receiver = message["user1"]
            sender = message["user2"]
        else : 
            receiver = message["user2"]
            sender = message["user1"]
    
        # sender: status: sent, receiver: pending
        await self.sent_to(receiver,sender, id, "sent_reply") # GỬI TỚI NGƯỜI GỬI
        await self.sent_to(sender, receiver, id, "sent") # GỬI TỚI NGƯỜI NHẬN

    async def sent_to(self, username_send, username_receiver , relationship_id, handle): 
       
        await self.cursor.execute(ChatServerQuery.INFO_USER_QUERY, (username_send,))
        information = await self.cursor.fetchone()
        message = {
            "category" : "AIO_FRIENDS",
            "handle": handle,
            "relationship_id": relationship_id,
            "username" : username_send,
            "name" : information[0],
            "birth" : information[1],
        } 
        if username_receiver in self.clients_ws: 
            await self.client_queue[self.clients_ws[username_receiver]].put(message)


    async def handle_to_database(self, message):
        """
        message = {
            "category" = "AIO_FRIENDS", 
            "handle" = "sent",
            "user1" = user1,
            "user2" = uesr2, 
            "user1_status" = user1_status, 
            "user2_status" = user2_status
        } 
        """
        await self.cursor.execute(ChatServerQuery.SEND_REQUEST_QUERY, (message["user1"], message["user2"], message["user1_status"], message["user2_status"])) # XỨ LÍ, ĐƯA VÀO DATABSE GỐC
        return self.cursor.lastrowid
   

    
   

   
  
    