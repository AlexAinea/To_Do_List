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
    notification_image_pre = Image.open('./Assets/bell.png').resize((50, 50))
    notification_image = ImageTk.PhotoImage(notification_image_pre)
    root.notification_image = notification_image  # Store in root to persist

    overdue_button = Button(user_details_frame, image=notification_image, command=notifications, borderwidth=0, highlightthickness=0)
    overdue_button.grid(row=0, column=2)

    # Sidebar image processing
    side_pre = Image.open('./Assets/sidebar.png').resize((50, 50))
    side_bar_image = ImageTk.PhotoImage(side_pre)
    root.side_bar_image = side_bar_image  # Store in root to persist

    side_bar_button = Button(user_details_frame, image=side_bar_image, command=notifications, borderwidth=0, highlightthickness=0)
    side_bar_button.grid(row=0, column=3)


# Main Tkinter window
root = Tk()
root.title("DO IT")

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
