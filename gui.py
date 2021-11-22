from tkinter import *
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
HEADER = 1024
PORT = 12345
FORMAT = 'utf-8'
SERVER = 'localhost'
ADDR = (SERVER, PORT)

# A list of all morph names (strings)
morph_names = morphs.getMorphNamesOnly(morphs.allMorphs)

loggedIn = False        # tracks user login state
username = ""           # holds username info
user_snakes = {}        # holds user's custom list of snakes

# These numbers are used for placement of morphs on the calculator page
p1_row = 5
p2_row = 5

# These are used for storing morph info to add custom snakes
temp_row = 0
temp_morphs = []
temp_labels = []
temp_buttons = []

############################### Socket Connections ###############################

# This is used for connecting to the user account server
# Returns 1 if there's an error connecting
def connect_to_server():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        print(f"Client connected to {SERVER} on port {PORT}")
    except:
        client = 1

    return client

# This function formats a dict to send to a server,
# letting it know how long of a message to expect first
def send(client, dict):
    dict = json.dumps(dict)

    # Encode the message and get its length
    message = dict.encode(FORMAT)
    msg_length = len(message)                                   # msg_length is an int
    send_length = str(msg_length).encode(FORMAT)                # send_length turns msg_length to a str and encodes it
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# This function waits for a response from the server and
# returns the response (as a string)
def receive(client):
    msg_len = int(client.recv(HEADER).decode())
    response = client.recv(msg_len).decode()

    return response

# This disconnects from the server
def disconnect_server(conn):
    conn.close()


############################## Commands and Functions ###############################


######## Menu Navigation Buttons ########

# Navigate to home page (calculator)
def go_home():
    build_login_frame(0)

    glossaryFrame.grid_remove()
    collectionFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    calcFrame.grid(row=1, column=0)

