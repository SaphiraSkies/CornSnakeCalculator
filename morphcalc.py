#######################################################################################
# Corn Snake Breeding Calculator
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This program will take two parent snakes with known morphs and calculate
# the possible breeding results based on that information.
#######################################################################################

import morphs
import punnettcalc


###########################################################################
# The Snake class contains information needed for an instance of a snake. #
###########################################################################
class Snake:
    # Initialize the snake with a name ("NULL" is the default for no name)
    def __init__(self, name='NULL'):
        self.name = name
        self.morphs = []

    # Returns snake's name
    def getName(self):
        return self.name

    # Sets snake's name
    def setName(self, name):
        self.name = name

    # Add a morph to this snake (input a new instance of a morph)
    def addMorph(self, morph):
        self.morphs.append(morph)

    # Remove a morph from this snake
    def removeMorph(self, morph):
        self.morphs.remove(morph)

    # Returns a string of all morph names on this snake, separated by commas
    def getMorphList(self):
        return morphs.getMorphNamesOnly(self.morphs)

    # Clears all data from this snake
    def clearData(self):
        self.name = "NULL"
        self.morphs.clear()

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
            choice = ""
            het = False
            while choice not in ["y", "Y", "n", "N"]:
                choice = input("Is this a het morph? (Y/N) ")
                if choice == "Y" or choice == "y":
                    het = True
                elif choice == "N" or choice == "n":
                    het = False
                else:
                    print("Invalid input. Please enter Y for yes or N for no.")

            # Create morph instance for this snake
            name = morphs.allMorphs[int(m) - 1].getName()
            inherit = morphs.allMorphs[int(m) - 1].getInheritance()

            snake.addMorph(morphs.Morph(name, inherit, het, False))

            print(f"Added morph: ", end='')
            if het == True:
                print("het ", end='')
            print(f"{snake.morphs[-1].getName()}")
            validInput = True

            # Loops for additional morphs
            choice = ""
            while choice not in ["y", "Y", "n", "N"]:
                choice = input("Would you like to add another morph to this snake? (Y/N) ")
                if choice == "Y" or choice == "y":
                    validInput = False
                elif choice == "N" or choice == "n":
                    validInput = True
                else:
                    print("Invalid input. Please enter Y for yes or N for no.")


# This is used for incrementing a character by one. Reference:
# https://www.geeksforgeeks.org/ways-increment-character-python/
def incChar(ch):
    temp = chr(ord(ch) + 1)
    return temp


# This function translates a list of morphs into allele characters for a Punnett Square
def getAlleles(morphlist):
    alleles = []
    char = 'A'

    for x in morphlist:
        # Normal traits are always inherited
        if x.inheritance == 'N':
            alleles.append("##")
        # Other traits are AA if normal (non-mutated), Aa if het, and aa if fully mutated
        else:
            if x.het == True:
                alleles.append(char.upper() + char.lower())
            elif x.default == True:
                alleles.append(char.upper() + char.upper())
            else:
                alleles.append(char.lower() + char.lower())

        char = incChar(char)

    return alleles


