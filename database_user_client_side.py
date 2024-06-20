import sqlite3

# # INITIAL DATABASE CONNECTION 
# conn = sqlite3.connect("USERS.db")
# cursor = conn.cursor()

# #USERS TABLE CREATION
# cursor.execute("CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT, PASSWORD TEXT,AVATAR BLOB)")

# conn.commit()
# conn.close()

def sign_up(username,password,avatar):
    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USERS (USERNAME,PASSWORD,AVATAR) VALUES (?,?,?)",(username,password,avatar))
    conn.commit()
    conn.close()

def log_in(username, password):
    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE USERNAME =? AND PASSWORD =?",(username,password))
    user = cursor.fetchall()
    conn.commit()
    conn.close()
    return user

