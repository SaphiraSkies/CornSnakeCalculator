#######################################################################################
# Corn Snake Morphs
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This file manages a list of morphs and necessary functions for
# a breeding calculator.
#######################################################################################

from os.path import exists

# This function is used to verify morph image links are working
def check_exists(path):
    return exists(path)

###########################
#                         #
#         Morphs          #
#                         #
###########################

# This class is for a snake morph. It has a name and is one of these types of inheritance:
# N = normal, R = recessive, I = incomplete dominant, D = dominant
# The het flag is for whether or not this morph is heterozygous on the animal.
# The default flag is for a normal, non-mutated animal.
class Morph:
    def __init__(self, name, inheritance, het=False, default=False, description=""):
        self.name = name
        self.inheritance = inheritance
        self.het = het
        self.default = default
        self.description = description
        self.imageLoc = "images/" + name + "-a.jpg"

    # Returns morph's name
    def getName(self):
        return self.name

    # Returns inheritance
    def getInheritance(self):
        return self.inheritance

    # Returns inheritance
    def getDescription(self):
        return self.description

    # Returns inheritance
    def getImageLoc(self):
        return self.imageLoc

# We need a list of all the morphs known by the program so
# that we can keep track of which are recessive/dominant/etc.
# This could at some point be automated using a csv file or similar.

# Wild types
normal = Morph("normal", 'N', False, False, "A standard corn snake, usually a brown or grey base, with red-brown and black patches.")
alabama = Morph("alabama", 'N', False, False, "Deep red patches with a brown or tan base. Reduced lateral pattern.")
keys = Morph("keys", 'N', False, False, "Lighter appearance with a tan base and orange patches. May have incomplete checkers on belly.")
miami = Morph("miami", 'N', False, False, "Silver base color with red or burnt-orange patches.")
okeetee = Morph("okeetee", 'N', False, False, "Deep red or burnt orange patches, a medium brown or deep orange base, and bold border patches.")

# A list of all wild type traits
wild_types = [normal, alabama, keys, miami, okeetee]

# Single recessive
amelanistic = Morph("amelanistic", 'R', False, False, "Lacking melanin (black pigment), low contrast, a yellow/orange/red snake with red eyes.")
anerythristic = Morph("anerythristic", 'R', False, False, "Lacking red/orange pigment, usually pale grey with black markings, may have a yellow stripe.")
caramel = Morph("caramel", 'R', False, False, "Yellow-brown base with caramel, light brown or rich chocolate patches.")
charcoal = Morph("charcoal", 'R', False, False, "Lacking red/orange pigment, usually pale grey with black markings, no yellow markings.")
christmas = Morph("christmas", 'R', False, False, "Reduced melanin (black), vibrant reds, whites, oranges and yellows, with deep reds.")
cinder = Morph("cinder", 'R', False, False, "Removes reds and oranges, leaving black, grey, and brown colorations.")
diffused = Morph("diffused", 'R', False, False, "Reduced side pattern and an uncheckered belly.")
dilute = Morph("dilute", 'R', False, False, "Reduced melanin (black), with a cooler shades of color.")
hypomelanistic = Morph("hypomelanistic", 'R', False, False, "Reduced melanin (black), vibrant combinations of light reds, whites, oranges and yellows, with an overall orange color.")
kastanie = Morph("kastanie", 'R', False, False, "Reduced reds and oranges, usually appears dark.")
lava = Morph("lava", 'R', False, False, "Reduced melanin (black), with a smoother pattern and a white belly stripe.")
lavender = Morph("lavender", 'R', False, False, "Removes most reds and oranges, reduces melanin (black), leaving shades of grey, light brown, pink, or orange.")
microscale = Morph("microscale", 'R', False, False, "")
motley = Morph("motley", 'R', False, False, "Elongates saddle patches and produces an uncheckered belly. Patches may be partially or fully connected, forming a stripe.")
red_coat = Morph("red coat", 'R', False, False, "Deep, vibrant reds.")
scaleless = Morph("scaleless", 'R', False, False, "Body has no scales, or very few.")
strawberry = Morph("strawberry", 'R', False, False, "Reduced melanin (black), vibrant reds, whites, oranges and yellows, with an overall red color.")
stripe = Morph("stripe", 'R', False, False, "Two dorsal stripes, two lateral stripes, and an uncheckered belly.")
sunkissed = Morph("sunkissed", 'R', False, False, "Reduced melanin (black) and smaller patches.")
sunrise = Morph("sunrise", 'R', False, False, "Reduced reds, may also be pale or very dark.")
terrazzo = Morph("terrazzo", 'R', False, False, "Striped or broken pattern with an uncheckered belly.")
ultra = Morph("ultra", 'R', False, False, "Reduced melanin (black), looks normal with lighter dark markings.")

