import hashlib
from io import BytesIO
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import database_user_client_side
from datetime import datetime

# Global variables
placeholder_frame = None
username_entry = None
password_entry = None
avatar_path_entry = None
main_frame_global = None
priority = None
custom_label = None
task_name = None
task_date = None
task_start_date = None
n_p_holder = {}

# Function to maximize window
def maximize_window(event=None):
    root.attributes('-fullscreen', True)

# Function to create a pop-up for sign-up success
def sign_up_success():
    messagebox.showinfo('Sign Up Success', 'Sign Up Success')

def bad_avatar_path():
    messagebox.showinfo('NO IMAGE AT PATH', 'NO IMAGE AT PATH!')

def short_password():
    messagebox.showinfo('NO IMAGE AT PATH', 'PASSWORD LENGTH MUST BE MORE THAN 8 CHARACTERS!')

# Database sign-up function
def sign_up_database():
    username = username_entry.get()
    password = password_entry.get()
    avatar_path = avatar_path_entry.get()

    # Password hashing
    hasher = hashlib.sha256()
    hasher.update(password.encode())
    hashed_password = hasher.hexdigest()

    try:
    # Avatar image processing to binary data to be stored in database
        with open(avatar_path, 'rb') as pre_binary:
            binary = pre_binary.read()
    except FileNotFoundError as e:
        bad_avatar_path()

    if len(password) < 8:
        short_password()
    else:
        database_user_client_side.sign_up(username, hashed_password, binary)

        # Call the sign-up success function to show the pop-up
        sign_up_success()

# Database log-in function
def log_in_database():
    global placeholder_frame, form ,n_p_holder

    username = username_entry.get()
    password = password_entry.get()

    # Password hashing
    hasher = hashlib.sha256()
    hasher.update(password.encode())
    hashed_password = hasher.hexdigest()

    users = database_user_client_side.login_user_query()
    for user in users:
        n = user[1]
        p = user[2]
        n_p_holder[n] = p

    if username in n_p_holder and hashed_password == n_p_holder[username]:
        database_user_client_side.log_in(username, hashed_password)

        # Destroy the placeholder frame
        form.destroy()
        placeholder_frame.destroy()

        # Load user details and avatar image
        user = database_user_client_side.user_array
        binary_avatar = user[3]

        # Convert binary data to image
        image = Image.open(BytesIO(binary_avatar))
        image = image.resize((50, 50))
        avatar_image = ImageTk.PhotoImage(image)

        # Store avatar image in a persistent variable
        root.avatar_image = avatar_image

        # BEGIN main instance display
        main()
    else:
        messagebox.showinfo('Invalid Login', 'Invalid Username or Password')

