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
    print(user_array)

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

    print_results()

def add_task(task_name, custom_label, priority_level):
    global user_array

    if user_array is None:
        print("User not logged in")
        return

    hashed_password = user_array[2]
    table_name = f"table_{hashed_password}"

    conn = sqlite3.connect("USERS.db")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {table_name} (TASKS, ONGOING, COMPLETED, DATE_TO_BE_COMPLETED, REMINDER, OVERDUE, LABELS) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (task_name, 0, 0, priority_level, 0, 0, custom_label))

    conn.commit()
    conn.close()
