
import asyncio
from datetime import datetime
from ChatServerQuery import ChatServerQuery
class HandleConversation: 
    def __init__(self, client_queue, clients_ws, cursor, conn):
        self.client_queue = client_queue
        self.client_ws = clients_ws
        self.cursor = cursor
        self.conn = conn
  
        
    
    async def handle(self, message):
        """
        
        message = {
        "category" = "AIO_CONVERSATION",
        "conversation_name" = name, 
        "member_tuple" = ()
        }
        """
        handle = message["handle"]
        if handle == "delete_conversation": 
            await self.delete_conversation(message)
        elif handle == "leave_conversation":
            await self.leave_conversation(message)
        elif handle == "create_conversation" :
            await self.create_conversation(message["conversation_name"], message["member_tuple"])
    


    async def create_conversation(self, conversation_name, username_tuple):
        # username tuple là tuple chứa nhiều tuple 2 phần tử
        # [0] : username
        # [1] : name
        ok = 0 if len(username_tuple) == 2 else 1
        await self.cursor.execute(ChatServerQuery.C2C_CONVERSATION_QUERY, (conversation_name , ok))
        id = self.cursor.lastrowid
       
        for x in username_tuple: 
            await self.cursor.execute(ChatServerQuery.ADD_MEMEBER_QUERY, (id, x[0]))
            
            message = {
            "category" : "AIO_CONVERSATION",
            "handle" : "create_conversation",
            "conversation_id" : id, 
            "conversation_name" : conversation_name, 
            "is_group" : ok,
            "member_tuple" : username_tuple
            }
            if x[0] in self.client_ws:
                await self.client_queue[self.client_ws[x[0]]].put(message)
        await self.conn.commit()
    async def delete_conversation(self, message): 
        username = message["username"]
        conversation_id = message["conversation_id"]
        delete_conversation_query = "delete from messages where receiver = %s and conversation_id = %s"
        await self.cursor.execute(delete_conversation_query, (username, conversation_id))
        await self.conn.commit()
        
    async def leave_conversation(self, message): 
        username = message["username"]
        conversation_id = message["conversation_id"]
        leave_conversation_query = "delete from participants where username = %s and conversation_id = %s"
        await self.cursor.execute(leave_conversation_query, (username, conversation_id))
        await self.conn.commit()
        message = { 
          "category" : "MESSAGE_CHAT",
          "sender" : None,
          "conversation_id" : conversation_id, 
          "receiver" : None, 
          "content" : f"{username} da roi khoi nhom", 
          "time_stamp" : str(datetime.now()),
          "is_read" : 0,
          "has_file" : 0
          }
        participants_query = "select username from participants where conversation_id = %s and username != %s"
        await self.cursor.execute(participants_query, (conversation_id, username))
        members_tuple = await self.cursor.fetchall()
        for x in members_tuple: 
            if x in self.client_ws : 
                await self.client_queue[self.client_ws[x]].put(message)
