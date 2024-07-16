import sqlite3

user_array = None

# INITIAL DATABASE CONNECTION
conn = sqlite3.connect("USERS.db")
cursor = conn.cursor()

# USERS TABLE CREATION
cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT,
        PASSWORD TEXT,
        AVATAR BLOB
    )
""")

conn.commit()
conn.close()

def sign_up(username, password, avatar):
    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, AVATAR) VALUES (?, ?, ?)", (username, password, avatar))
    conn.commit()
    conn.close()

def print_results():
    global user_array
    hashed_password = user_array[2]
    print(hashed_password)

def login_user_query():
    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS")
    users = cursor.fetchall()

    for user in users:
        n = user[1]
        p = user[2]
        print(f"Username: {n}, Password: {p}")

    conn.close()
    return n,p

def log_in(username, password):
    global user_array

    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
    users = cursor.fetchall()

    if users:
        user_array = users[0]
        hashed_password = user_array[2]

        table_name = f"table_{hashed_password}"

        # Create the user's task table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                TASK_NAME TEXT,
                LABELS TEXT,
                PRIORITY_LEVEL TEXT,
                DATE_TO_BE_COMPLETED TEXT,
                START_DATE TEXT
            )
        """)
    
    conn.commit()
    conn.close()

def add_task(task_name, custom_label, priority_level,date_to_be_completed,start_date):
    global user_array

    if user_array is None:
        print("User not logged in")
        return

    hashed_password = user_array[2]
    table_name = f"table_{hashed_password}"

    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {table_name} (TASK_NAME,LABELS,PRIORITY_LEVEL, DATE_TO_BE_COMPLETED,START_DATE ) VALUES (?, ?, ?, ?, ?)",
                   (task_name, custom_label,priority_level,date_to_be_completed,start_date))

    conn.commit()
    conn.close()
