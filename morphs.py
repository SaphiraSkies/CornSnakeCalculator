#######################################################################################
# Corn Snake Morphs
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This file manages a list of morphs and necessary functions for
# a breeding calculator.
#######################################################################################


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
    def __init__(self, name, inheritance, het=False, default=False):
        self.name = name
        self.inheritance = inheritance
        self.het = het
        self.default = default

    # Returns morph's name
    def getName(self):
        return self.name

    # Returns inheritance
    def getInheritance(self):
        return self.inheritance

# We need a list of all the morphs known by the program so
# that we can keep track of which are recessive/dominant/etc.
# This could at some point be automated using a csv file or similar.

# Wild types
normal = Morph("normal", 'N')
alabama = Morph("alabama", 'N')
keys = Morph("keys", 'N')
miami = Morph("miami", 'N')
okeetee = Morph("okeetee", 'N')

# A list of all wild type traits
wild_types = [normal, alabama, keys, miami, okeetee]

# Single recessive
amelanistic = Morph("amelanistic", 'R')
anerythristic = Morph("anerythristic", 'R')
caramel = Morph("caramel", 'R')
charcoal = Morph("charcoal", 'R')
christmas = Morph("christmas", 'R')
cinder = Morph("cinder", 'R')
diffused = Morph("diffused", 'R')
dilute = Morph("dilute", 'R')
hypomelanistic = Morph("hypomelanistic", 'R')
kastanie = Morph("kastanie", 'R')
lava = Morph("lava", 'R')
lavender = Morph("lavender", 'R')
microscale = Morph("microscale", 'R')
motley = Morph("motley", 'R')
red_coat = Morph("red coat", 'R')
scaleless = Morph("scaleless", 'R')
strawberry = Morph("strawberry", 'R')
stripe = Morph("stripe", 'R')
sunkissed = Morph("sunkissed", 'R')
sunrise = Morph("sunrise", 'R')
terrazzo = Morph("terrazzo", 'R')
ultra = Morph("ultra", 'R')

# A list of all recessive traits
recessive = [amelanistic, anerythristic, caramel,
             charcoal, christmas, cinder, diffused,
             dilute, hypomelanistic, kastanie, lava,
             lavender, microscale, motley, red_coat,
             scaleless, strawberry, stripe,
             sunkissed, sunrise, terrazzo, ultra]

# Incomplete dominant traits
palmetto = Morph("palmetto", 'I')

# A list of all incomplete dominant traits
incDom = [palmetto]

# Dominant traits
buf = Morph("buf", 'D')
masque = Morph("masque", 'D')
tessera = Morph("tessera", 'D')
toffee = Morph("toffee", 'D')

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

# Used to print a list of morph names, each on a new line
# Second parameter is 0 for single line, 1 for each on new line, 2 for numbered new lines
def printMorphNames(morphlist, format):
    strH = "het "
    strD = "def "
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
    elif format == 1:
        for i in range(len(morphlist)):
            if morphlist[i].het == True:
                print(f"{strH}{morphlist[i].name}")
            elif morphlist[i].default == True:
                print(f"{strD}{morphlist[i].name}")
            else:
                print(f"{morphlist[i].name}")
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



########### Test code ###########

# print("Wild types: ", end='')
# printMorphNames(wild_types, 0)
#
# print("\nI want to add amelanistic to a snake...")
# print(f"{amelanistic.getName().capitalize()} is an {amelanistic.getInheritance()} trait.")
#
# print("\nMorphs in a line...")
# printMorphNames(dominant, 0)
#
# print("\nMorphs on new lines...")
# printMorphNames(dominant, 1)
#
# print("\nMorphs numbered...")
# printMorphNames(dominant, 2)