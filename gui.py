from tkinter import *
from PIL import ImageTk,Image
import morphs
import morphcalc
import json
import socket

### Build the GUI base
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


# User-related variables
loggedIn = False        # tracks user login state
username = ""           # holds username info
user_snakes_dict = "[]" # holds user's description (list of snakes as dicts), "[]" when empty
user_snakes_obj = []    # holds user's custom list of snakes as Snake objects


# These numbers are used for placement of morphs on the calculator page
p1_row = 5
p2_row = 5

# These are used for storing morph info to add snakes to collection
temp_row = 0
temp_morphs = []
temp_labels = []
temp_buttons = []

# These are used for managing some frames
p1_labels = []
p2_labels = []
snakeItemList = []


############################### Socket Connections ###############################
#                                                                                #
#     These functions are for communicating with an accounts microservice.       #
#                                                                                #
##################################################################################

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
# letting it know message size to expect first
def send(client, dict):
    dict = json.dumps(dict)
    print(f"Client sending: {dict}")

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

    print(f"Client received: {response}")

    return response

# This disconnects from the server
def disconnect_server(conn):
    print("Client disconnected from server.")
    conn.close()


############################## Commands and Functions ###############################
#                                                                                   #
#                       These functions make the app work.                          #
#                                                                                   #
#####################################################################################


######## Menu Navigation Functions ########

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
    clear_newSnakeFrame_entry()
    build_newSnake_frame(0)

    global user_snakes_dict
    if user_snakes_dict != "[]":
        display_collection()

    add_snake_selected.set(morph_names[0])
    add_snake_het_val.set(0)
    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    glossaryFrame.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    collectionFrame.grid(row=1, column=0)

# Navigate to login page
def go_login():
    build_login_frame(0)
    build_newSnake_frame(0)

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


######## Home Calculator Functions ########

# Clears and builds the calculator frame
def build_calc_frame():
    clear_frame(calcFrame, 0)

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

# Clears just the p1 or p2 morphs from the calculator
# Option = 1 for p1, option = 2 for p2
def clear_calc_column(option):
    global p1_row
    global p2_row

    if option == 1:
        for x in p1_labels:
            x.grid_forget()
            p1_row = p1_row - 1
    elif option == 2:
        for x in p2_labels:
            x.grid_forget()
            p2_row = p2_row - 1

# Snake is the snake object, morph is morph name, het is true/false, column is 1 for parent 1 or 2 for parent 2
def add_morph_to_calc(snake, morph, het, column):
    # Look up inheritance
    inherit = ""

    global p1_labels
    global p2_labels

    for m in morphs.allMorphs:
        if m.name == morph:
            inherit = m.getInheritance()

    snake.addMorph(morphs.Morph(morph, inherit, het, False))

    if column == 1:
        global p1_row

        morph_label = Label(calcFrame, text=snake.getMorphList()[-1])
        morph_label.grid(row=p1_row, column=0)
        p1_row = p1_row + 1
        p1_labels.append(morph_label)
    elif column == 2:
        global p2_row

        morph_label = Label(calcFrame, text=snake.getMorphList()[-1])
        morph_label.grid(row=p2_row, column=2)
        p2_row = p2_row + 1
        p2_labels.append(morph_label)

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


######## Glossary Functions ########

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


######## Collection Functions ########

