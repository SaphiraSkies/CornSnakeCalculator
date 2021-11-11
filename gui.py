from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import morphs
import morphcalc
import json
import socket

### Always needed first
root = Tk()
root.geometry("600x800")
root.title("Corn Snake Morph Calculator")
root.iconbitmap("favicon.ico")

### Need this for server connections
HEADER = 64
PORT = 12345
FORMAT = 'utf-8'
SERVER = 'localhost'
ADDR = (SERVER, PORT)

morph_names = morphs.getMorphNamesOnly(morphs.allMorphs)

# Tracks if user is logged in or not
loggedIn = False
userToken = 999999
current_row1 = 5
current_row2 = 5

# This function formats a message to send to a server,
# letting it know how long of a message to expect first
def send(client, msg):
    # Encode the message and get its length
    message = msg.encode(FORMAT)
    msg_length = len(message)                                   # msg_length is an int
    send_length = str(msg_length).encode(FORMAT)                # send_length turns msg_length to a str and encodes it
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

#################### First create objects ####################

##### Frames #####
menuFrame = LabelFrame(root, padx=50, pady=5, borderwidth=0, highlightthickness=0)
calcFrame = LabelFrame(root, width=100, height=100)
resultsFrame = LabelFrame(root, text="Results")
glossaryFrame = LabelFrame(root)
collectionFrame = LabelFrame(root)
loginFrame = LabelFrame(root)
logoutFrame = LabelFrame(root)

##### Menu buttons #####
def go_home():
    build_login_frame(0)

    glossaryFrame.grid_remove()
    collectionFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    calcFrame.grid(row=1, column=0)

def go_glossary():
    build_login_frame(0)

    calcFrame.grid_remove()
    collectionFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    glossaryFrame.grid(row=1, column=0)

def go_collection():
    build_login_frame(0)
    clear_frame(collectionFrame, 0)

    calcFrame.grid_remove()
    glossaryFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    collectionFrame.grid(row=1, column=0)

    snakesLabel.pack()

def go_login():
    build_login_frame(0)

    calcFrame.grid_remove()
    collectionFrame.grid_remove()
    glossaryFrame.grid_remove()
    logoutFrame.grid_remove()
    loginFrame.grid(row=1, column=0)

def go_logout():
    build_login_frame(0)

    calcFrame.grid_remove()
    collectionFrame.grid_remove()
    loginFrame.grid_remove()
    glossaryFrame.grid_remove()
    logoutFrame.grid(row=1, column=0)

# This is for clearing username/password fields
def clear_login_entry():
    un.delete(0, END)
    pw.delete(0, END)

# This is used for connecting to the user account server
def connect_to_server():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        print(f"Client connected to {SERVER} on port {PORT}")
    except:
        client = 1

    return client

# This disconnects from the server
def disconnect_server(conn):
    conn.close()

# This can be used to clear a frame, 0 for forget, 1 for detroy
def clear_frame(frame, setting):
    if setting == 0:
        for widgets in frame.winfo_children():
            widgets.grid_forget()
    if setting == 1:
        for widgets in frame.winfo_children():
            widgets.destroy()

# This builds the login frame with an option to display errors
def build_login_frame(error, str=""):
    warning = Label(loginFrame, text="Error: " + str, fg="red")
    clear_login_entry()

    # If there's no error, build the standard login frame:
    if error == 0:
        clear_frame(loginFrame, 0)
        title_login.grid(row=0, column=0, columnspan=2)
        username.grid(row=1, column=0)
        un.grid(row=1, column=1)
        password.grid(row=2, column=0)
        pw.grid(row=2, column=1)
        submit.grid(row=3, column=0)
        create.grid(row=3, column=1)
    # Builds the frame with an error message from str parameter
    elif error == 1:
        warning.grid(row=0, column=0, columnspan=2)
        title_login.grid(row=1, column=0, columnspan=2)
        username.grid(row=2, column=0)
        un.grid(row=2, column=1)
        password.grid(row=3, column=0)
        pw.grid(row=3, column=1)
        submit.grid(row=4, column=0)
        create.grid(row=4, column=1)

def temp_submit_process(username, pw):
    if userToken == 999999:
        build_login_frame(1, "You must first create an account.")
    else:
        login()

