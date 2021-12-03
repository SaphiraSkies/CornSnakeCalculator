#######################################################################################
# Corn Snake Breeding Calculator GUI
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This program runs the GUI for the Corn Snake Breeding Calculator.
#######################################################################################

from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from PIL import ImageTk,Image
import morphs
import morphcalc
import json
import socket

### Build the GUI base
root = Tk()
root.geometry("600x900")
root.title("Corn Snake Morph Calculator")
root.iconbitmap("favicon.ico")

### Need this for server connections
HEADER = 1024
PORT = 12345
FORMAT = 'utf-8'
SERVER = 'localhost'
ADDR = (SERVER, PORT)


# A list of all morph names (strings)
morph_names = morphs.getMorphNamesOnly(morphs.all_morphs)


# User-related variables
loggedIn = False            # tracks user login state
username = ""               # holds username info
user_snakes_dict = "[]"     # holds user's description (list of snakes as dicts), "[]" when empty
user_snakes_obj = []        # holds user's custom list of snakes as Snake objects


# These numbers are used for placement of morphs on the calculator page
p1_row = 5
p2_row = 5

# These are used for storing morph info for calculation
temp_p1_morphs = []
temp_p2_morphs = []
p1_item_list = []
p2_item_list = []

# These are used for storing morph info to add snakes to collection
temp_row = 0
temp_morphs = []
temp_labels = []
temp_buttons = []

# These are used for managing some frames in collection
p1_labels = []
p2_labels = []
snake_item_list = []


############################### Socket Connections ###############################
#                                                                                #
#     These functions are for communicating with an accounts microservice.       #
#                                                                                #
##################################################################################

# This is used for connecting to the user account server
# Returns 1 if there's an error connecting
def connectToServer():
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
def disconnectServer(conn):
    print("Client disconnected from server.")
    conn.close()


############################## Commands and Functions ###############################
#                                                                                   #
#                       These functions make the app work.                          #
#                                                                                   #
#####################################################################################

######## Menu Navigation Functions ########

# Navigate to home page (calculator)
def goHome():
    buildLoginFrame(0)

    glossaryFrame.grid_remove()
    collectionFrame.grid_remove()
    login_msg.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    calcFrame.grid(row=1, column=0)

