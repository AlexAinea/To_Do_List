import sqlite3

# # INITIAL DATABASE CONNECTION 
# conn = sqlite3.connect("USERS.db")
# cursor = conn.cursor()

# #USERS TABLE CREATION
# cursor.execute("CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT, PASSWORD TEXT,AVATAR BLOB)")

# conn.commit()
# conn.close()

def sign_up(username, password, avatar):
    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, AVATAR) VALUES (?, ?, ?)", (username, password, avatar))
    conn.commit()
    conn.close()

def log_in(username, password):
    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
    users = cursor.fetchall()

    for user in users:
        name = user[1]
        hashed_password = user[2] 
        avatar = user[3]

        table_name = f"table_{hashed_password}"
        
        # Create the user's task table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                TASKS TEXT,
                ONGOING INTEGER,
                COMPLETED INTEGER,
                DATE_TO_BE_COMPLETED INTEGER,
                REMINDER INTEGER,
                OVERDUE INTEGER,
                LABELS TEXT
            )
        """)

    conn.commit()
    conn.close()