# Navigate to glossary page
def go_glossary():
    build_login_frame(0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    collectionFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    glossaryFrame.grid(row=1, column=0)

# Navigate to collection page
def go_collection():
    build_login_frame(0)
    clear_frame(collectionFrame, 0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    glossaryFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    collectionFrame.grid(row=1, column=0)

    # snakesLabel.pack()

# Navigate to login page
def go_login():
    build_login_frame(0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    collectionFrame.grid_remove()
    glossaryFrame.grid_remove()
    logoutFrame.grid_remove()
    loginFrame.grid(row=1, column=0)

# Navigate to logout page
def go_logout():
    build_login_frame(0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    collectionFrame.grid_remove()
    loginFrame.grid_remove()
    glossaryFrame.grid_remove()
    logoutFrame.grid(row=1, column=0)


######## Glossary Construction ########

# This is used for constructing a scrollbox within the Glossary frame
# Code adapted from:
# https://bytes.com/topic/python/answers/157174-how-get-scrollregion-adjust-w-window-size
def build_scrollframe():
    # Create canvas and scrollbar
    canv = Canvas(glossaryFrame, height=650, width=400)
    vsb = Scrollbar(glossaryFrame, orient="v", command=canv.yview)
    canv.configure(yscrollcommand=vsb.set)

    glossaryFrame.grid_rowconfigure(0, weight=1)
    glossaryFrame.grid_columnconfigure(0, weight=1)

    # Determine scroll area
    canv.configure(scrollregion=(0, 0, 300, 12800))

    y = 100             # y is the location on canvas to place something
    global image_ref    # image_ref maintains references to our images
    image_ref = []

    # Add all the morphs to the canvas
    for i in morphs.allMorphs:
        path = i.getImageLoc()
        img = Image.open(path)
        img = img.resize((390,290), Image.ANTIALIAS)
        pimg = ImageTk.PhotoImage(img)
        image_ref.append(pimg)
        canv.create_image((0,y), anchor=W, image=pimg)

        name = i.getName().capitalize()
        canv.create_text((0,y+170), anchor=W, text=name, font=('Arial', '18', 'bold'))

        desc = i.getDescription()
        canv.create_text((0,y+200), anchor=W, text=desc, width=390)

        y = y + 400

    # Place the canvas and scrollbar
    canv.grid(row=1, column=0, sticky="nsew")
    vsb.grid(row=1, column=1, sticky="ns")


######## Collection Construction ########

# This builds the frame within the collection page, with an option to display errors
def build_newSnake_frame(error, str=""):
    warning = Label(newSnakeFrame, text="Error: " + str, fg="red")
    clear_login_entry()

    # If there's no error, build the standard newSnakeFrame frame:
    if error == 0:
        clear_frame(newSnakeFrame, 0)
        add_snake_title.grid(row=0, column=0, padx=10, pady=10, columnspan=4)
        add_snake_name.grid(row=1, column=0)
        as_name.grid(row=1, column=1, columnspan=3)
        add_snake_morph.grid(row=2, column=0, pady=10)
        add_snake_menu.grid(row=2, column=1)
        hetCheck3.grid(row=2, column=2)
        add3.grid(row=2, column=3)
        add_snake_morph_list.grid(row=3, column=0)
        newSnakeMorphList.grid(row=3, column=1, pady=10, columnspan=3)
        add_snake_list_empty.grid(row=0, column=0)
        save_snake.grid(row=4, column=0, padx=10, pady=10, columnspan=4)
    # Builds the frame with an error message from str parameter
    elif error == 1:
        clear_frame(newSnakeFrame, 0)
        add_snake_title.grid(row=0, column=0, padx=10, pady=10, columnspan=4)
        warning.grid(row=1, column=0, columnspan=4)
        add_snake_name.grid(row=2, column=0)
        as_name.grid(row=2, column=1, columnspan=3)
        add_snake_morph.grid(row=3, column=0, pady=10)
        add_snake_menu.grid(row=3, column=1)
        hetCheck3.grid(row=3, column=2)
        add3.grid(row=3, column=3)
        add_snake_morph_list.grid(row=4, column=0)
        newSnakeMorphList.grid(row=4, column=1, pady=10, columnspan=3)
        add_snake_list_empty.grid(row=0, column=0)
        save_snake.grid(row=5, column=0, padx=10, pady=10, columnspan=4)

# Store chosen morphs while creating new snake
def store_morph(name, het):
    global temp_morphs
    global temp_labels
    global temp_buttons
    global temp_row

    # Fill in any empty spots in the list before adding new ones
    if "none" in temp_morphs:
        current_index = temp_morphs.index("none")
    else:
        current_index = temp_row

    # Store morph info for later
    if het == 0:
        temp_morphs.insert(current_index, name)
    elif het == 1:
        name = "het " + name
        temp_morphs.insert(current_index, name)

    # Display the chosen morph
    add_snake_list_empty.grid_forget()
    new_morph_label = Label(newSnakeMorphList, text=name)
    new_morph_label.grid(row=temp_row, column=0, columnspan=2)
    temp_labels.insert(current_index, new_morph_label)

    # Add the option to remove it later
    remove_morph_button = Button(newSnakeMorphList, text="X Remove", font=('Arial', 8), command=lambda: remove_stored_morph(current_index))
    remove_morph_button.grid(row=temp_row, column=2)
    temp_buttons.insert(current_index, remove_morph_button)

    # Increment current row for display
    temp_row = temp_row + 1

# This function removes stored morphs while selecting to save a new snake
def remove_stored_morph(index):
    global temp_morphs
    global temp_labels
    global temp_buttons
    global temp_row

    # Remove morph at index
    temp_morphs[index] = "none"
    temp_labels[index].grid_forget()
    temp_buttons[index].grid_forget()

# This creates a new snake object and saves it to the user's account
def create_save_snake(name):
    global temp_morphs

    build_newSnake_frame(0)

    # Make sure user selected at least one morph
    no_morphs_found = True
    for item in temp_morphs:
        if item != "none":
            no_morphs_found = False

    # Either give an error or proceed
    if no_morphs_found:
        build_newSnake_frame(1, "You must select at least one morph.")
    else:
        print(f"Save snake named {name}")
        # Convert snake into JSON with temp_morphs

        # Clear entries

        # Clear temp_morphs, labels, buttons

        # Clear user inputs for saved snake

        # Build page

# This is for clearing saved snake fields
def clear_newSnakeFrame_entry():
    un.delete(0, END)
    pw.delete(0, END)


######## Login Page Construction ########

# This builds the frame within the login page, with an option to display errors
def build_login_frame(error, str=""):
    warning = Label(loginFrame, text="Error: " + str, fg="red")
    clear_login_entry()

    # If there's no error, build the standard login frame:
    if error == 0:
        clear_frame(loginFrame, 0)
        title_login.grid(row=0, column=0, columnspan=2)
        username_entry.grid(row=1, column=0)
        un.grid(row=1, column=1)
        password_entry.grid(row=2, column=0)
        pw.grid(row=2, column=1)
        submit.grid(row=3, column=0)
        create.grid(row=3, column=1)
    # Builds the frame with an error message from str parameter
    elif error == 1:
        clear_frame(loginFrame, 0)
        warning.grid(row=0, column=0, columnspan=2)
        title_login.grid(row=1, column=0, columnspan=2)
        username_entry.grid(row=2, column=0)
        un.grid(row=2, column=1)
        password_entry.grid(row=3, column=0)
        pw.grid(row=3, column=1)
        submit.grid(row=4, column=0)
        create.grid(row=4, column=1)

# This is for clearing login username/password fields
def clear_login_entry():
    un.delete(0, END)
    pw.delete(0, END)


######## Login Server Actions ########
# This function attempts to create an account with username and password
def account_create(user, pw):
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:
        # Prevents empty user info
        if user == "":
            build_login_frame(1, "Username required.")
        elif pw == "":
            build_login_frame(1, "Password required.")
        else:
            sendmsg = {
                "action":"create",
                "username": user,
                "password": pw,
                "description":"{}"
            }

            send(client, sendmsg)
            response = receive(client)

            # Handles error
            if "1" in response:
                response = json.loads(response)
                build_login_frame(1, response["1"])
            # Creation successful
            elif "0" in response:
                print(f"Account created: {user}")
                global username
                username = user
                login()

        disconnect_server(client)

    # Server ran into an error...
    else:
        build_login_frame(1, "Could not connect to server.")

# This function attempts to log in with username and password
def account_submit_login(user, pw):
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:
        # Prevents empty user info
        if user == "":
            build_login_frame(1, "Username required.")
        elif pw == "":
            build_login_frame(1, "Password required.")
        else:
            sendmsg = {
                "action":"login",
                "username": user,
                "password": pw
            }

            send(client, sendmsg)
            response = receive(client)

            # Handles invalid user error
            if "1" in response:
                response = json.loads(response)
                build_login_frame(1, "Username does not exist.")
            # Handles incorrect password error
            elif "2" in response:
                response = json.loads(response)
                build_login_frame(1, response["2"])
            # Creation successful
            elif "0" in response:
                print(f"Account logged in: {user}")
                global username
                username = user
                login()

        disconnect_server(client)
    # Server ran into an error...
    else:
        build_login_frame(1, "Could not connect to server.")

# This function attempts to log out of a user's account
def account_logout():
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:
        global username
        sendmsg = {
            "action": "logout",
            "username": username
        }

        send(client, sendmsg)
        response = receive(client)

        # Logout successful
        if "0" in response:
            print(f"Account logged out: {username}")
            username = ""
            logout()

        disconnect_server(client)
    # Server ran into an error...
    else:
        print("Error: Could not connect to server.")

# This function attempts to update the user's description.
# This is used to save snakes to the account.
def account_edit(description):
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:
        global username
        sendmsg = {
            "action": "edit",
            "username": username,
            "new_description": description
        }

        send(client, sendmsg)
        response = receive(client)

        # Edit successful
        if "0" in response:
            print(f"Updated description for {username}:")
            print(f"New description: {description}")

        disconnect_server(client)
    # Server ran into an error...
    else:
        print("Error: Could not connect to server.")

# This function retrieve's a user's account information.
# It can also be used to return a user's description info.
def account_retrieve_description():
    client = connect_to_server()

    # If server connection is valid...
    if client != 1:
        global username
        sendmsg = {
            "action": "retrieve",
            "username": username
        }

        send(client, sendmsg)
        response = receive(client)

        # Retrieval successful
        if "description" in response:
            response = json.loads(response)
            disconnect_server(client)
            return response["description"]

        disconnect_server(client)
    # Server ran into an error...
    else:
        print("Error: Could not connect to server.")


######## Other Helper Functions ########

# This can be used to clear a frame, 0 for forget, 1 for detroy
def clear_frame(frame, setting):
    if setting == 0:
        for widgets in frame.winfo_children():
            widgets.grid_forget()
    if setting == 1:
        for widgets in frame.winfo_children():
            widgets.destroy()


############################### Create GUI objects ###############################

##### Frames #####
menuFrame = LabelFrame(root, padx=50, pady=5, borderwidth=0, highlightthickness=0)
calcFrame = LabelFrame(root, width=100, height=100)
resultsFrame = LabelFrame(root, text="Results")
glossaryFrame = LabelFrame(root)
collectionFrame = LabelFrame(root)
newSnakeFrame = LabelFrame(collectionFrame)
newSnakeMorphList = LabelFrame(newSnakeFrame)
loginFrame = LabelFrame(root)
logoutFrame = LabelFrame(root)

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

# Adjusts the login page after user logs in
def login():
    clear_login_entry()

    # Add snakes to collection page
    # global snakesLabel
    # snakesLabel = Label(collectionFrame, text=data['description'])

    loggedIn = True

    collectionButton.config(state=NORMAL)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid(row=0, column=3)
    logoutFrame.grid(row=1, column=0)
    loginButton.grid_remove()
    loginFrame.grid_remove()

# Adjusts the login page after user logs out
def logout():
    clear_login_entry()

    # Clear collection page
    # snakesLabel.destroy()

    loggedIn = False
    build_login_frame(0)

    collectionButton.config(state=DISABLED)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid_remove()
    logoutFrame.grid_remove()
    loginButton.grid(row=0, column=3)
    loginFrame.grid(row=1, column=0)

# Snake is the snake object, morph is morph name, het is true/false, column is 1 for parent 1 or 2 for parent 2
def add_morph_to_calc(snake, morph, het, column):
    # Look up inheritance
    inherit = ""

    for m in morphs.allMorphs:
        if m.name == morph:
            inherit = m.getInheritance()

    snake.addMorph(morphs.Morph(morph, inherit, het, False))

    if column == 1:
        global p1_row

        morph_label = Label(calcFrame, text=snake.getMorphList()[-1])
        morph_label.grid(row=p1_row, column=0)
        p1_row = p1_row + 1
    elif column == 2:
        global p2_row

        morph_label = Label(calcFrame, text=snake.getMorphList()[-1])
        morph_label.grid(row=p2_row, column=2)
        p2_row = p2_row + 1

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

##### Menu Navigation Buttons #####

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
add1 = Button(calcFrame, text="Add", padx=40, command=lambda: add_morph_to_calc(morphcalc.p1, selected1.get(), het1.get(), 1))
selected2 = StringVar()
selected2.set(morph_names[0])
p2_morphs = OptionMenu(calcFrame, selected2, *morph_names)
add2 = Button(calcFrame, text="Add", padx=40, command=lambda: add_morph_to_calc(morphcalc.p2, selected2.get(), het2.get(), 2))
het2 = IntVar()
hetCheck2 = Checkbutton(calcFrame, text="Het", variable=het2)
calculate = Button(calcFrame, text="Calculate Results", padx=40, pady=10, command=calculate_results)
res_clear = Button(root, text="Clear results", command=clear_results)

# Labels for glossary
title_glossary = Label(glossaryFrame, text="Morph List", font=('Arial', 20))

# Labels, buttons for collection
title_collection = Label(collectionFrame, text="My Collection", font=('Arial', 20))
add_snake_title = Label(newSnakeFrame, text="Add a new snake:", font=('Arial', 12, 'italic'))
add_snake_name = Label(newSnakeFrame, text="Name: ", anchor=E)
as_name = Entry(newSnakeFrame, width=35)
add_snake_morph_list = Label(newSnakeFrame, text="Selected morphs: ", anchor=E)
add_snake_list_empty = Label(newSnakeMorphList, text="None selected", font=('Arial', 9, 'italic'))
add_snake_morph = Label(newSnakeFrame, text="Add morphs: ", anchor=E)
selected3 = StringVar()
selected3.set(morph_names[0])
het3 = IntVar()
hetCheck3 = Checkbutton(newSnakeFrame, text="Het", variable=het3)
add_snake_menu = OptionMenu(newSnakeFrame, selected3, *morph_names)
add3 = Button(newSnakeFrame, text="Add", command=lambda: store_morph(selected3.get(), het3.get()))
save_snake = Button(newSnakeFrame, text="Save this snake to your account", padx=10, pady=10, command=lambda: create_save_snake(as_name.get()))

# Labels, entry, buttons for login
title_login = Label(loginFrame, text="Log in to account: ")
username_entry = Label(loginFrame, text="Username: ")
un = Entry(loginFrame, width=20)
password_entry = Label(loginFrame, text="Password: ")
pw = Entry(loginFrame, show="*", width=20)
submit = Button(loginFrame, text="Submit", command=lambda: account_submit_login(un.get(), pw.get()))
create = Button(loginFrame, text="Create Account", command=lambda: account_create(un.get(), pw.get()))

# Labels, buttons for logout
confirmation = Label(logoutFrame, text="You are currently logged in.")
title_logout = Label(logoutFrame, text="Log out of account?")
yes = Button(logoutFrame, text="Yes", command=account_logout)
no = Button(logoutFrame, text="No", command=go_home)


############################### Display GUI objects ###############################

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
title_glossary.grid(row=0, column=0)
build_scrollframe()

# Collection frame
title_collection.pack()
newSnakeFrame.pack()
build_newSnake_frame(0)


# Login frame
build_login_frame(0)

# Logout frame
confirmation.grid(row=0, column=0, columnspan=2)
title_logout.grid(row=1, column=0, columnspan=2)
yes.grid(row=2, column=0)
no.grid(row=2, column=1)

### This runs the GUI
root.mainloop()