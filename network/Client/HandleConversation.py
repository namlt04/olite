"""
XỬ LÍ TẠO HỘI THOẠI, TIN NHẮN TRONG HỘI THOẠI ĐÓ
"""
class HandleConversation: 
    def __init__(self , packet_queue, me , conn,name, conversation, conversation_name, friend , participant, main_window): 
        
        self.me = me
        self.conversation = conversation
        self.name = name
        self.friend = friend
        self.participant = participant
        self.conversation_name = conversation_name
        self.conn = conn
        self.main_window = main_window
        self.packet_queue = packet_queue
   
    async def handle(self, message): 
        await self.create_conversation(message)
        self.main_window.renew_contact_list(message["conversation_id"])
        
    async def create_conversation(self, message): 
        # KHI CÓ GÓI TIN GỬI TỚI TẠO CONVERSATION, CONVERSATION NÀY CHƯA CÓ TIN NHẮN
        query = "insert into conversations(conversation_id, conversation_name, is_group) values(?,?,?)"
        id, name, ok = message["conversation_id"], message["conversation_name"], message["is_group"]
        await self.conn.execute(query, (id, name, ok))
        self.conversation_name[id] = (name, message["is_group"])
        l = list()
        # conversation_name ở đây chưa có gói tin
        for x in message["member_tuple"]: 
            query = "insert into participants(conversation_id, username) values(?, ?)"
            await self.conn.execute(query, (id, x[0]))
            l.append(x[0])
            if ( x[0] not in self.name): 
                self.name[x[0]] = x[1]
            if ( ok == 0 and x[0] != self.me):
                self.conversation_name[id] = (x[1], ok)
        self.participant[id] = l
        self.conversation[id] = []
        await self.conn.commit()
        self.update_conversation()
    async def delete_conversation(self, conversation_id):
        # xóa lịch sử phiá local, 
        # gửi server
        # xóa tin nhắn ở phía server
        message = {
            "category" : "AIO_CONVERSATION",
            "handle" : "delete_conversation", 
            "username" : self.me,
            "conversation_id" : conversation_id,
        }
        # xử lí local
        await self.packet_queue.put(message)

        delete_query = "delete from messages where conversation_id = ?"
        await self.conn.execute(delete_query, (conversation_id, ))
        await self.conn.commit()
        self.conversation.pop(conversation_id)
        self.update_conversation()

        
    async def leave_conversation(self, conversation_id):
      
        # RỜI KHỎI NHÓM
        # ROI NHOM O LOCAL 
        # GUI MSG ROI NHOM O SERVER
        # SERVER GUI 1 TIN NHAN THONG BAO TOI CAC USER KHAC TRONG NHOM DUOI DANG TIN NHAN
        # CẬP NHẬT CONVERSATION DICT()
        message = {
            "category" : "AIO_CONVERSATION",
            "handle" : "leave_conversation", 
            "username" : self.me,
            "conversation_id" : conversation_id,
        }
    
        await self.packet_queue.put(message)
        # xử lí local
        delete_conversation_query = "delete from conversations where conversation_id = ?"
        await self.conn.execute(delete_conversation_query, (conversation_id,))
        await self.conn.commit()
        self.conversation_name.pop(conversation_id) 
        self.update_conversation()
        


    def update_conversation(self):
        # CẬP NHẬT conversation Ở PHÍA GIAO DIỆN
        self.main_window.update_conversation(self.conversation, self.conversation_name, self.name, self.participant)
    
    # TẠO CONVERSATION