#######################################################################################
# Corn Snake Breeding Calculator
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This program will take two parent snakes with known morphs and calculate
# the possible breeding results based on that information.
#######################################################################################

import morphs
from morphs import Morph
from morphs import Locus
import punnettcalc


###########################################################################
# The Snake class contains information needed for an instance of a snake. #
###########################################################################
class Snake:
    # Initialize the snake with a name ("NULL" is the default for no name)
    def __init__(self, name='NULL'):
        self.name = name
        self.morphs = []
        self.loc = Locus()

    # Returns snake's name
    def getName(self):
        return self.name

    # Sets snake's name
    def setName(self, name):
        self.name = name

    # Add a morph to this snake
    def addMorph(self, morph):
        self.morphs.append(morph)
        self.loc.setType(morph.getName())

    # Remove a morph from this snake
    def removeMorph(self, morph):
        self.morphs.remove(morph)

    # Returns a string of all morphs on this snake, separated by commas
    def getMorphList(self):
        return morphs.getMorphNamesOnly(self.morphs)

    # Clears all data from this snake
    def clearData(self):
        self.name = "NULL"
        self.morphs.clear()
        self.loc.clearAllLocus()

# Adds a new snake. Any existing data for this snake will be overwritten.
def selectSnake(snake):
    snake.clearData()

    # Set snake's name
    n = input("Choose a name: ")
    snake.setName(n)
    print(f"Name set to: '{n}'\n")

    # Print menu of morphs to be selected
    morphs.printMorphNames(morphs.allMorphs, 2)
    print("")

    validInput = False

    # Loops for morph choices
    while validInput == False:
        m = input("Choose a morph for this snake by typing the number: ")
        if int(m) < 0 or int(m) > len(morphs.allMorphs):
            print("Invalid input. Please enter the number next to the morph you want to add.")
        else:
            print(f"Added morph: {morphs.allMorphs[int(m) - 1].getName()}")
            snake.addMorph(morphs.allMorphs[int(m) - 1])
            validInput = True

            # Loops for additional morphs
            choice = ""
            while choice not in ["y", "Y", "n", "N"]:
                choice = input("Would you like to add another morph to this snake? (Y/N) ")
                if choice == "Y" or choice == "y":
                    validInput = False
                elif choice == "N" or choice == "n":
                    validInput = True
                    pass
                else:
                    print("Invalid input. Please enter Y for yes or N for no.")

# This function handles the calculations for breeding results
def breedResults(p1, p2):
    p1_alleles = ""
    p2_alleles = ""
    
    for x in p1.loc.getActiveLocus():
        print(f"Looking for {p1.loc.getActiveLocus()} in p2...")
        if x in p2.loc.getActiveLocus():
            pass
        else:
            p2.loc.




running = True

p1 = Snake()
p2 = Snake()

print("*******************************************************************")
print("Welcome to the breeding calculator. Please use the menu to proceed.")
print("*******************************************************************")

# Menu
while running:
    print("\n---- Current parent snakes ----")
    print("Parent 1:")
    if p1.getName() == "NULL":
        if p1.loc.getActiveLocus()[0] == "none":
            print("None selected")
        else:
            morphs.printList(p1.getMorphList(), 0)
    else:
        print(f"{p1.getName()} - ", end='')
        morphs.printList(p1.getMorphList(), 0)
    print("\nParent 2:")
    if p2.getName() == "NULL":
        if p2.loc.getActiveLocus()[0] == "none":
            print("None selected")
        else:
            morphs.printList(p2.getMorphList(), 0)
    else:
        print(f"{p2.getName()} - ", end='')
        morphs.printList(p2.getMorphList(), 0)

    print("\n1. Select parent #1 snake")
    print("2. Select parent #2 snake")
    print("3. Clear parent snakes")
    print("4. Calculate breeding results")
    print("5. Quit\n")

    response = 0
    while response not in ["1", "2", "3", "4", "5"]:
        response = input("Select an option: ")
        if response == "1":
            print("Selected 1.")
            selectSnake(p1)
        elif response == "2":
            print("Selected 2.")
            selectSnake(p2)
        elif response == "3":
            print("Selected 3. Clearing selected snakes.")
            p1.clearData()
            p2.clearData()
        elif response == "4":
            print("Selected 4")
            print("Parent 1 active locus: ", end='')
            morphs.printList(p1.loc.getActiveLocus(), 0)
            print("Parent 2 active locus: ", end='')
            morphs.printList(p2.loc.getActiveLocus(), 0)
        elif response == "5":
            print("Selected 5. Quitting...")
            running = False
        else:
            print("Invalid entry. Please choose 1, 2, 3, 4, or 5.")