def temp_create_process(username, pw):
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:

        sendmsg = {
            "action": "create",
            "username": username,
            "description": "Snake 1:\nSpot\nnormal\n\nSnake 2:\nMissy\nhet albino"
        }

        y = json.dumps(sendmsg)
        y = y.encode('utf-8')
        ylen = len(y)
        ylen_str = str(ylen).encode('utf-8')
        ylen_buffer = b' ' * (1024 - len(ylen_str)) + ylen_str
        client.send(ylen_buffer)
        client.send(y)

        # Block here, wait for a response...
        client.recv(1024).decode()
        msg = client.recv(1024).decode()

        # Show the received message
        # print(f"Received from server: {msg}")
        global userToken
        userToken = msg[14:len(msg)-1]
        # print(f"Token: \n{userToken}")

        login()

        disconnect_server(client)
    # Server ran into an error...
    else:
        build_login_frame(1, "Could not connect to server.")

# This function verifies login attempts
def submit_login(user, pw):
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:

        # CHECK LOGIN

        # IF successful...
        # ELIF not successful...

        disconnect_server(client)
    # Server ran into an error...
    else:
        build_login_frame(1, "Could not connect to server.")

# This function verifies account creation attempts
def create_login(user, pw):
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:

        # CHECK LOGIN

        disconnect_server(client)
    # Server ran into an error...
    else:
        build_login_frame(1, "Could not connect to server.")

# The login process takes username and password strings for verification
def login():
    clear_login_entry()

    client = connect_to_server()

    sendmsg = {
        "action": "retrieve",
        "userToken": userToken
    }

    b = json.dumps(sendmsg)
    b = b.encode('utf-8')
    blen = len(b)
    blen_str = str(blen).encode('utf-8')
    blen_buffer = b' ' * (1024 - len(blen_str)) + blen_str
    client.send(blen_buffer)
    client.send(b)

    client.recv(1024).decode()
    msg = client.recv(1024).decode()
    data = json.loads(msg)

    global snakesLabel
    snakesLabel = Label(collectionFrame, text=data['description'])

    disconnect_server(client)

    loggedIn = True
    loginButton.grid_remove()
    collectionButton.config(state=NORMAL)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid(row=0, column=3)

    loginFrame.grid_remove()
    logoutFrame.grid(row=1, column=0)

def logout():
    clear_login_entry()
    snakesLabel.destroy()

    loggedIn = False
    collectionButton.config(state=DISABLED)
    collectionButton.grid(row=0, column=2)
    loginButton.grid(row=0, column=3)
    logoutButton.grid_remove()

    logoutFrame.grid_remove()
    loginFrame.grid(row=1, column=0)

# Snake is the snake, morph is morph name, het is true/false, column is 1 for parent 1 or 2 for parent 2
def addMorph(snake, morph, het, column):
    # Look up inheritance
    inherit = ""

    for m in morphs.allMorphs:
        if m.name == morph:
            inherit = m.getInheritance()

    snake.addMorph(morphs.Morph(morph, inherit, het, False))

    if column == 1:
        global current_row1

        morph_label = Label(calcFrame, text=snake.getMorphList()[-1])
        morph_label.grid(row=current_row1, column=0)
        current_row1 = current_row1 + 1
    elif column == 2:
        global current_row2

        morph_label = Label(calcFrame, text=snake.getMorphList()[-1])
        morph_label.grid(row=current_row2, column=2)
        current_row2 = current_row2 + 1

# This clears the breeding results frame from the calc menu
def clear_results():
    clear_frame(resultsFrame, 1)
    resultsFrame.grid_forget()
    res_clear.grid_forget()

# This function calculates breeding results
def calculate_results():
    clear_frame(resultsFrame, 1)

    results = morphcalc.breedResults(morphcalc.p1, morphcalc.p2)

    res_clear.grid(row=2, column=0, padx=10, pady=10)
    resultsLabel = Label(resultsFrame, text=results)
    resultsLabel.pack()
    resultsFrame.grid(row=3, column=0)


homeButton = Button(menuFrame, text="Home", width=15, height=1, command=go_home)
glossaryButton = Button(menuFrame, text="Morph Glossary", width=15, height=1, command=go_glossary)
loginButton = Button(menuFrame, text="Log In", width=15, height=1, command=go_login)
collectionButton = Button(menuFrame, text="My Collection", width=15, height=1, command=go_collection)
logoutButton = Button(menuFrame, text="Log Out", width=15, height=1, command=go_logout)

##### Items for frames #####