# This builds the frame within the collection page, with an option to display errors
def build_newSnake_frame(error, str=""):
    print(".. CALLING BUILD_NEWSNAKE_FRAME ..")
    warning = Label(newSnakeFrame, text="Error: " + str, fg="red")
    global user_snakes_dict

    # If there's no error, build the standard newSnakeFrame frame:
    if error == 0:
        clear_frame(userSnakesFrame, 0)
        clear_frame(newSnakeFrame, 0)
        display_collection()
        newSnakeFrame.pack()
        if user_snakes_dict != "[]":
            userSnakesFrame.pack()
        add_snake_title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
        add_snake_name_label .grid(row=1, column=0)
        add_snake_name_entry.grid(row=1, column=1, columnspan=3)
        add_snake_morph_label.grid(row=2, column=0, pady=5)
        add_snake_morph_menu.grid(row=2, column=1)
        add_snake_het.grid(row=2, column=2)
        add_snake_add_button.grid(row=2, column=3)
        add_snake_selected_morph_label.grid(row=3, column=0)
        addSnakeSelectedMorphFrame.grid(row=3, column=1, pady=5, columnspan=3)
        add_snake_selected_list_empty.grid(row=0, column=0)
        add_snake_save_button.grid(row=4, column=0, padx=10, pady=10, columnspan=4)
    # Builds the frame with an error message from str parameter
    elif error == 1:
        clear_frame(userSnakesFrame, 0)
        clear_frame(newSnakeFrame, 0)
        display_collection()
        newSnakeFrame.pack()
        if user_snakes_dict != "[]":
            userSnakesFrame.pack()
        add_snake_title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
        warning.grid(row=1, column=0, columnspan=4)
        add_snake_name_label .grid(row=2, column=0)
        add_snake_name_entry.grid(row=2, column=1, columnspan=3)
        add_snake_morph_label.grid(row=3, column=0, pady=5)
        add_snake_morph_menu.grid(row=3, column=1)
        add_snake_het.grid(row=3, column=2)
        add_snake_add_button.grid(row=3, column=3)
        add_snake_selected_morph_label.grid(row=4, column=0)
        addSnakeSelectedMorphFrame.grid(row=4, column=1, pady=5, columnspan=3)
        add_snake_selected_list_empty.grid(row=0, column=0)
        add_snake_save_button.grid(row=5, column=0, padx=10, pady=10, columnspan=4)

# Store chosen morphs in a temp list while creating new snake
def store_morph(name, het):
    global temp_morphs
    global temp_labels
    global temp_buttons
    global temp_row

    build_newSnake_frame(0)

    current_index = temp_row

    # Store morph info for later
    if het == 0:
        temp_morphs.insert(current_index, name)
    elif het == 1:
        name = "het " + name
        temp_morphs.insert(current_index, name)

    # Display the chosen morph
    add_snake_selected_list_empty.grid_forget()
    new_morph_label = Label(addSnakeSelectedMorphFrame, text=name)
    new_morph_label.grid(row=temp_row, column=0, columnspan=2)
    temp_labels.insert(current_index, new_morph_label)

    # Add the option to remove it later
    remove_morph_button = Button(addSnakeSelectedMorphFrame, text="X Remove", font=('Arial', 8), command=lambda: remove_stored_morph(current_index))
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

    print(f"Removed morph at index {index}")

    # Remove morph at index
    temp_morphs[index] = "none"
    temp_labels[index].grid_forget()
    temp_buttons[index].grid_forget()

    if morphs_is_empty():
        add_snake_selected_list_empty.grid(row=0, column=0)

# Saves the selected snake to the user's account
def save_snake(name):
    global user_snakes_dict
    print(f".. CALLING SAVE_SNAKE ..")

    global temp_morphs

    build_newSnake_frame(0)
    userSnakesFrame.pack()

    # Either give an error or proceed
    if morphs_is_empty():
        build_newSnake_frame(1, "You must select at least one morph.")
    else:
        # Remove any empty slots in temp_morphs
        try:
            while True:
                temp_morphs.remove("none")
        except:
            pass

        snake_morph_list = temp_morphs.copy()

        # Create a dict for this snake
        snake = {
            "name": name,
            "morphs": snake_morph_list
        }

        # print(f'SAVING SNAKE: {snake["name"]} - {snake["morphs"]}')

        if user_snakes_dict == "[]":
            user_snakes_dict = []

        # Save this snake to the user's account
        user_snakes_dict.append(snake)
        description_to_snakes()
        account_edit(user_snakes_dict)
        display_collection()
        clear_newSnakeFrame_entry()

# Deletes a snake from the user's account
def delete_snake(snake):
    print(".. CALLING DELETE_SNAKE ..")
    global user_snakes_dict
    global user_snakes_obj

    print(f"Deleting snake: {snake}, type {type(snake)}")

    # Look for the item in user_names_dict and remove it
    print(f"User dict before: {user_snakes_dict}")
    for i in range(len(user_snakes_dict)):
        if user_snakes_dict[i] == snake:
            snake_str = str(snake)
            user_snakes_dict.pop(i)
            break
    print(f"User dict after: {user_snakes_dict}")

    # Look for the item in user_names_obj and remove it
    print(f"User obj before: {user_snakes_obj}")
    for i in range(len(user_snakes_dict)):
        name = user_snakes_obj[i].getName()
        morph_list = user_snakes_obj[i].getMorphList()
        print(f"Name: {name}, morphs: {morph_list}")
        if name == snake["name"]:
            if morph_list == snake["morphs"]:
                user_snakes_obj.pop(i)
                break
    print(f"User obj after: {user_snakes_obj}")

    # Adapt if the collection is now empty
    if not user_snakes_dict:
        user_snakes_dict = "[]"
        userSnakesFrame.pack_forget()

    # Update user description
    account_edit(user_snakes_dict)

    # Remove GUI objects
    clear_frame(userSnakesFrame, 0)
    display_collection()