# A list of all recessive traits
recessive = [amelanistic, anerythristic, caramel,
             charcoal, christmas, cinder, diffused,
             dilute, hypomelanistic, kastanie, lava,
             lavender, microscale, motley, red_coat,
             scaleless, strawberry, stripe,
             sunkissed, sunrise, terrazzo, ultra]

# Incomplete dominant traits
palmetto = Morph("palmetto", 'I', False, False, "A solid white base with scattered spots of color.")

# A list of all incomplete dominant traits
incDom = [palmetto]

# Dominant traits
buf = Morph("buf", 'D', False, False, "Reduced reds and oranges, similar to caramel but less extreme.")
masque = Morph("masque", 'D', False, False, "Reduced belly pattern, extended head pattern, and lightened overall colors.")
tessera = Morph("tessera", 'D', False, False, "Bold striped dorsal pattern with lateral patches. May have an uncheckered belly.")
toffee = Morph("toffee", 'D', False, False, "Light brown colors, similar to caramel, but with reduced colors.")

# A list of all dominant traits
dominant = [buf, masque, tessera, toffee]

# A list of all morphs
allMorphs = wild_types + recessive + incDom + dominant

###########################
#                         #
#  Some helper functions  #
#                         #
###########################

# Used to retrieve a list of morph (string) names from a list of morph objects
def getMorphNamesOnly(morphlist):
    list = []

    # Adds het and default prefixes when applicable
    for i in range(len(morphlist)):
        if morphlist[i].het == False:
            list.append(morphlist[i].name)
        elif morphlist[i].default == True:
            str = "def " + morphlist[i].name
            list.append(str)
        else:
            str = "het " + morphlist[i].name
            list.append(str)

    return list

# Used to print a list of morph names from a list of morph objects
# Second parameter is 0 for single line, 1 for each on new line, 2 for numbered new lines
def printMorphNames(morphlist, format):
    strH = "het "
    strD = "def "
    # Single line
    if format == 0:
        templist = []
        for i in range(len(morphlist)):
            if morphlist[i].het == True:
                templist.append(strH + morphlist[i].name)
            elif morphlist[i].default == True:
                templist.append(strD + morphlist[i].name)
            else:
                templist.append(morphlist[i].name)
        print(*templist, sep=', ')
    # New line
    elif format == 1:
        for i in range(len(morphlist)):
            if morphlist[i].het == True:
                print(f"{strH}{morphlist[i].name}")
            elif morphlist[i].default == True:
                print(f"{strD}{morphlist[i].name}")
            else:
                print(f"{morphlist[i].name}")
    # Numbered new lines
    elif format == 2:
        for i in range(len(morphlist)):
            if morphlist[i].het == True:
                print(f"{i + 1}. {strH}{morphlist[i].name}")
            elif morphlist[i].default == True:
                print(f"{i + 1}. {strD}{morphlist[i].name}")
            else:
                print(f"{i+1}. {morphlist[i].name}")
    else:
        print("Error in printMorphNames")

# Function for easily printing a list in preferred format.
# Format is 0 for single line, 1 for new line
def printList(list, format):
    if format == 0:
        print(*list, sep=', ')
    if format == 1:
        print(*list, sep='\n')

# Will retrieve a morph's inheritance by its name
def getInheritanceByName(str):
    for i in range(len(allMorphs)):
        if str == allMorphs[i].getName():
            return allMorphs[i].getInheritance()



########### Test code ###########

# for i in allMorphs:
#     print(f"Morph name: '{i.getName()}'")
#     print(f"Inheritance: {i.getInheritance()}")
#     print(f"Het: {i.het}")
#     print(f"Default: {i.default}")
#     print(f"Image location: {i.getImageLoc()}")
#     print(f"Image exists: {check_exists(i.getImageLoc())}")
#     print(f"Description: '{i.getDescription()}'\n")