# Labels, buttons, entry for calcFrame
title_home = Label(calcFrame, text="Morph Calculator", font=('Arial', 20))
p1_label = Label(calcFrame, text="Parent 1's morphs:")
p2_label = Label(calcFrame, text="Parent 2's morphs:")
selected1 = StringVar()
selected1.set(morph_names[0])
het1 = IntVar()
hetCheck1 = Checkbutton(calcFrame, text="Het", variable=het1)
p1_morphs = OptionMenu(calcFrame, selected1, *morph_names)
add1 = Button(calcFrame, text="Add", padx=40, command=lambda: addMorph(morphcalc.p1, selected1.get(), het1.get(), 1))
selected2 = StringVar()
selected2.set(morph_names[0])
p2_morphs = OptionMenu(calcFrame, selected2, *morph_names)
add2 = Button(calcFrame, text="Add", padx=40, command=lambda: addMorph(morphcalc.p2, selected2.get(), het2.get(), 2))
het2 = IntVar()
hetCheck2 = Checkbutton(calcFrame, text="Het", variable=het2)
calculate = Button(calcFrame, text="Calculate Results", padx=40, pady=10, command=calculate_results)
res_clear = Button(root, text="Clear results", command=clear_results)

# Labels for glossary
title_glossary = Label(glossaryFrame, text="Morph List", font=('Arial', 20))
normal_image = ImageTk.PhotoImage(Image.open("images/normal-a.jpg"))
normal_img_label = Label(glossaryFrame, image=normal_image)
normal_title = Label(glossaryFrame, text="Normal", font=('Arial', 14))
normal_description = Label(glossaryFrame, text="A standard wild type morph.", font=('Arial', 10))
amel_image = ImageTk.PhotoImage(Image.open("images/amelanistic-a.jpg"))
amel_img_label = Label(glossaryFrame, image=amel_image)
amel_title = Label(glossaryFrame, text="Amelanistic", font=('Arial', 14))
amel_description = Label(glossaryFrame, text="AKA 'albino' or 'amel'. Lacks melanin (black coloration).", font=('Arial', 10))
anery_image = ImageTk.PhotoImage(Image.open("images/anerythristic-a.jpg"))
anery_img_label = Label(glossaryFrame, image=anery_image)
anery_title = Label(glossaryFrame, text="Anerythristic", font=('Arial', 14))
anery_description = Label(glossaryFrame, text="AKA 'anery'. Lacks red pigment.", font=('Arial', 10))

# Labels for collection
title_collection = Label(collectionFrame, text="My Collection", font=('Arial', 20))

# Labels, entry, buttons for login
title_login = Label(loginFrame, text="Log in to account: ")
username = Label(loginFrame, text="Username: ")
un = Entry(loginFrame, width=20)
password = Label(loginFrame, text="Password: ")
pw = Entry(loginFrame, show="*", width=20)
submit = Button(loginFrame, text="Submit", command=lambda: temp_submit_process(un.get(), pw.get()))
create = Button(loginFrame, text="Create Account", command=lambda: temp_create_process(un.get(), pw.get()))

# Labels, buttons for logout
confirmation = Label(logoutFrame, text="You are currently logged in.")
title_logout = Label(logoutFrame, text="Log out of account?")
yes = Button(logoutFrame, text="Yes", command=logout)
no = Button(logoutFrame, text="No", command=go_home)

#################### Second, display it ####################


##### FILL THE GUI #####

# Menu Frame
menuFrame.grid(row=0, column=0)
homeButton.grid(row=0, column=0, pady=10)
glossaryButton.grid(row=0, column=1)
if loggedIn:
    collectionButton.config(state=NORMAL)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid(row=0, column=3)
else:
    collectionButton.config(state=DISABLED)
    collectionButton.grid(row=0, column=2)
    loginButton.grid(row=0, column=3)

# Home/Calculator Frame
title_home.grid(row=0, column=0, columnspan=4)
calcFrame.grid(row=1, column=0)
p1_morphs.grid(row=1, column=0)
hetCheck1.grid(row=1, column=1)
p2_morphs.grid(row=1, column=2)
hetCheck2.grid(row=1, column=3)
add1.grid(row=2, column=0, columnspan=2)
add2.grid(row=2, column=2, columnspan=2)
calculate.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
p1_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
p2_label.grid(row=4, column=2, columnspan=2, padx=10, pady=10)

# Glossary frame
title_glossary.pack()
normal_img_label.pack()
normal_title.pack()
normal_description.pack()
amel_img_label.pack()
amel_title.pack()
amel_description.pack()
anery_img_label.pack()
anery_title.pack()
anery_description.pack()

# Collection frame
title_collection.pack()

# Login frame
build_login_frame(0)

# Logout frame
confirmation.grid(row=0, column=0, columnspan=2)
title_logout.grid(row=1, column=0, columnspan=2)
yes.grid(row=2, column=0)
no.grid(row=2, column=1)

### This runs the GUI
root.mainloop()