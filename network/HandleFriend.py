
class HandleFriend: 
    def __init__(self, packet_queue, me, conn, friend, main_window): 
        # (self , packet_queue, me ,conn,note, main_window
        self.packet_queue = packet_queue
        self.me = me
        self.conn = conn
        self.friend = friend
        self.main_window = main_window
        


    async def handle(self, message): 
        handle = message["handle"]
        relationship_id = message["relationship_id"]
        if ( handle == "deny"): 
            await self.handle_deny(relationship_id)
        elif (handle == "accept"): 
            await self.handle_accept(relationship_id, message)
        elif (handle == "sent"):
            await self.handle_sent(relationship_id, message)
        elif (handle == "sent_reply"): 
            await self.handle_sent_reply(message)
        await self.conn.commit()
    

    async def handle_sent_reply(self, message):
      
        query = """
        insert into users(user_id, relationship_id, name, birth, status_relationship) values
        (?,?,?,?,?)
        """
        user = (message["username"], message["relationship_id"], message["name"], message["birth"], "pending")
        await self.conn.execute(query, user)
        await self.conn.commit()
        
        self.update_friend()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ PHẦN NHẬN ĐƯỢC GÓI TIN CỦA SERVER
    async def handle_deny(self, relationship_id, message):
        # BỊ TỪ CHỐI KẾT CHẤP NHẬN KẾT BẠN
        # NGƯỜI TỪ CHỐI GỬI handle : deny tới server -> server gửi cho người bị từ chối -> người bị từ chối xóa khỏi local database
        """
        message = {
            "category" :"AIO_FRIENDS", 
            "handle" : "deny",
            "relationship_id" : relationship_id
        }
        """
       
        query = "delete from users where relationship_id = ? "
        await self.conn.excute(query, ( relationship_id ,))
        await self.conn.commit()


        self.update_friend()
    async def handle_sent(self, relationship_id, message):
        # SERVER CẬP NHẬT DATABASE -> CLIENT LƯU VÀO DATABASE -> UPDATE dict
        # NHẬN ĐƯỢC 1 LỜI MỜI KẾT BẠN, THÌ ĐƯA NÓ BẢNG user1 + trạng thái pending
        """
        message = {
            "category" : "AIO_FRIENDS", 
            "handle" : "sent", 
            "relationship_id" : id,
            "sender" : sender,
            "name" : result_tuple[1],
            "birth" : result_tuple[3],
         
        } 
        """ 
        query = "insert into users(username, relationship_id, name, birth, status_relationship) values(?,?, ?,?,?)"
        user = (message["sender"], message["relationship_id"], message["name"], message["birth"], "sent")
        await self.conn.execute(query, user)
        await self.conn.commit() 
        self.friend[relationship_id] = list(user)
        
        self.update_friend()
        # self.update_screen_friend() >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cập nhật lại thông báo lời mời kết bạn, nhảy thông báo lên 


        
    async def handle_accept(self, relationship_id, message):
        # THÔNG BÁO LÀ BẢN THÂN ĐƯỢC CHẤP NHẬN LỜI MỜI TỪ NGƯỜI MÀ BẢN THÂN ĐÃ GỬI LỜI MỚI KẾT BẠN
        """
        message = {
            "category" = "AIO_FRIENDS", 
            "handle" = "accept",
            "relationship_id" = id,
        }
        """
        query = """update users set status_relationship = "friend" where relationship_id = ? """
        await self.conn.execute(query, (relationship_id, ))

        


        self.update_friend()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ PHẦN NHẬN ĐƯỢC GÓI TIN CỦA SERVER


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ PHẦN CỦA USER
    # TỨC LÀ CHẤP NHẬN HOẶC KHÔNG CHẤP NHẬN KẾT BẠN
    async def accept_event(self, relationship_id): 
        print(self.friend)
        # PHÍA SERVER SẼ TRUY VẤN RA ID VÀ CẬP NHẬT
        # PHẦN CẬP NHẬT DATABASE, SAU ĐÓ CẬP NHẬT LẠI UI THÌ THÊM CÁCH PENDING ( ĐỢI KẾT BẠN)
        # CẬP NHẬT TRONG DATABASE
        query = """update users set status_relationship = "friend" where relationship_id = ? """
        await self.conn.execute(query, (relationship_id, ))
        await self.conn.commit()
        # GỬI VỀ PHÍA SERVER
        message = {
            "category" : "AIO_FRIENDS", 
            "handle" : "accept",
            "relationship_id" : relationship_id,
            "username" : self.friend[relationship_id][0]
        }
        await self.packet_queue.put(message)
      
      

        self.update_friend()
        

    async def deny_event(self, relationship_id): 
        # CẬP NHẬT TRÊN DATABASE -> CHUYỂN SERVER, SERVER XÓA TRÊN SERVER -> CHUYỂN CHO CLIENT CÒN LẠI
        print(self.friend)
        query = "delete from users where relationship_id = ?"
        await self.conn.execute(query, (relationship_id, ))
        await self.conn.commit()

        message = {
            "category" :"AIO_FRIENDS", 
            "handle" : "deny",
            "relationship_id" : relationship_id
        }
        await self.packet_queue.put(message)
        
        self.update_friend()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> XỬ LÍ PHẦN CỦA USER


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GỬI LỜI MỜI KẾT BẠN CHO 1 USER


    async def sent_event(self, user1): 
        print(self.friend)
        user2 = self.me
        user1_status = "pending"
        user2_status = "sent"

        if ( user1 > user2) :
            user1, user2 = user2, user1
            user1_status, user2_status = user2_status, user1_status
        message = {
            "category" : "AIO_FRIENDS", 
            "handle" : "sent",
            "user1" : user1,
            "user2" : user2,
            "user1_status" : user1_status, 
            "user2_status" : user2_status
        }
        await self.packet_queue.put(message)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GỬI LỜI MỜI KẾT BẠN CHO 1 USER
    def update_friend(self): 
        self.main_window.update_friend(self.friend)



    
    # a và b 
    # a gửi lời mời kết bạn cho b
    # a soạn 1 gói tin gửi lên server 
    # server nhận được gói tin, gửi cho cả 2
    # a lưu vào local database của mình 
    # b cũng lưu vào local database của mình, và đầy lên màn hình


    # b chấp nhận a
    # b sửa trong local databse của mình thành "friend" 
    # b gửi 1 gói tin thông báo server
    # server sửa dữ liệu trong database
    # server gửi gói tin cho a
    # server gửi luôn thông báo cho a 
    # server tạo hội thoại giữa a và b 
    # server gửi cho a và gửi cho b hội thoại 
    # a nhận được hội thoại, đưa vào local database
    # a cập nhật giao diện
    
    # b từ chối a
    # b xóa trong local database
    # b gửi gói tin tới server
    # server xóa database
    # server gửi tới a
    # a xóa trong local database
    # để làm gì ? ĐỂ a có thể tiếp tục gửi

    # a đã gửi lời mời kết bạn 
    # nhưng không muốn gửi nữa
    # a bấm nút hủy, soạn gói tin hủy gửi tới server
    # server xóa đi
    # server gửi gói tin, xóa luôn local database của b
    # b cập nhật giao diện
    