# This removes existing data from stored morphs and resets the frame
def clear_stored_morphs():
    print(f".. CALLING CLEAR_STORED_MORPHS ..")

    global temp_row
    global temp_morphs
    global temp_labels
    global temp_buttons
    temp_row = 0
    temp_morphs.clear()
    temp_labels.clear()
    temp_buttons.clear()
    clear_frame(addSnakeSelectedMorphFrame, 0)
    add_snake_selected_list_empty.grid(row=0, column=0)

# This function tells you whether or not the temp_morph list is empty
# Returns True if empty, False if not
def morphs_is_empty():
    global temp_morphs

    no_morphs_found = True

    # If the list isn't empty, check for any index that is not "none"
    if temp_morphs:
        for item in temp_morphs:
            if item != "none":
                no_morphs_found = False

    return no_morphs_found

# This is for clearing saved snake fields
def clear_newSnakeFrame_entry():
    print(f".. CALLING CLEAR_NEWSNAKEFRAME_ENTRY ..")
    add_snake_name_entry.delete(0, END)
    clear_stored_morphs()

# This function will remove all of a user's snakes
def delete_collection():
    global user_snakes_dict
    print(f".. CALLING DELETE_COLLECTION ..")

    user_snakes_obj.clear()
    if user_snakes_dict != "[]":
        user_snakes_dict.clear()
    user_snakes_dict = "[]"
    account_edit("[]")
    clear_frame(userSnakesFrame, 0)
    userSnakesFrame.pack_forget()

# This adds a snake from the user's collection to the morph calculator
# Parent variable is 1 for p1 (parent #1) or 2 for p2 (parent #2)
def add_from_collection(snake, parent):
    print(f"Snake to p{parent}: {snake}")

    clear_calc_column(parent)

    snake_morphs = snake["morphs"].copy()

    # Read "het" as its own value
    for i in range(len(snake_morphs)):
        het = False
        if "het " in snake_morphs[i]:
            snake_morphs[i] = snake_morphs[i][4:]
            het = True

        if parent == 1:
            add_morph_to_calc(morphcalc.p1, snake_morphs[i], het, 1)
        elif parent == 2:
            add_morph_to_calc(morphcalc.p2, snake_morphs[i], het, 2)

# This function displays all the user's snakes on the collection frame
def display_collection():
    global user_snakes_dict

    print(f".. CALLING DISPLAY_COLLECTION ..")

    row = 0
    col = 0

    if user_snakes_dict != "[]":
        nuke_button = Button(userSnakesFrame, text="Delete All", padx=10, pady=10, command=delete_collection)
        nuke_button.grid(row=row, column=col, padx=10, pady=10, columnspan=4)

        userSnakesRow = 1
        userSnakesCol = -1

        global snakeItemList

        snakeFrameRow = 0
        snakeFrameCol = 0

        # Build a 4-column grid with each snake's name and morphs
        for i in range(len(user_snakes_dict)):
            snakeFrame = LabelFrame(userSnakesFrame)
            if user_snakes_dict[i]["name"] == "":
                name = "[Unnamed]"
            else:
                name = user_snakes_dict[i]["name"]
            snakeName = Label(snakeFrame, text=name, font=('Arial', 12, 'bold'))
            snakeName.grid(row=snakeFrameRow, column=snakeFrameCol, columnspan=2)
            for y in user_snakes_dict[i]["morphs"]:
                snakeFrameRow = snakeFrameRow + 1
                snakeMorph = Label(snakeFrame, text=y, font=('Arial', 10))
                snakeMorph.grid(row=snakeFrameRow, column=snakeFrameCol, columnspan=2)

            # Button to add this snake to p1 on the calculator
            snakeFrameRow = snakeFrameRow + 1
            add_to_p1_button = Button(snakeFrame, text="Select as\nParent 1", command=lambda i=i: add_from_collection(user_snakes_dict[i], 1))
            add_to_p1_button.grid(row=snakeFrameRow, column=snakeFrameCol, padx=5)

            # Button to add this snake to p2 on the calculator
            snakeFrameCol = snakeFrameCol + 1
            add_to_p2_button = Button(snakeFrame, text="Select as\nParent 2", command=lambda i=i: add_from_collection(user_snakes_dict[i], 2))
            add_to_p2_button.grid(row=snakeFrameRow, column=snakeFrameCol, padx=5)

            # Button for deleting this snake
            snakeFrameRow = snakeFrameRow + 1
            snakeFrameCol = snakeFrameCol - 1
            delete_snake_button = Button(snakeFrame, text="Delete this Snake", command=lambda i=i: delete_snake(user_snakes_dict[i]), padx=10)
            delete_snake_button.grid(row=snakeFrameRow, column=snakeFrameCol, columnspan=2, padx=5, pady=5)

            # Adjust grid position
            if userSnakesCol < 2:
                userSnakesCol = userSnakesCol + 1
            else:
                userSnakesCol = 0
                userSnakesRow = userSnakesRow + 1

            snakeFrame.grid(row=userSnakesRow, column=userSnakesCol, padx=10, pady=10)

            snakeItemList.append(snakeFrame)
            snakeItemList.append(snakeName)
            snakeItemList.append(delete_snake_button)