# Navigate to glossary page
def goGlossary():
    buildLoginFrame(0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    collectionFrame.grid_remove()
    login_msg.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    glossaryFrame.grid(row=1, column=0)

# Navigate to collection page
def goCollection():
    buildLoginFrame(0)
    clearFrame(collectionFrame, 0)
    clearNewSnakeFrameEntry()
    buildNewSnakeFrame(0)

    global user_snakes_dict
    if user_snakes_dict != "[]":
        displayCollection()

    add_snake_selected.set(morph_names[0])
    add_snake_het_val.set(0)
    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    glossaryFrame.grid_remove()
    login_msg.grid_remove()
    loginFrame.grid_remove()
    logoutFrame.grid_remove()
    collectionFrame.grid(row=1, column=0)

# Navigate to login page
def goLogin():
    buildLoginFrame(0)
    buildNewSnakeFrame(0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    collectionFrame.grid_remove()
    glossaryFrame.grid_remove()
    logoutFrame.grid_remove()
    login_msg.grid(row=1, column=0)
    loginFrame.grid(row=2, column=0)

# Navigate to logout page
def goLogout():
    buildLoginFrame(0)

    calcFrame.grid_remove()
    resultsFrame.grid_remove()
    res_clear.grid_forget()
    collectionFrame.grid_remove()
    login_msg.grid_remove()
    loginFrame.grid_remove()
    glossaryFrame.grid_remove()
    logoutFrame.grid(row=1, column=0)


######## Home Calculator Functions ########

# Clears and builds the calculator frame
def buildCalcFrame():
    clearFrame(calcFrame, 0)

    title_home.grid(row=0, column=0, columnspan=3, pady=10, padx=5)
    help.grid(row=0, column=3)
    calcFrame.grid(row=1, column=0)
    p1_label.grid(row=1, column=0, columnspan=2)
    p1_morphs.grid(row=2, column=0)
    hetCheck1.grid(row=2, column=1)
    p2_label.grid(row=1, column=2, columnspan=2)
    p2_morphs.grid(row=2, column=2)
    hetCheck2.grid(row=2, column=3)
    add1.grid(row=3, column=0, columnspan=2, padx=20)
    add2.grid(row=3, column=2, columnspan=2, padx=20)
    calculate.grid(row=4, column=0, columnspan=4, padx=10, pady=20)

    global temp_p1_morphs
    global temp_p2_morphs

    if temp_p1_morphs:
        selectedMorphsFrame_p1.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        p1_clear.grid(row=0, column=0, pady=5, columnspan=2)
    if temp_p2_morphs:
        selectedMorphsFrame_p2.grid(row=5, column=2, columnspan=2, padx=10, pady=10)
        p2_clear.grid(row=0, column=0, pady=5, columnspan=2)

# Clears just the p1 or p2 morphs from the calculator
# Option = 1 for p1, option = 2 for p2
def clearCalcColumn(parent):
    global temp_p1_morphs
    global temp_p2_morphs
    global p1_item_list
    global p2_item_list

    if parent == 1:
        temp_p1_morphs.clear()
        p1_item_list.clear()
        selectedMorphsFrame_p1.grid_forget()
    elif parent == 2:
        temp_p2_morphs.clear()
        p2_item_list.clear()
        selectedMorphsFrame_p2.grid_forget()

    buildSelectedMorphsFrames()

# Adds a selected morph to parent 1 or 2
def addToCalculator(parent, selected_morph, het):
    morph_info = [selected_morph, het]

    # Store morph info
    if parent == 1:
        global temp_p1_morphs
        temp_p1_morphs.append(morph_info)
    elif parent == 2:
        global temp_p2_morphs
        temp_p2_morphs.append(morph_info)

    # Refresh selected morph frames
    buildSelectedMorphsFrames()

# Builds a frame that shows which morphs are selected for the calculator
# Parent is 1 for left column or 2 for right column
def buildSelectedMorphsFrames():
    clearFrame(selectedMorphsFrame_p1, 0)
    clearFrame(selectedMorphsFrame_p2, 0)

    global temp_p1_morphs
    global temp_p2_morphs
    global p1_item_list
    global p2_item_list

    # If there are any P1 morphs currently applied...
    if temp_p1_morphs:
        selectedMorphsFrame_p1.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        p1_clear.grid(row=0, column=0, pady=5, columnspan=2)

        # Make a label and deletion button for each one, then display it
        for i in range(len(temp_p1_morphs)):
            if temp_p1_morphs[i][1] == True:
                morph_label = Label(selectedMorphsFrame_p1, text="het " + temp_p1_morphs[i][0])
            else:
                morph_label = Label(selectedMorphsFrame_p1, text=temp_p1_morphs[i][0])
            morph_label.grid(row=i+1, column=0)

            delete_button = Button(selectedMorphsFrame_p1, text="X", command=lambda i=i: removeMorphFromCalc(1, i))
            delete_button.grid(row=i+1, column=1)

            items = [morph_label, delete_button]
            p1_item_list.append(items)

    # If there are any P1 morphs currently applied...
    if temp_p2_morphs:
        selectedMorphsFrame_p2.grid(row=5, column=2, columnspan=2, padx=10, pady=10)
        p2_clear.grid(row=0, column=0, pady=5, columnspan=2)

        # Make a label and deletion button for each one, then display it
        for i in range(len(temp_p2_morphs)):
            if temp_p2_morphs[i][1] == True:
                morph_label = Label(selectedMorphsFrame_p2, text="het " + temp_p2_morphs[i][0])
            else:
                morph_label = Label(selectedMorphsFrame_p2, text=temp_p2_morphs[i][0])
            morph_label.grid(row=i+1, column=0)
            p2_item_list.append(morph_label)

            delete_button = Button(selectedMorphsFrame_p2, text="X", command=lambda i=i: removeMorphFromCalc(2, i))
            delete_button.grid(row=i+1, column=1)
            p2_item_list.append(delete_button)

# Remove a morph from the calculator
# First arg is 1 or 2 for parent, and i is an item index in temp morph list
def removeMorphFromCalc(parent, i):
    global p1_item_list
    global p2_item_list
    global temp_p1_morphs
    global temp_p2_morphs

    if parent == 1:
        del temp_p1_morphs[i]

        # Adapt if the collection is now empty
        if not temp_p1_morphs:
            clearCalcColumn(1)
    elif parent == 2:
        del temp_p2_morphs[i]

        # Adapt if the collection is now empty
        if not temp_p2_morphs:
            clearCalcColumn(2)

    # Remove GUI objects
    clearFrame(selectedMorphsFrame_p1, 0)
    buildSelectedMorphsFrames()

# This clears the breeding results frame from the calc menu
def clearResults():
    clearFrame(resultsFrame, 1)
    resultsFrame.grid_forget()
    res_clear.grid_forget()

# Applies all selected morphs to snakes for calculation
def applyMorphsToSnakes():
    global temp_p1_morphs
    global temp_p2_morphs

    for m in temp_p1_morphs:
        morph_name = m[0]
        morph_inheritance = morphs.getInheritanceByName(morph_name)
        morph_het = m[1]

        morphcalc.p1.addMorph(morphs.Morph(morph_name, morph_inheritance, morph_het))

    for m in temp_p2_morphs:
        morph_name = m[0]
        morph_inheritance = morphs.getInheritanceByName(morph_name)
        morph_het = m[1]

        morphcalc.p2.addMorph(morphs.Morph(morph_name, morph_inheritance, morph_het))

# This function calculates and displays breeding results
def calculateResults():
    clearResults()

    global temp_p1_morphs
    global temp_p2_morphs

    if temp_p1_morphs and temp_p2_morphs:
        applyMorphsToSnakes()

        results = morphcalc.run(morphcalc.p1, morphcalc.p2)

        res_clear.grid(row=2, column=0, padx=10, pady=10)
        resultsLabel = Label(resultsFrame, text=results)
        resultsLabel.pack()
        resultsFrame.grid(row=4, column=0)

        morphcalc.p1.clearData()
        morphcalc.p2.clearData()
    else:
        clearResults()
        messagebox.showwarning("Error", "You must enter at least one morph for each parent before calculation.")

# Offers information to the user about calculation
def helpWithCalc():
    help_msg = "How to use the Morph Calculator\n\n" \
               "1. Select a morph from the dropdown menu for each parent snake. Use the checkbox " \
               "to indicate whether the morph is het (heterozygous) or not.\n\nNote: A 'het' morph may or may not have a " \
               "visible appearance, depending on the gene's type of inheritance.\n\n" \
               "2. Select each morph for each parent. Morphs can be cleared or removed individually from the menu." \
               "\n\n3. Press 'Calculate Results'" \
               "\n\n4. Breeding results will be displayed below. These are listed by the percentage chance " \
               "of appearance in a clutch.\n\nKeep in mind that there are no guarantees that you will get any" \
               " of the given results if it is less than 100%!"
    messagebox.showinfo(title="Information on Calculations", message=help_msg)


######## Glossary Functions ########

# This is used for constructing a scrollbox within the Glossary frame
# Code adapted from:
# https://bytes.com/topic/python/answers/157174-how-get-scrollregion-adjust-w-window-size
def buildGlossaryScrollframe():
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
    for i in morphs.all_morphs:
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
def buildNewSnakeFrame(error, str=""):
    warning = Label(newSnakeFrame, text="Error: " + str, fg="red")
    global user_snakes_dict

    # If there's no error, build the standard newSnakeFrame frame:
    if error == 0:
        clearFrame(userSnakesFrame, 0)
        clearFrame(newSnakeFrame, 0)
        displayCollection()
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
        clearFrame(userSnakesFrame, 0)
        clearFrame(newSnakeFrame, 0)
        displayCollection()
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
def storeMorph(name, het):
    global temp_morphs
    global temp_labels
    global temp_buttons
    global temp_row

    buildNewSnakeFrame(0)

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
    remove_morph_button = Button(addSnakeSelectedMorphFrame, text="X Remove", font=('Arial', 8), command=lambda: removeStoredMorph(current_index))
    remove_morph_button.grid(row=temp_row, column=2)
    temp_buttons.insert(current_index, remove_morph_button)

    # Increment current row for display
    temp_row = temp_row + 1

# This function removes stored morphs while selecting to save a new snake
def removeStoredMorph(index):
    global temp_morphs
    global temp_labels
    global temp_buttons
    global temp_row

    # Remove morph at index
    temp_morphs[index] = "none"
    temp_labels[index].grid_forget()
    temp_buttons[index].grid_forget()

    if morphsIsEmpty():
        add_snake_selected_list_empty.grid(row=0, column=0)

# This removes existing data from stored morphs and resets the frame
def clearStoredMorphs():
    global temp_row
    global temp_morphs
    global temp_labels
    global temp_buttons
    temp_row = 0
    temp_morphs.clear()
    temp_labels.clear()
    temp_buttons.clear()
    clearFrame(addSnakeSelectedMorphFrame, 0)
    add_snake_selected_list_empty.grid(row=0, column=0)

# Saves the selected snake to the user's account
def saveSnake(name):
    global user_snakes_dict

    global temp_morphs

    # Either give an error or proceed
    if morphsIsEmpty():
        buildNewSnakeFrame(1, "You must select at least one morph.")
    else:
        buildNewSnakeFrame(0)
        userSnakesFrame.pack()

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

        if user_snakes_dict == "[]":
            user_snakes_dict = []

        # Save this snake to the user's account
        user_snakes_dict.append(snake)
        descriptionToSnakes()
        accountEdit(user_snakes_dict)
        displayCollection()
        clearNewSnakeFrameEntry()

# Deletes a snake from the user's account
def deleteSnake(snake):
    global user_snakes_dict
    global user_snakes_obj

    msg = "Are you sure you'd like to remove this snake? This action is irreversible."
    answer = askyesno(title="Confirm deletion", message=msg)

    if answer:
        # Look for the item in user_names_dict and remove it
        for i in range(len(user_snakes_dict)):
            if user_snakes_dict[i] == snake:
                user_snakes_dict.pop(i)
                break

        # Look for the item in user_names_obj and remove it
        for i in range(len(user_snakes_dict)):
            name = user_snakes_obj[i].getName()
            morph_list = user_snakes_obj[i].getMorphNameList()
            if name == snake["name"]:
                if morph_list == snake["morphs"]:
                    user_snakes_obj.pop(i)
                    break

        # Adapt if the collection is now empty
        if not user_snakes_dict:
            user_snakes_dict = "[]"
            userSnakesFrame.pack_forget()

        # Update user description
        accountEdit(user_snakes_dict)

        # Remove GUI objects
        clearFrame(userSnakesFrame, 0)
        displayCollection()

# This function tells you whether or not the temp_morph list is empty
# Returns True if empty, False if not
def morphsIsEmpty():
    global temp_morphs

    no_morphs_found = True

    # If the list isn't empty, check for any index that is not "none"
    if temp_morphs:
        for item in temp_morphs:
            if item != "none":
                no_morphs_found = False

    return no_morphs_found

# This is for clearing saved snake fields
def clearNewSnakeFrameEntry():
    add_snake_name_entry.delete(0, END)
    clearStoredMorphs()

# This function will remove all of a user's snakes in collection
def deleteCollection():
    global user_snakes_dict

    msg = "Are you sure you'd like to remove all snakes from your collection? This action is irreversible."
    answer = askyesno(title="Confirm deletion", message=msg)
    if answer:

        user_snakes_obj.clear()
        if user_snakes_dict != "[]":
            user_snakes_dict.clear()
        user_snakes_dict = "[]"
        accountEdit("[]")
        clearFrame(userSnakesFrame, 0)
        userSnakesFrame.pack_forget()

# This adds a snake from the user's collection to the morph calculator
# Parent variable is 1 for p1 (parent #1) or 2 for p2 (parent #2)
def addFromCollection(snake, parent):
    clearCalcColumn(parent)

    snake_morphs = snake["morphs"].copy()

    # Read "het" as its own separate value from the list of morphs
    for i in range(len(snake_morphs)):
        het = False
        if "het " in snake_morphs[i]:
            snake_morphs[i] = snake_morphs[i][4:]
            het = True

        if parent == 1:
            addToCalculator(1, snake_morphs[i], het)
        elif parent == 2:
            addToCalculator(2, snake_morphs[i], het)

    # Go to calculator
    goHome()

# This function displays all the user's snakes on the collection frame
def displayCollection():
    global user_snakes_dict

    row = 0
    col = 0

    if user_snakes_dict != "[]":
        nuke_button = Button(userSnakesFrame, text="Delete All", padx=10, pady=10, command=deleteCollection)
        nuke_button.grid(row=row, column=col, padx=10, pady=10, columnspan=4)

        userSnakesRow = 1
        userSnakesCol = -1

        global snake_item_list

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
            add_to_p1_button = Button(snakeFrame, text="Select as\nParent 1", command=lambda i=i: addFromCollection(user_snakes_dict[i], 1))
            add_to_p1_button.grid(row=snakeFrameRow, column=snakeFrameCol, padx=5)

            # Button to add this snake to p2 on the calculator
            snakeFrameCol = snakeFrameCol + 1
            add_to_p2_button = Button(snakeFrame, text="Select as\nParent 2", command=lambda i=i: addFromCollection(user_snakes_dict[i], 2))
            add_to_p2_button.grid(row=snakeFrameRow, column=snakeFrameCol, padx=5)

            # Button for deleting this snake
            snakeFrameRow = snakeFrameRow + 1
            snakeFrameCol = snakeFrameCol - 1
            delete_snake_button = Button(snakeFrame, text="Delete this Snake", command=lambda i=i: deleteSnake(user_snakes_dict[i]), padx=10)
            delete_snake_button.grid(row=snakeFrameRow, column=snakeFrameCol, columnspan=2, padx=5, pady=5)

            # Wrap grid position
            if userSnakesCol < 2:
                userSnakesCol = userSnakesCol + 1
            else:
                userSnakesCol = 0
                userSnakesRow = userSnakesRow + 1

            snakeFrame.grid(row=userSnakesRow, column=userSnakesCol, padx=10, pady=10)

            snake_item_list.append(snakeFrame)
            snake_item_list.append(snakeName)
            snake_item_list.append(delete_snake_button)

# This clears ALL of a user's snakes from the collection frame
def clearUserSnakes():
    global snake_item_list
    for x in snake_item_list:
        x.grid_forget()
    userSnakesFrame.pack_forget()



######## Login Page Functions ########

# This builds the frame within the login page, with an option to display errors
def buildLoginFrame(error, str=""):
    warning = Label(loginFrame, text="Error: " + str, fg="red")
    clearLoginEntry()

    # If there's no error, build the standard login frame:
    if error == 0:
        clearFrame(loginFrame, 0)
        title_login.grid(row=0, column=0, columnspan=2)
        username_entry.grid(row=1, column=0)
        un.grid(row=1, column=1)
        password_entry.grid(row=2, column=0)
        pw.grid(row=2, column=1)
        submit.grid(row=3, column=0)
        create.grid(row=3, column=1)
    # Builds the frame with an error message from str parameter
    elif error == 1:
        clearFrame(loginFrame, 0)
        warning.grid(row=0, column=0, columnspan=2)
        title_login.grid(row=1, column=0, columnspan=2)
        username_entry.grid(row=2, column=0)
        un.grid(row=2, column=1)
        password_entry.grid(row=3, column=0)
        pw.grid(row=3, column=1)
        submit.grid(row=4, column=0)
        create.grid(row=4, column=1)

# This is for clearing login username/password fields
def clearLoginEntry():
    un.delete(0, END)
    pw.delete(0, END)

# Adjusts the login page after user logs in
def login():
    clearLoginEntry()
    login_msg.grid_remove()
    buildNewSnakeFrame(0)

    global user_snakes_dict
    if user_snakes_dict != "[]":
        displayCollection()

    loggedIn = True

    collectionButton.config(state=NORMAL)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid(row=0, column=3)
    logoutFrame.grid(row=1, column=0)
    loginButton.grid_remove()
    loginFrame.grid_remove()

# Adjusts the login page after user logs out
def logout():
    clearLoginEntry()
    clearFrame(collectionFrame, 0)
    clearUserSnakes()

    loggedIn = False
    buildLoginFrame(0)
    buildNewSnakeFrame(0)

    collectionButton.config(state=DISABLED)
    collectionButton.grid(row=0, column=2)
    logoutButton.grid_remove()
    logoutFrame.grid_remove()
    loginButton.grid(row=0, column=3)
    login_msg.grid(row=1, column=0)
    loginFrame.grid(row=2, column=0)


######## Login Server Functions ########

# This function attempts to create an account with username and password
def accountCreate(user, pw):
    client = connectToServer()

    # If server connection is valid...
    if client != 1:
        # Prevents empty user info
        if user == "":
            buildLoginFrame(1, "Username required.")
        elif pw == "":
            buildLoginFrame(1, "Password required.")
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
                buildLoginFrame(1, response["1"])
            # Creation successful
            elif "0" in response:
                print(f"Account created: {user}")
                global username
                username = user
                login()

        disconnectServer(client)

    # Server ran into an error...
    else:
        buildLoginFrame(1, "Could not connect to server.")

# This function attempts to log in with username and password
def accountSubmitLogin(user, pw):
    client = connectToServer()

    # If server connection is valid...
    if client != 1:
        # Prevents empty user info
        if user == "":
            buildLoginFrame(1, "Username required.")
        elif pw == "":
            buildLoginFrame(1, "Password required.")
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
                buildLoginFrame(1, "Username does not exist.")
            # Handles incorrect password error
            elif "2" in response:
                response = json.loads(response)
                buildLoginFrame(1, response["2"])
            # Creation successful
            elif "0" in response:
                print(f"Account logged in: {user}")
                global username
                global user_snakes_dict
                username = user
                user_snakes_dict = accountRetrieveDescription()
                descriptionToSnakes()
                login()

        disconnectServer(client)
    # Server ran into an error...
    else:
        buildLoginFrame(1, "Could not connect to server.")

# This function attempts to log out of a user's account
def accountLogout():
    client = connectToServer()

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

            clearStoredMorphs()

            print(f"Account logged out: {username}")
            username = ""
            if user_snakes_dict != "[]":
                user_snakes_dict.clear()
            user_snakes_dict = "[]"
            if user_snakes_obj:
                user_snakes_obj.clear()
            logout()

        disconnectServer(client)
    # Server ran into an error...
    else:
        messagebox.showwarning("Error", "Could not connect to server.")

# This function attempts to update the user's description.
# This is used to save snakes to the account.
def accountEdit(description):
    client = connectToServer()

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
            print(f"Updated description for {username}")

        disconnectServer(client)
    # Server ran into an error...
    else:
        messagebox.showwarning("Error", "Could not connect to server.")

# This function retrieve's a user's account information.
# It can also be used to return a user's description info.
def accountRetrieveDescription():
    client = connectToServer()

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
            disconnectServer(client)
            return response["description"]

        disconnectServer(client)
    # Server ran into an error...
    else:
        messagebox.showwarning("Error", "Could not connect to server.")


######## Other Helper Functions ########

# This can be used to clear a frame, 0 for forget, 1 for detroy
def clearFrame(frame, setting):
    if setting == 0:
        for widgets in frame.winfo_children():
            widgets.grid_forget()
    if setting == 1:
        for widgets in frame.winfo_children():
            widgets.destroy()

# This function converts the user's description to a list of snakes
def descriptionToSnakes():
    global user_snakes_dict
    global user_snakes_obj

    # Cancel operation if there are no snakes for this user
    if user_snakes_dict == "[]":
        return

    # Scrap existing list
    user_snakes_obj.clear()

    # Generate new one
    for x in user_snakes_dict:
        dictToSnake(x)

# This takes a dict, creates a snake object from it, and adds it to the user's list
# Option is 0 to process the snake straight to the user_snakes_obj list
# Option 1 will return the snake as an object
def dictToSnake(dict, option=0):
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
selectedMorphsFrame_p1 = LabelFrame(calcFrame, text="Parent 1")
selectedMorphsFrame_p2 = LabelFrame(calcFrame, text="Parent 2")
resultsFrame = LabelFrame(root, text="Results", font=('Arial', 14))
glossaryFrame = LabelFrame(root)
collectionFrame = LabelFrame(root)
newSnakeFrame = LabelFrame(collectionFrame)
userSnakesFrame = LabelFrame(collectionFrame)
addSnakeSelectedMorphFrame = LabelFrame(newSnakeFrame)
loginFrame = LabelFrame(root)
logoutFrame = LabelFrame(root)

##### Menu Navigation Buttons #####

homeButton = Button(menuFrame, text="Home", width=15, height=1, command=goHome)
glossaryButton = Button(menuFrame, text="Morph Glossary", width=15, height=1, command=goGlossary)
loginButton = Button(menuFrame, text="Log In", width=15, height=1, command=goLogin)
collectionButton = Button(menuFrame, text="My Collection", width=15, height=1, command=goCollection)
logoutButton = Button(menuFrame, text="Log Out", width=15, height=1, command=goLogout)

##### Items for frames #####

# Items for calcFrame
title_home = Label(calcFrame, text="Morph Calculator", font=('Arial', 20))
image = Image.open('question.png')
image = image.resize((20, 20), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(image)
help = Button(calcFrame, image=my_img, command=helpWithCalc)
p1_label = Label(calcFrame, text="Select morphs\nfor parent 1:")
p2_label = Label(calcFrame, text="Select morphs\nfor parent 2:")
selected1 = StringVar()
selected1.set(morph_names[0])
het1 = IntVar()
hetCheck1 = Checkbutton(calcFrame, text="Het", variable=het1)
p1_morphs = OptionMenu(calcFrame, selected1, *morph_names)
add1 = Button(calcFrame, text="Add", padx=40, command=lambda: addToCalculator(1, selected1.get(), het1.get()))
selected2 = StringVar()
selected2.set(morph_names[0])
p2_morphs = OptionMenu(calcFrame, selected2, *morph_names)
add2 = Button(calcFrame, text="Add", padx=40, command=lambda: addToCalculator(2, selected2.get(), het2.get()))
het2 = IntVar()
hetCheck2 = Checkbutton(calcFrame, text="Het", variable=het2)
calculate = Button(calcFrame, text="Calculate Results", padx=40, pady=10, command=calculateResults)
p1_clear = Button(selectedMorphsFrame_p1, text="Clear", padx=15, command=lambda: clearCalcColumn(1))
p2_clear = Button(selectedMorphsFrame_p2, text="Clear", padx=15, command=lambda: clearCalcColumn(2))
res_clear = Button(root, text="Clear results", command=clearResults)

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
add_snake_add_button = Button(newSnakeFrame, text="Add morph", command=lambda: storeMorph(add_snake_selected.get(), add_snake_het_val.get()))
add_snake_save_button = Button(newSnakeFrame, text="Save this snake to your account", padx=10, pady=10, command=lambda: saveSnake(add_snake_name_entry.get()))

# Items for login
login_msg = Label(root, text="Create an account to save multiple snakes from your collection for easy calculation.", padx=10, pady=10)
title_login = Label(loginFrame, text="Log in to account: ")
username_entry = Label(loginFrame, text="Username: ")
un = Entry(loginFrame, width=20)
password_entry = Label(loginFrame, text="Password: ")
pw = Entry(loginFrame, show="*", width=20)
submit = Button(loginFrame, text="Submit", command=lambda: accountSubmitLogin(un.get(), pw.get()))
create = Button(loginFrame, text="Create Account", command=lambda: accountCreate(un.get(), pw.get()))

# Items for logout
confirmation = Label(logoutFrame, text="You are currently logged in.")
title_logout = Label(logoutFrame, text="Log out of account?")
yes = Button(logoutFrame, text="Yes", command=accountLogout)
no = Button(logoutFrame, text="No", command=goHome)


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
buildCalcFrame()

# Glossary frame
title_glossary.grid(row=0, column=0)
buildGlossaryScrollframe()

# Collection frame
title_collection.pack()
newSnakeFrame.pack()
buildNewSnakeFrame(0)

# Login frame
buildLoginFrame(0)

# Logout frame
confirmation.grid(row=0, column=0, columnspan=2)
title_logout.grid(row=1, column=0, columnspan=2)
yes.grid(row=2, column=0)
no.grid(row=2, column=1)

### This runs the GUI
root.mainloop()