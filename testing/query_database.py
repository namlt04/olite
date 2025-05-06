import sqlite3

# Kết nối đến SQLite
conn = sqlite3.connect("chat_db.db")
cursor = conn.cursor()

# Lấy danh sách tất cả các bảng
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

# Duyệt qua từng bảng và lấy dữ liệu
for table in tables:
    print(f"\n📌 Dữ liệu từ bảng: {table}")
    
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    # Lấy tên cột
    col_names = [desc[0] for desc in cursor.description]
    print(f"{' | '.join(col_names)}")  # In tiêu đề cột
    
    for row in rows:
        print(row)  # In từng dòng dữ liệu

conn.close()
