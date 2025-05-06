
class ChatServerQuery:
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TABLE NOTE QUERY
    INFO_USER_QUERY = "select u.name, u.birth from users u where u.username = %s"
 
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TABLE FRIENDS QUERY
    FRIEND_RECEIVER_QUERY = """
        select 
            case 
            when user1_status = "%s" then user1 
            else user2 
            end as receiver
        from friends
        where relationship_id = %s;
    """
    YM_QUERY = """
    select f.user1, u1.name, f.user2, u2.name
    from friends f
    join users u1 on f.user1 = u1.username
    join users u2 on f.user2 = u2.username
    where relationship_id = %s 
    """
    ACCEPT_REQUEST_QUERY = """
        update friends 
        set user1_status = "friend", user2_status = "friend"
        where relationship_id = %s
    """
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TABLE CONVERSATIONS QUERY
    ADD_MEMEBER_QUERY = """ insert into participants(conversation_id, username) values (%s, %s); """
    C2C_CONVERSATION_QUERY = "insert into conversations(conversation_name,is_group) values(%s, %s);"
    
    SEND_REQUEST_QUERY = "insert into friends(user1, user2, user1_status, user2_status) values(%s, %s, %s, %s)"
    DENY_REQUEST_QUERY = "delete from friends where relationship_id = %s;"
    INFO_FILE_QUERY = " select * from files join on messages where file_id = %s;"
    INFO_FILE_QUERY = """
    select f.* , m.key_enc
    from files f
    join messages m on f.message_id = m.message_id
    where f.file_id = %s;
    """
    INSERT_FILE_QUERY = """
        insert ignore into files(file_id,  file_url, file_type, file_size, message_id)
        values(%s, %s, %s, %s, %s)
    """
    INSERT_MESSAGE_QUERY = """
      insert into messages(username, conversation_id, receiver, content, key_enc, time_stamp, is_read, has_file)
      values(%s, %s, %s, %s, %s,%s, %s, %s); 
      """ 
    UPDATE_READ_QUERY = """
        update messages 
        set is_read = 1
        where message_id = %s
    """ 
    VERIFY_USER_QUERY = "select username, email from users where username=%s or email = %s ;"
    USER_QUERY  = """
        select u.username, u.name, u.birth
        from users u
    """
    # a gửi kết bạn đến b: a sent, b pending
    # TRUY VẤN BẠN BÈ 
    CONTACT_QUERY = """
        with username_table as(
        select relationship_id, 
            case 
            when user1 = %s then user2
            else user1
            end as other_username, 
            case 
            when user1 = %s then user2_status
            else user1_status
            end as status
        from friends
        where user1 = %s or user2 = %s
        )
        select u.username, u.name, u.birth ,ut.relationship_id, ut.status as status_relationship
        from users u
        join username_table ut on ut.other_username = u.username
        
        
    """
    CONVERSATION_QUERY = """
        select distinct conversations.conversation_id , conversations.conversation_name, conversations.is_group
        from participants
        join conversations on participants.conversation_id = conversations.conversation_id 
        where participants.username =%s;
    """
   
    MESSAGE_TABLE_QUERY = """
        with conversation_attend as ( 
        select distinct conversations.conversation_id , conversations.conversation_name, conversations.is_group
        from participants
        join conversations on participants.conversation_id = conversations.conversation_id 
        where participants.username = %s
        )
        SELECT * FROM (
        SELECT m.message_id, m.username, m.conversation_id, m.content, m.key_enc,  m.time_stamp, m.is_read, m.has_file,
           ROW_NUMBER() OVER (PARTITION BY m.conversation_id ORDER BY m.time_stamp DESC) AS rn
        FROM messages m
        JOIN conversation_attend cu ON m.conversation_id = cu.conversation_id
        where m.receiver = %s
        ) subquery
        WHERE rn <= 20
        ORDER BY time_stamp ASC;
    """
    FILE_QUERY = """ 
      with conversation_attend as (
         select distinct conversations.conversation_id , conversations.conversation_name, conversations.is_group
         from participants
         join conversations on participants.conversation_id = conversations.conversation_id 
         where participants.username = %s
      ), message_table as (
      SELECT * FROM (
      SELECT m.message_id, m.username, m.conversation_id, m.content, m.key_enc, m.time_stamp, m.is_read, m.has_file,
           ROW_NUMBER() OVER (PARTITION BY m.conversation_id ORDER BY m.time_stamp DESC) AS rn
      FROM messages m
      JOIN conversation_attend cu ON m.conversation_id = cu.conversation_id
      where m.receiver = %s
      ) subquery
      WHERE rn <= 20
      ORDER BY time_stamp DESC
      )
      select f.file_id, f.message_id
      from files f
      join message_table m on m.message_id = f.message_id;
      """
 
    PARTICIPANT_QUERY =  """
       with username_table as (
        SELECT p1.* 
        FROM participants p1
        JOIN participants p2 ON p1.conversation_id = p2.conversation_id
        WHERE p2.username = %s
        ) 
        select ut.conversation_id, ut.username, u.name, u.public_key
        from users u
        join username_table ut on ut.username = u.username 
    """