# Function to create and switch to Sign Up frame
def sign_up():
    global placeholder_frame, username_entry, password_entry, avatar_path_entry

    # Destroy any existing placeholder frame
    if placeholder_frame:
        placeholder_frame.destroy()

    # Create a new frame for Sign Up
    placeholder_frame = Frame(root)
    placeholder_frame.pack(pady=20)

    # Addition of widgets to the Sign Up frame
    username_label = Label(placeholder_frame, borderwidth=0,text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = Entry(placeholder_frame,borderwidth=0, width=30)
    username_entry.grid(row=0, column=1)

    password_label = Label(placeholder_frame,borderwidth=0,text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = Entry(placeholder_frame,borderwidth=0, width=30, show="*")
    password_entry.grid(row=1, column=1)

    avatar_path_label = Label(placeholder_frame,borderwidth=0,text="Avatar Path:")
    avatar_path_label.grid(row=2, column=0)
    avatar_path_entry = Entry(placeholder_frame,borderwidth=0, width=30)
    avatar_path_entry.grid(row=2, column=1)

    submit_button = Button(placeholder_frame, borderwidth=0,text="Sign Up",command=sign_up_database)
    submit_button.grid(row=3, column=1)

# Function to create and switch to Log In frame
def log_in():
    global placeholder_frame, username_entry, password_entry

    # Destroy any existing placeholder frame
    if placeholder_frame:
        placeholder_frame.destroy()

    # Create a new frame for Log In
    placeholder_frame = Frame(root)
    placeholder_frame.pack(pady=20)

    # Add widgets as needed for Log In form
    username_label = Label(placeholder_frame,borderwidth=0, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = Entry(placeholder_frame,borderwidth=0, width=30)
    username_entry.grid(row=0, column=1)

    password_label = Label(placeholder_frame,borderwidth=0, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = Entry(placeholder_frame,borderwidth=0, width=30, show="*")
    password_entry.grid(row=1, column=1)

    submit_button = Button(placeholder_frame,borderwidth=0,text="Log In",command=log_in_database)
    submit_button.grid(row=2, column=1)

def set_priority(priority_var):
    global priority
    priority = priority_var.get()
    print(priority)

def priority_level(child_frame):
    priority_var = StringVar()

    randy = Label(child_frame,text="",fg="orange",bg="orange")
    randy.grid(row=0, column=0)

    randy2 = Label(child_frame,text="",fg="orange",bg="orange")
    randy2.grid(row=1, column=0)

    p_one = Radiobutton(child_frame, text="Priority 1", value= "P1",bg="white", fg="orange",variable=priority_var,command=lambda: set_priority(priority_var))
    p_one.grid(row=2, column=0)

    p_two = Radiobutton(child_frame, text="Priority 2", value= "P2",bg="white", fg="orange",variable=priority_var,command=lambda: set_priority(priority_var))
    p_two.grid(row=2, column=1)

    p_three = Radiobutton(child_frame, text="Priority 3", value= "P3",bg="white", fg="orange",variable=priority_var,command=lambda: set_priority(priority_var))
    p_three.grid(row=2, column=2)

def update_custom_label(custom_var):
    global custom_label
    custom_label = custom_var.get()
    print(custom_label)

#THIS FUNCTION IS FOR DRY:IT TAKE S A PARENT FRAME THAT IS IN GRID FORMAT<PERHAPS A PLACEHOLDER FRAME< AND ENSURES POP UP ABLIITY
def labels(parent_frame):
    child_frame = Frame(parent_frame,bg="orange")
    child_frame.grid(row=0, column=1)

    priority_button = Button(parent_frame,bg="white", fg="orange",text="PRIORITY LEVEL",command=lambda:priority_level(child_frame))
    priority_button.grid(row=0 , column=0)

    custom_var = StringVar()
    Label(parent_frame,fg="black",bg="orange",text="CUSTOM LABEL:").grid(row=0,column=1)
    custom_label_entry = Entry(parent_frame, textvariable=custom_var)
    custom_label_entry.grid(row=0,column=3)

    custom_var.trace_add("write", lambda *args :update_custom_label(custom_var))

# notifications function
def notifications():
    pass

# hide function
def hide():
    pass

def update_task_name(task_name_var):
    global task_name
    task_name = task_name_var.get()
    print(task_name)

def update_date(completion_date_var):
    global task_date
    task_date = completion_date_var.get()
    print(task_date)

def update_start_date(task_start_date_var):
    global task_start_date
    task_start_date = task_start_date_var.get()
    print(task_start_date)

def global_handler():
    global task_name,priority,custom_label,task_date,task_start_date
    print(task_name,priority,custom_label,task_date,task_start_date)
    database_user_client_side.add_task(task_name,priority,custom_label,task_date,task_start_date)

def add():
    global main_frame_global , priority , custom_label , task_name ,task_date ,task_start_date

    #Current page frame
    current_page_frame = Frame(main_frame_global,bg="white")
    current_page_frame.pack(fill="y")

    #Addition area
    add_frame = Frame(current_page_frame,bg="orange")
    add_frame.pack(pady=300)

    #Add task WIDGETS

    frame_1 = Frame(add_frame,bg="orange")
    frame_1.grid(row=0, column=0)

    add_task_label = Label(frame_1, text="Add Task",bg="orange",fg="black")
    add_task_label.grid(row=0, column=0)

    task_name_var = StringVar()
    add_task_entry = Entry(frame_1, textvariable=task_name_var)
    add_task_entry.grid(row=0, column=1)
    task_name_var.trace_add("write",lambda *args :update_task_name(task_name_var))

    add_button = Button(frame_1, text="ADD",bg="orange", fg="orange",command=global_handler)
    add_button.grid(row=0, column=2)


    frame_2= Frame(add_frame,bg="orange")
    frame_2.grid(row=1, column=0)

    frame_3 = Frame(add_frame,bg="orange")
    frame_3.grid(row=2, column=0)

    #Task details
    date_label = Label(frame_3,fg="black",bg="orange",text="COMLETION DATE:")
    date_label.grid(row=0, column=0)

    completion_date_var = StringVar()
    completion_date_entry = Entry(frame_3, textvariable=completion_date_var)
    completion_date_entry.grid(row=0, column=1)
    completion_date_var.trace_add("write",lambda *args :update_date(completion_date_var))

    date_label = Label(frame_3, text="START DATE:",fg="black",bg="orange")
    date_label.grid(row=2, column=0)

    task_start_date_var = StringVar()
    task_start_date_entry = Entry(frame_3, textvariable=task_start_date_var)
    task_start_date_entry.grid(row=2, column=1)
    task_start_date_var.trace_add("write",lambda *args :update_start_date(task_start_date_var))

    Label(frame_3,text="YY/MM/DD format for dates",fg="black",bg="orange").grid(row=3, column=0)

    labels_parent_frame = Frame(frame_2,bg="orange")
    labels_parent_frame.grid(row=1, column=1)
    labels(labels_parent_frame)


def search():
    pass

def inbox():
    pass

def today():
    pass

def upcoming():
    pass

def home():
    pass

def calendar():
    pass

# Function to create the main application interface after login
def main():
    global main_frame_global

    main_frame = Frame(root,background="white")
    main_frame.pack(fill=BOTH, expand=True)

    main_frame_global = main_frame

    # Side bar creation
    side_bar_frame = Frame(main_frame, width=250, bg="orange", borderwidth=2)
    side_bar_frame.pack(expand=False, fill="y", side="left", anchor="nw")

    # User processing
    user = database_user_client_side.user_array
    username = user[1]

    # Retrieve avatar image from root object
    avatar_image = root.avatar_image

    # Widget creation
    user_details_frame = Frame(side_bar_frame,bg="white",borderwidth=2)
    user_details_frame.pack(fill='x', pady=10, padx=10)
    avatar_image_label = Label(user_details_frame, image=avatar_image)
    avatar_image_label.grid(row=0, column=0, padx=5)
    username_label = Label(user_details_frame, bg="white",fg="black",text=username.upper())
    username_label.grid(row=0, column=1, padx=5)

    # Notification image processing
    notification_image_pre = Image.open('./Assets/bell.png').resize((20, 20))
    notification_image = ImageTk.PhotoImage(notification_image_pre)
    root.notification_image = notification_image  # Store in root to persist

    overdue_button = Button(user_details_frame, bg="white",image=notification_image, command=notifications, borderwidth=0, highlightthickness=0)
    overdue_button.grid(row=0, column=2, padx=30)

    # Sidebar image processing
    side_pre = Image.open('./Assets/sidebar.png').resize((20, 20))
    side_bar_image = ImageTk.PhotoImage(side_pre)
    root.side_bar_image = side_bar_image  # Store in root to persist

    side_bar_button = Button(user_details_frame, image=side_bar_image, command=hide, borderwidth=0, highlightthickness=0)
    side_bar_button.grid(row=0, column=3, padx=5)

    add_image_pre = Image.open('./Assets/add.png').resize((20, 20))
    add_image = ImageTk.PhotoImage(add_image_pre)
    root.add_image = add_image  # Store in root to persist

    add_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    add_frame.pack(fill='x', pady=40, padx=10)
    add_button = Button(add_frame, image=add_image, command=add)
    add_button.grid(row=0, column=0, padx=5)
    add_label = Label(add_frame, bg="white",fg="black",text='ADD TASK')
    add_label.grid(row=0, column=1, padx=30)

    search_image_pre = Image.open('./Assets/search.png').resize((20, 20))
    search_image = ImageTk.PhotoImage(search_image_pre)
    root.search_image = search_image  # Store in root to persist

    search_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    search_frame.pack(fill='x', pady=40, padx=10)
    search_button = Button(search_frame, image=search_image, command=search)
    search_button.grid(row=0, column=0, padx=5)
    search_label = Label(search_frame, bg="white",fg="black",text='SEARCH TASK')
    search_label.grid(row=0, column=1, padx=30)

    inbox_image_pre = Image.open('./Assets/inbox.png').resize((20, 20))
    inbox_image = ImageTk.PhotoImage(inbox_image_pre)
    root.inbox_image = inbox_image  # Store in root to persist

    inbox_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    inbox_frame.pack(fill='x', pady=40, padx=10)
    inbox_button = Button(inbox_frame, image=inbox_image, command=inbox)
    inbox_button.grid(row=0, column=0, padx=5)
    inbox_label = Label(inbox_frame, bg="white",fg="black",text='INBOX')
    inbox_label.grid(row=0, column=1, padx=30)

    today_image_pre = Image.open('./Assets/today.png').resize((20, 20))
    today_image = ImageTk.PhotoImage(today_image_pre)
    root.today_image = today_image  # Store in root to persist

    today_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    today_frame.pack(fill='x', pady=40, padx=10)
    today_button = Button(today_frame, image=today_image, command=today)
    today_button.grid(row=0, column=0, padx=5)
    today_label = Label(today_frame, bg="white",fg="black",text='TODAY')
    today_label.grid(row=0, column=1, padx=30)

    upcoming_image_pre = Image.open('./Assets/upcoming.png').resize((20, 20))
    upcoming_image = ImageTk.PhotoImage(upcoming_image_pre)
    root.upcoming_image = upcoming_image  # Store in root to persist

    upcoming_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    upcoming_frame.pack(fill='x', pady=40, padx=10)
    upcoming_button = Button(upcoming_frame, image=upcoming_image, command=upcoming)
    upcoming_button.grid(row=0, column=0, padx=5)
    upcoming_label = Label(upcoming_frame, bg="white",fg="black",text='UPCOMING')
    upcoming_label.grid(row=0, column=1, padx=30)

    home_image_pre = Image.open('./Assets/home.png').resize((20, 20))
    home_image = ImageTk.PhotoImage(home_image_pre)
    root.home_image = home_image  # Store in root to persist

    home_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    home_frame.pack(fill='x', pady=40, padx=10)
    home_button = Button(home_frame, image=home_image, command=home)
    home_button.grid(row=0, column=0, padx=5)
    home_label = Label(home_frame, bg="white",fg="black",text='HOME')
    home_label.grid(row=0, column=1, padx=30)

    calendar_image_pre = Image.open('./Assets/calendar.png').resize((20, 20))
    calendar_image = ImageTk.PhotoImage(calendar_image_pre)
    root.calendar_image = calendar_image  # Store in root to persist

    calendar_frame = Frame(side_bar_frame, bg="white", borderwidth=2)
    calendar_frame.pack(fill='x', pady=40, padx=10)
    calendar_button = Button(calendar_frame, image=calendar_image, command=calendar)
    calendar_button.grid(row=0, column=0, padx=5)
    calendar_label = Label(calendar_frame,fg="black", bg="white",text='CALENDAR')
    calendar_label.grid(row=0, column=1, padx=30)

# Main Tkinter window
root = Tk()
root.title("DO IT")

# Bind window resizing to maximize function
root.bind('<Configure>', maximize_window)

# Frame containing Sign Up and Log In buttons
form = Frame(root,borderwidth=0)
form.pack(pady=200)

sign_up_button_option = Button(form,text="Sign Up", command=sign_up)
sign_up_button_option.grid(row=0, column=0)

log_in_button_option = Button(form,text="Log In", command=log_in)
log_in_button_option.grid(row=0, column=1)

# Start the main event loop
root.mainloop()