# This clears ALL of a user's snakes from the collection frame
def clear_user_snakes():
    global snakeItemList
    for x in snakeItemList:
        x.grid_forget()
    userSnakesFrame.pack_forget()


######## Login Page Functions ########

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

# Adjusts the login page after user logs in
def login():
    clear_login_entry()
    build_newSnake_frame(0)

    global user_snakes_dict
    if user_snakes_dict != "[]":
        display_collection()

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
    clear_frame(collectionFrame, 0)
    clear_user_snakes()

    loggedIn = False
    build_login_frame(0)
    build_newSnake_frame(0)

    collectionButton.config(state=DISABLED)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid_remove()
    logoutFrame.grid_remove()
    loginButton.grid(row=0, column=3)
    loginFrame.grid(row=1, column=0)


######## Login Server Functions ########

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
                "description": "[]"
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
    print(f".. CALLING ACCOUNT_SUBMIT_LOGIN ..")
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
                global user_snakes_dict
                username = user
                user_snakes_dict = account_retrieve_description()
                print(f"GOT DESCRIPTION: {user_snakes_dict}, type {type(user_snakes_dict)}")
                description_to_snakes()
                login()

        disconnect_server(client)
    # Server ran into an error...
    else:
        build_login_frame(1, "Could not connect to server.")

# This function attempts to log out of a user's account
def account_logout():
    print(f".. CALLING ACCOUNT_LOGOUT ..")
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
            global user_snakes_dict
            global user_snakes_obj

            clear_stored_morphs()

            print(f"Account logged out: {username}")
            username = ""
            if user_snakes_dict != "[]":
                user_snakes_dict.clear()
            user_snakes_dict = "[]"
            if user_snakes_obj:
                user_snakes_obj.clear()
            logout()

        disconnect_server(client)
    # Server ran into an error...
    else:
        print("Error: Could not connect to server.")

# This function attempts to update the user's description.
# This is used to save snakes to the account.
def account_edit(description):
    print(f".. CALLING ACCOUNT_EDIT ..")
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
    print(f".. CALLING ACCOUNT_DESCRIPTION ..")
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

# This function converts the user's description to a list of snakes
def description_to_snakes():
    print(".. CALLING DESCRIPTION_TO_SNAKES")
    global user_snakes_dict
    global user_snakes_obj

    # Cancel operation if there are no snakes for this user
    if user_snakes_dict == "[]":
        return

    # Scrap existing list
    user_snakes_obj.clear()

    # Generate new one
    for x in user_snakes_dict:
        dict_to_snake(x)

    print(f"OBJ Generated: {user_snakes_obj}")

# This takes a dict, creates a snake object from it, and adds it to the user's list
# Option is 0 to process the snake straight to the user_snakes_obj list
# Option 1 will return the snake as an object
def dict_to_snake(dict, option=0):
    global user_snakes_obj

    snake = morphcalc.Snake(dict["name"])
    morphs_list = dict["morphs"].copy()
    # Read "het" as its own value
    for i in range(len(morphs_list)):
        het = False
        if "het " in morphs_list[i]:
            morphs_list[i] = morphs_list[i][4:]
            het = True

        inherit = morphs.getInheritanceByName(morphs_list[i])

        snake.addMorph(morphs.Morph(morphs_list[i], inherit, het, False))

    if option == 0:
        user_snakes_obj.append(snake)
    elif option == 1:
        return snake


