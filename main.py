from tkinter import *
from tkinter import messagebox
import database_user_client_side 
import hashlib
from io import BytesIO
from PIL import Image, ImageTk

# Global variables
placeholder_frame = None
username_entry = None
password_entry = None
avatar_path_entry = None

# Function to maximize window
def maximize_window(event=None):
    root.attributes('-fullscreen', True)

# Function to create a pop-up for sign-up success
def sign_up_success():
    messagebox.showinfo('Sign Up Success', 'Sign Up Success')

# Database sign-up function
def sign_up_database():
    username = username_entry.get()
    password = password_entry.get()
    avatar_path = avatar_path_entry.get()

    # Password hashing
    hasher = hashlib.sha256()
    hasher.update(password.encode())
    hashed_password = hasher.hexdigest()

    # Avatar image processing to binary data to be stored in database
    with open(avatar_path, 'rb') as pre_binary:
        binary = pre_binary.read()

    database_user_client_side.sign_up(username, hashed_password, binary)

    # Call the sign-up success function to show the pop-up
    sign_up_success()

# Database log-in function
def log_in_database():
    global placeholder_frame, form

    username = username_entry.get()
    password = password_entry.get()

    # Password hashing
    hasher = hashlib.sha256()
    hasher.update(password.encode())
    hashed_password = hasher.hexdigest()

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
    username_label = Label(placeholder_frame, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = Entry(placeholder_frame, width=30)
    username_entry.grid(row=0, column=1)

    password_label = Label(placeholder_frame, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = Entry(placeholder_frame, width=30, show="*")
    password_entry.grid(row=1, column=1)

    avatar_path_label = Label(placeholder_frame, text="Avatar Path:")
    avatar_path_label.grid(row=2, column=0)
    avatar_path_entry = Entry(placeholder_frame, width=30)
    avatar_path_entry.grid(row=2, column=1)

    submit_button = Button(placeholder_frame, text="Sign Up", command=sign_up_database)
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
    username_label = Label(placeholder_frame, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = Entry(placeholder_frame, width=30)
    username_entry.grid(row=0, column=1)

    password_label = Label(placeholder_frame, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = Entry(placeholder_frame, width=30, show="*")
    password_entry.grid(row=1, column=1)

    submit_button = Button(placeholder_frame, text="Log In", command=log_in_database)
    submit_button.grid(row=3, column=1)

# notifications function
def notifications():
    pass

# hide function
def hide():
    pass

def add():
    pass

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
    global root

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    # Side bar creation
    side_bar_frame = Frame(main_frame, width=200, bg="lightgray", relief="sunken", borderwidth=2)
    side_bar_frame.pack(expand=False, fill="y", side="left", anchor="nw")

    # User processing
    user = database_user_client_side.user_array
    username = user[1]
    password = user[2]

    # Retrieve avatar image from root object
    avatar_image = root.avatar_image

    # Widget creation
    user_details_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    user_details_frame.pack(fill='x')
    avatar_image_label = Label(user_details_frame, image=avatar_image)
    avatar_image_label.grid(row=0, column=0)
    username_label = Label(user_details_frame, text=username.upper())
    username_label.grid(row=0, column=1)

    # Notification image processing
    notification_image_pre = Image.open('./Assets/bell.png').resize((20, 20))
    notification_image = ImageTk.PhotoImage(notification_image_pre)
    root.notification_image = notification_image  # Store in root to persist

    overdue_button = Button(user_details_frame, image=notification_image, command=notifications, borderwidth=0, highlightthickness=0)
    overdue_button.grid(row=0, column=2,padx=30)

    # Sidebar image processing
    side_pre = Image.open('./Assets/sidebar.png').resize((20, 20))
    side_bar_image = ImageTk.PhotoImage(side_pre)
    root.side_bar_image = side_bar_image  # Store in root to persist

    side_bar_button = Button(user_details_frame, image=side_bar_image, command=hide, borderwidth=0, highlightthickness=0)
    side_bar_button.grid(row=0, column=3)

    add_image_pre = Image.open('./Assets/add.png').resize((20, 20))
    add_image = ImageTk.PhotoImage(add_image_pre)
    root.add_image = add_image  # Store in root to persist

    add_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    add_frame.pack(fill='x')
    add_button = Button(add_frame, image=add_image,command=add)
    add_button.grid(row=0, column=0)
    add_label = Label(add_frame, text='ADD TASK')
    add_label.grid(row=0, column=1,padx=30)

    search_image_pre = Image.open('./Assets/search.png').resize((20, 20))
    search_image = ImageTk.PhotoImage(search_image_pre)
    root.search_image = search_image  # Store in root to persist

    search_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    search_frame.pack(fill='x')
    search_button = Button(search_frame, image=search_image,command=search)
    search_button.grid(row=0, column=0)
    search_label = Label(search_frame, text='SEARCH TASK')
    search_label.grid(row=0, column=1,padx=30)

    inbox_image_pre = Image.open('./Assets/inbox.png').resize((20, 20))
    inbox_image = ImageTk.PhotoImage(inbox_image_pre)
    root.inbox_image = inbox_image  # Store in root to persist

    inbox_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    inbox_frame.pack(fill='x')
    inbox_button = Button(inbox_frame, image=inbox_image,command=inbox)
    inbox_button.grid(row=0, column=0)
    inbox_label = Label(inbox_frame, text='INBOX')
    inbox_label.grid(row=0, column=1,padx=30)

    today_image_pre = Image.open('./Assets/today.png').resize((20, 20))
    today_image = ImageTk.PhotoImage(today_image_pre)
    root.today_image = today_image  # Store in root to persist

    today_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    today_frame.pack(fill='x')
    today_button = Button(today_frame, image=today_image,command=today)
    today_button.grid(row=0, column=0)
    today_label = Label(today_frame, text='TODAY')
    today_label.grid(row=0, column=1,padx=30)

    upcoming_image_pre = Image.open('./Assets/upcoming.png').resize((20, 20))
    upcoming_image = ImageTk.PhotoImage(upcoming_image_pre)
    root.upcoming_image = upcoming_image  # Store in root to persist

    upcoming_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    upcoming_frame.pack(fill='x')
    upcoming_button = Button(upcoming_frame, image=upcoming_image,command=upcoming)
    upcoming_button.grid(row=0, column=0)
    upcoming_label = Label(upcoming_frame, text='UPCOMING')
    upcoming_label.grid(row=0, column=1,padx=30)

    home_image_pre = Image.open('./Assets/home.png').resize((20, 20))
    home_image = ImageTk.PhotoImage(home_image_pre)
    root.home_image = home_image  # Store in root to persist

    home_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    home_frame.pack(fill='x')
    home_button = Button(home_frame, image=home_image,command=home)
    home_button.grid(row=0, column=0)
    home_label = Label(home_frame, text='HOME')
    home_label.grid(row=0, column=1,padx=30)

    calendar_image_pre = Image.open('./Assets/calendar.png').resize((20, 20))
    calendar_image = ImageTk.PhotoImage(calendar_image_pre)
    root.calendar_image = calendar_image  # Store in root to persist

    calendar_frame = Frame(side_bar_frame, relief="sunken", borderwidth=2)
    calendar_frame.pack(fill='x')
    calendar_button = Button(calendar_frame, image=calendar_image,command=calendar)
    calendar_button.grid(row=0, column=0)
    calendar_label = Label(calendar_frame, text='CALENDAR')
    calendar_label.grid(row=0, column=1,padx=30)

# Main Tkinter window
root = Tk()
root.title("DO IT")
x=None

# Bind window resizing to maximize function
root.bind('<Configure>', maximize_window)

# Frame containing Sign Up and Log In buttons
form = Frame(root)
form.pack(pady=200)

sign_up_button_option = Button(form, text="Sign Up", command=sign_up)
sign_up_button_option.grid(row=0, column=0)

log_in_button_option = Button(form, text="Log In", command=log_in)
log_in_button_option.grid(row=0, column=2)

# Start the main event loop
root.mainloop()
