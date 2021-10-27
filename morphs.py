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
class Morph:
    def __init__(self, name, inheritance):
        self.name = name
        self.inheritance = inheritance

    # Returns morph's name
    def getName(self):
        return self.name

    # Returns inheritance
    def getInheritance(self):
        return self.inheritance

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
        list.append(morphlist[i].name)

    return list

# Used to print a list of morph names, each on a new line
# Second parameter is 0 for single line, 1 for each on new line, 2 for numbered new lines
def printMorphNames(morphlist, format):
    if format == 0:
        templist = []
        for i in range(len(morphlist)):
            templist.append(morphlist[i].name)
        print(*templist, sep=', ')
    elif format == 1:
        for i in range(len(morphlist)):
            print(f"{morphlist[i].name}")
    elif format == 2:
        for i in range(len(morphlist)):
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



###########################
#                         #
#         Locus           #
#                         #
###########################


# A Locus is a particular location in a snake's chromosome which can be
# normal, or it can be mutated to produce a color variation (morph).
# This class contains a snake's possible locus factors.
# We only need to consider a certain locus if it is active in a snake's
# genetic breeding line, so by default we turn them off (False).
class Locus:
    def __init__(self):
        self.wildtype = False       # Normal, Alabama, Keys, Miami, Okeetee
        self.albino = False         # Amelanism, Ultra
        self.anery = False          # Anerythrism
        self.caramel = False        # Caramel
        self.charcoal = False       # Charcoal
        self.cinder = False         # Cinder
        self.diffused = False       # Diffused
        self.dilute = False         # Dilute
        self.hypo = False           # Hypomelanism, Strawberry, Christmas
        self.kastanie = False       # Kastanie
        self.lava = False           # Lava
        self.lavender = False       # Lavender
        self.microscale = False     # Microscale
        self.motley = False         # Motley, Stripe
        self.redcoat = False        # Red coat
        self.scaleless = False      # Scaleless
        self.sunkissed = False      # Sunkissed
        self.sunrise = False        # Sunrise
        self.terrazzo = False       # Terrazo
        self.palmetto = False       # Palmetto
        self.buf = False            # Buf
        self.masque = False         # Masque
        self.tessera = False        # Tessera
        self.toffee = False         # Toffee

    # Sets a Locus as active based on the snake's morph
    def setType(self, morph):
        if morph in getMorphNamesOnly(wild_types):
            self.wildtype = True
        elif morph == "amelanistic" or morph == "ultra" or morph == "albino":
            self.albino = True
        elif morph == "anerythristic":
            self.anery = True
        elif morph == "caramel":
            self.caramel = True
        elif morph == "charcoal":
            self.charcoal = True
        elif morph == "cinder":
            self.cinder = True
        elif morph == "diffused":
            self.diffused = True
        elif morph == "dilute":
            self.dilute = True
        elif morph == "hypomelanistic" or morph == "strawberry" or morph == "christmas":
            self.hypo = True
        elif morph == "kastanie":
            self.kastanie = True
        elif morph == "lava":
            self.lava = True
        elif morph == "lavender":
            self.lavender = True
        elif morph == "microscale":
            self.microscale = True
        elif morph == "motley" or morph == "stripe":
            self.motley = True
        elif morph == "red coat":
            self.redcoat = True
        elif morph == "scaleless":
            self.scaleless = True
        elif morph == "sunkissed":
            self.sunkissed = True
        elif morph == "sunrise":
            self.sunrise = True
        elif morph == "terrazzo":
            self.terrazzo = True
        elif morph == "palmetto":
            self.palmetto = True
        elif morph == "buf":
            self.buf = True
        elif morph == "masque":
            self.masque = True
        elif morph == "tessera":
            self.tessera = True
        elif morph == "toffee":
            self.toffee = True
        else:
            print("Error: not a valid morph name")

    # Removes all active Locus values for this snake
    def clearAllLocus(self):
        self.wildtype = False
        self.albino = False
        self.anery = False
        self.caramel = False
        self.charcoal = False
        self.cinder = False
        self.diffused = False
        self.dilute = False
        self.hypo = False
        self.kastanie = False
        self.lava = False
        self.lavender = False
        self.microscale = False
        self.motley = False
        self.redcoat = False
        self.scaleless = False
        self.sunkissed = False
        self.sunrise = False
        self.terrazzo = False
        self.palmetto = False
        self.buf = False
        self.masque = False
        self.tessera = False
        self.toffee = False

    # Retrieves a list of any Locus that are active on this snake
    def getActiveLocus(self):
        list = []
        noneActive = True

        if self.wildtype == True:
            list.append("wildtype")
            noneActive = False
        if self.albino == True:
            list.append("albino")
            noneActive = False
        if self.anery == True:
            list.append("anery")
            noneActive = False
        if self.caramel == True:
            list.append("caramel")
            noneActive = False
        if self.charcoal == True:
            list.append("charcoal")
            noneActive = False
        if self.cinder == True:
            list.append("cinder")
            noneActive = False
        if self.diffused == True:
            list.append("diffused")
            noneActive = False
        if self.dilute == True:
            list.append("dilute")
            noneActive = False
        if self.hypo == True:
            list.append("hypo")
            noneActive = False
        if self.kastanie == True:
            list.append("kastanie")
            noneActive = False
        if self.lava == True:
            list.append("lava")
            noneActive = False
        if self.lavender == True:
            list.append("lavender")
            noneActive = False
        if self.microscale == True:
            list.append("microscale")
            noneActive = False
        if self.motley == True:
            list.append("motley")
            noneActive = False
        if self.redcoat == True:
            list.append("redcoat")
            noneActive = False
        if self.scaleless == True:
            list.append("scaleless")
            noneActive = False
        if self.sunkissed == True:
            list.append("sunkissed")
            noneActive = False
        if self.sunrise == True:
            list.append("sunrise")
            noneActive = False
        if self.terrazzo == True:
            list.append("terrazzo")
            noneActive = False
        if self.palmetto == True:
            list.append("palmetto")
            noneActive = False
        if self.buf == True:
            list.append("buf")
            noneActive = False
        if self.masque == True:
            list.append("masque")
            noneActive = False
        if self.tessera == True:
            list.append("tessera")
            noneActive = False
        if self.toffee == True:
            list.append("toffee")
            noneActive = False

        if noneActive:
            list.append("none")

        return list

    # Manually sets a Locus to be active
    def setActiveLocus(self):
        list = []
        noneActive = True

        if self.wildtype == True:
            list.append("wildtype")
            noneActive = False
        if self.albino == True:
            list.append("albino")
            noneActive = False
        if self.anery == True:
            list.append("anery")
            noneActive = False
        if self.caramel == True:
            list.append("caramel")
            noneActive = False
        if self.charcoal == True:
            list.append("charcoal")
            noneActive = False
        if self.cinder == True:
            list.append("cinder")
            noneActive = False
        if self.diffused == True:
            list.append("diffused")
            noneActive = False
        if self.dilute == True:
            list.append("dilute")
            noneActive = False
        if self.hypo == True:
            list.append("hypo")
            noneActive = False
        if self.kastanie == True:
            list.append("kastanie")
            noneActive = False
        if self.lava == True:
            list.append("lava")
            noneActive = False
        if self.lavender == True:
            list.append("lavender")
            noneActive = False
        if self.microscale == True:
            list.append("microscale")
            noneActive = False
        if self.motley == True:
            list.append("motley")
            noneActive = False
        if self.redcoat == True:
            list.append("redcoat")
            noneActive = False
        if self.scaleless == True:
            list.append("scaleless")
            noneActive = False
        if self.sunkissed == True:
            list.append("sunkissed")
            noneActive = False
        if self.sunrise == True:
            list.append("sunrise")
            noneActive = False
        if self.terrazzo == True:
            list.append("terrazzo")
            noneActive = False
        if self.palmetto == True:
            list.append("palmetto")
            noneActive = False
        if self.buf == True:
            list.append("buf")
            noneActive = False
        if self.masque == True:
            list.append("masque")
            noneActive = False
        if self.tessera == True:
            list.append("tessera")
            noneActive = False
        if self.toffee == True:
            list.append("toffee")
            noneActive = False

        if noneActive:
            list.append("none")

        return list




########### Test code ###########
#
# loc = Locus()
# inhrt = amelanistic.getInheritance()
#
# print("Wild types: ", end='')
# printMorphNames(wild_types, 0)
#
# print("\nI want to add amelanistic to a snake...")
# print(f"{amelanistic.getName().capitalize()} is an {inhrt} trait.")
# print("Current active Locus is: ", end='')
# printList(loc.getActiveLocus(), 0)
#
# print("\nAdding amelanistic...")
# loc.setType(amelanistic.getName())
# print("Current active Locus is now: ", end='')
# printList(loc.getActiveLocus(), 0)
#
# print("\nAdding miami...")
# loc.setType(miami.getName())
# print("Current active Locus is now: ", end='')
# printList(loc.getActiveLocus(), 0)
#
# print("\nClearing Locus...")
# loc.clearAllLocus()
# print("Current active Locus is now: ", end='')
# printList(loc.getActiveLocus(), 0)
#
# print("\nMorphs in a line...")
# printMorphNames(dominant, 0)
#
# print("\nMorphs on new lines...")
# printMorphNames(dominant, 1)
#
# print("\nMorphs numbered...")
# printMorphNames(dominant, 2)