############################### Construct GUI objects ###############################
#                                                                                   #
#                  Tkinter objects need to be created before use.                   #
#                                                                                   #
#####################################################################################

##### Frames #####

menuFrame = LabelFrame(root, padx=50, pady=5, borderwidth=0, highlightthickness=0)
calcFrame = LabelFrame(root, width=100, height=100)
resultsFrame = LabelFrame(root, text="Results")
glossaryFrame = LabelFrame(root)
collectionFrame = LabelFrame(root)
newSnakeFrame = LabelFrame(collectionFrame)
userSnakesFrame = LabelFrame(collectionFrame)
addSnakeSelectedMorphFrame = LabelFrame(newSnakeFrame)
loginFrame = LabelFrame(root)
logoutFrame = LabelFrame(root)

##### Menu Navigation Buttons #####

homeButton = Button(menuFrame, text="Home", width=15, height=1, command=go_home)
glossaryButton = Button(menuFrame, text="Morph Glossary", width=15, height=1, command=go_glossary)
loginButton = Button(menuFrame, text="Log In", width=15, height=1, command=go_login)
collectionButton = Button(menuFrame, text="My Collection", width=15, height=1, command=go_collection)
logoutButton = Button(menuFrame, text="Log Out", width=15, height=1, command=go_logout)

##### Items for frames #####

# Items for calcFrame
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

# Items for glossary
title_glossary = Label(glossaryFrame, text="Morph List", font=('Arial', 20))

# Items for collection
title_collection = Label(collectionFrame, text="My Collection", font=('Arial', 20))
add_snake_title = Label(newSnakeFrame, text="Add a new snake:", font=('Arial', 12, 'italic'))
add_snake_name_label  = Label(newSnakeFrame, text="Name: ", anchor=E)
add_snake_name_entry = Entry(newSnakeFrame, width=35)
add_snake_morph_label = Label(newSnakeFrame, text="Add morphs: ", anchor=E)
add_snake_selected_morph_label = Label(newSnakeFrame, text="Selected morphs: ", anchor=E)
add_snake_selected_list_empty = Label(addSnakeSelectedMorphFrame, text="None selected", font=('Arial', 9, 'italic'))
add_snake_selected = StringVar()
add_snake_selected.set(morph_names[0])
add_snake_morph_menu = OptionMenu(newSnakeFrame, add_snake_selected, *morph_names)
add_snake_het_val = IntVar()
add_snake_het_val.set(0)
add_snake_het = Checkbutton(newSnakeFrame, text="Het", variable=add_snake_het_val)
add_snake_add_button = Button(newSnakeFrame, text="Add morph", command=lambda: store_morph(add_snake_selected.get(), add_snake_het_val.get()))
add_snake_save_button = Button(newSnakeFrame, text="Save this snake to your account", padx=10, pady=10, command=lambda: save_snake(add_snake_name_entry.get()))

# Items for login
title_login = Label(loginFrame, text="Log in to account: ")
username_entry = Label(loginFrame, text="Username: ")
un = Entry(loginFrame, width=20)
password_entry = Label(loginFrame, text="Password: ")
pw = Entry(loginFrame, show="*", width=20)
submit = Button(loginFrame, text="Submit", command=lambda: account_submit_login(un.get(), pw.get()))
create = Button(loginFrame, text="Create Account", command=lambda: account_create(un.get(), pw.get()))

# Items for logout
confirmation = Label(logoutFrame, text="You are currently logged in.")
title_logout = Label(logoutFrame, text="Log out of account?")
yes = Button(logoutFrame, text="Yes", command=account_logout)
no = Button(logoutFrame, text="No", command=go_home)


############################### Display GUI objects ###############################
#                                                                                 #
#             These commands display the GUI objects to the window.               #
#                                                                                 #
###################################################################################

# Menu Frame
menuFrame.grid(row=0, column=0)
homeButton.grid(row=0, column=0, pady=10)
glossaryButton.grid(row=0, column=1)
collectionButton.config(state=DISABLED)
collectionButton.grid(row=0, column=2)
loginButton.grid(row=0, column=3)

# Home/Calculator Frame
build_calc_frame()

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
# root.mainloop()