# This function handles the calculations for breeding results
def breedResults(p1, p2):

    # Make a copy of each parents' morph lists
    morphs_p1 = p1.morphs.copy()
    morphs_p2 = p2.morphs.copy()

    tempList1 = []      # These lists will contain matched morphs
    tempList2 = []
    matched = []        # Used for keeping track of which morphs are already matched

    # Look at each morph, determine if the same trait is in the other parent
    for i in morphs_p1:
        matchFound = False

        for j in morphs_p2:
            # If this trait is in both snakes, move those traits over to the temp list
            if i.name == j.name:
                matchFound = True
                tempList1.append(i)
                tempList2.append(j)

        # If the second snake does not have this trait, add it, but as "default" (a non-mutated allele)
        if matchFound == False:
            tempMorph = morphs.Morph(i.name, i.inheritance, False, True)

            tempList1.append(i)
            tempList2.append(tempMorph)

        matched.append(i.name)

    # Look at the remaining traits in the second parent the same way
    for j in morphs_p2:
        if j.name not in matched:
            matchFound = False

            for i in morphs_p1:
                # If this trait is in both snakes, move those traits over to the temp list
                if i.name == j.name:
                    matchFound = True
                    tempList1.append(i)
                    tempList2.append(j)

            # If the second snake does not have this trait, add it, but as "default" (a non-mutated allele)
            if matchFound == False:
                tempMorph = morphs.Morph(j.name, j.inheritance, False, True)

                tempList1.append(tempMorph)
                tempList2.append(j)

            matched.append(j.name)

    # Now we have two comparable lists...
    # We want to convert the morph names into allele characters
    # that can be used in a Punnett Square
    p1_alleles = "".join(getAlleles(tempList1))
    p2_alleles = "".join(getAlleles(tempList2))

    # We need a list to keep track of the results for each morph combination.
    # Each morph has a possibility of being normal, het, or fully mutated -
    # these are the three numbers in "count"
    numOffspring = []
    norm = 0
    het = 0
    mut = 0
    for n in range(len(tempList1)):
        count = [norm, het, mut]
        numOffspring.append(count)

    # print("NumOffspring: ", end='')
    # for e in range(len(numOffspring)):
    #     print(f"{numOffspring[e][0]}, {numOffspring[e][1]}, {numOffspring[e][2]}")

    # Run the Punnet Square calculation
    results = punnettcalc.punnett(p1_alleles, p2_alleles)
    # morphs.printList(results, 0)


    # Now we have...
    # tempList1     tempList2       p1_alleles      p2_alleles      numOffspring
    # --------------------------------------------------------------------------
    # morph1        morph1          Aa              AA              [0, 1, 2]
    # morph2        morph2          bb              Bb              [0, 0, 0]
    #
    # And we have RESULTS with all breeding results


    # print("NumOffspring START: ")
    # for e in range(len(numOffspring)):
    #     print(f"{numOffspring[e][0]}, {numOffspring[e][1]}, {numOffspring[e][2]}")

    index = 0

    # Count the results
    # For each allele pair...
    for i in range(len(p1_alleles)):

        # Only look at every other character (each pair of two)
        try:
            curChar = p1_alleles[index][0]
        except:
            break

        normChar = curChar.upper() + curChar.upper()
        hetChar1 = curChar.upper() + curChar.lower()    # The two het versions account for
        hetChar2 = curChar.lower() + curChar.upper()    # Aa and aA combinations
        fullChar = curChar.lower() + curChar.lower()

        for combo in results:
            # Count normal
            if normChar in combo:
                numOffspring[i][0] += 1
            # Count het
            elif hetChar1 in combo or hetChar2 in combo:
                numOffspring[i][1] += 1
            # Count fully mutated
            elif fullChar in combo:
                numOffspring[i][2] += 1

        index = index + 2

    # Translate results into concise output
    total_results = len(results)

    results = ""

    for i in range(len(morphs_p1)):
        numNormal = (numOffspring[i][0] / total_results) * 100
        numHet = (numOffspring[i][1] / total_results) * 100
        numFull = (numOffspring[i][2] / total_results) * 100

        if morphs_p1[i].inheritance == 'N':
            results = results + "\n" + morphs_p1[i].name.capitalize() + ": 100% " + morphs_p1[i].name
        else:
            results = results + "\n" + morphs_p1[i].name.capitalize() + ": " + str(numNormal) + "% normal, "
            results = results + str(numHet) + "% het " + morphs_p1[i].name + ", " + str(numFull) + "% " + morphs_p1[i].name

    # for i in range(len(morphs_p1)):
    #     numNormal = (numOffspring[i][0] / total_results) * 100
    #     numHet = (numOffspring[i][1] / total_results) * 100
    #     numFull = (numOffspring[i][2] / total_results) * 100
    #
    #     if morphs_p1[i].inheritance == 'N':
    #         print(f"{morphs_p1[i].name.capitalize()}: 100% {morphs_p1[i].name}")
    #     else:
    #         print(f"{morphs_p1[i].name.capitalize()}: {numNormal}% normal, "
    #               f"{numHet}% het {morphs_p1[i].name}, {numFull}% {morphs_p1[i].name}")

    return results




running = False

p1 = Snake()
p2 = Snake()

# For testing
# p1.addMorph(morphs.Morph("caramel", 'R', True))
# p1.addMorph(morphs.Morph("okeetee", 'N'))
# p1.addMorph(morphs.Morph("hypomelanistic", 'R'))
# p2.addMorph(morphs.Morph("tessera", 'D'))
# p2.addMorph(morphs.Morph("caramel", 'R'))

# print("*******************************************************************")
# print("Welcome to the breeding calculator. Please use the menu to proceed.")
# print("*******************************************************************")

###### Menu ######
while running:
    print("\n---- Current parent snakes ----")
    print("Parent 1:")
    if p1.getName() == "NULL":
        if p1.morphs:
            morphs.printList(p1.getMorphList(), 0)
        else:
            print("None selected")
    else:
        print(f"{p1.getName()} - ", end='')
        morphs.printList(p1.getMorphList(), 0)
    print("\nParent 2:")
    if p2.getName() == "NULL":
        if p2.morphs:
            morphs.printList(p2.getMorphList(), 0)
        else:
            print("None selected")
    else:
        print(f"{p2.getName()} - ", end='')
        morphs.printList(p2.getMorphList(), 0)

    print("\n1. Select parent #1 snake")
    print("2. Select parent #2 snake")
    print("3. Clear parent snakes")
    print("4. Calculate breeding results")
    print("5. Create account")
    print("6. View morphs")
    print("7. Quit\n")

    response = 0
    while response not in ["1", "2", "3", "4", "5", "6", "7"]:
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
            breedResults(p1, p2)
        elif response == "5":
            print("Selected 5")
            print("[Prompts to create user account go here]")
        elif response == "6":
            for i in morphs.allMorphs:
                print("[Image of the morph goes here]")
                print(f"{i.name.capitalize()}\n")
        elif response == "7":
            print("Selected 7. Quitting...")
            running = False
        else:
            print("Invalid entry. Please choose 1, 2, 3, 4, 5, 6, or 7.")