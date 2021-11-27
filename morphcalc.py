#######################################################################################
# Corn Snake Breeding Calculator
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This program will take two parent snakes with known morphs and calculate
# the possible breeding results based on that information.
#######################################################################################

import morphs
import punnettcalc
from textwrap import wrap


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

    # Add a morph to this snake (input a new instance of a morph)
    def addMorph(self, morph):
        self.morphs.append(morph)

    # Removes a morph object from this snake
    def removeMorph(self, morph):
        self.morphs.remove(morph)

    # Returns a string of all morph names on this snake, separated by commas
    def getMorphNameList(self):
        return morphs.getMorphNamesOnly(self.morphs)

    # Returns a list of all morph objects on this snake
    def getMorphObjList(self):
        return self.morphs

    # Returns a morph object on this snake based on its name
    def getMorphByName(self, name):
        for x in self.morphs:
            if x.getName == name:
                return x

    # Removes all data from snake
    def clearData(self):
        self.name = ""
        self.morphs.clear()


#######################################
#   Breeding calculation functions.   #
#######################################

# Global variables for calculations
allele_dict = {}
total_mutated = 0

# Add a key to the global allele dict
def addKey(key, val):
    global allele_dict
    allele_dict[key] = val

# Clear the allele_dict
def clearDict():
    global allele_dict
    allele_dict.clear()

# Takes a dict and sorts by key name alphabetically
def sortDict(dict):
    result = sorted(dict.items())
    return result

# Increment a character and return it
def incChar(ch):
    temp = chr(ord(ch) + 1)
    return temp

# This function takes two parent snakes with morphs that are not equivalent, then returns a list of two lists that are comparable
def matchMorphs(p1, p2):
    # Make a copy of each parents' morph lists
    morphs_p1 = p1.morphs.copy()
    morphs_p2 = p2.morphs.copy()

    tempList1 = []      # These lists will contain matched morphs
    tempList2 = []
    matched = []        # Used for keeping track of which morphs are already matched

    # Look at each morph, determine if the same trait exists in the other parent
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

    results = [tempList1, tempList2]
    return results

# Builds the allele dictionary
def storeToDict(morph, char):
    name = morph.getName()
    none = "no mutation"
    het = "het "
    vis = " (Visual)"
    nonvis = " (Nonvisual)"
    sup = " (Super)"

    upper = char.upper() + char.upper()
    mixed1 = char.upper() + char.lower()
    mixed2 = char.lower() + char.upper()
    lower = char.lower() + char.lower()

    # Dominant traits
    if morph.inheritance == 'D':
        addKey(upper, none)
        addKey(mixed1, het + name + vis)
        addKey(mixed2, het + name + vis)
        addKey(lower, name + vis)
    # Incomplete dominant traits
    elif morph.inheritance == 'I':
        addKey(upper, none)
        addKey(mixed1, het + name + vis)
        addKey(mixed2, het + name + vis)
        addKey(lower, name + sup)
    # Recessive traits
    elif morph.inheritance == 'R':
        addKey(upper, none)
        addKey(mixed1, het + name + nonvis)
        addKey(mixed2, het + name + nonvis)
        addKey(lower, name + vis)
    elif morph.inheritance == 'N':
        addKey("##", name)

# This function translates a list of morph objectss into allele characters for a Punnett Square
# Returned is a dict in the form of: alleles = {"XX":"normal", "AA":"alemanistic"}
def getAllelesFromMorphList(morphlist):
    alleles = {}
    char = 'A'

    for x in morphlist:
        # Normal traits are always inherited
        if x.inheritance == 'N':
            alleles["##"] = x.getName()
            storeToDict(x, "#")
        # Other traits are AA if normal (non-mutated), Aa if het, and aa if fully mutated
        else:
            name = x.getName()

            if x.het == True:
                pair = char.upper() + char.lower()
                alleles[pair] = "het " + name
            elif x.default == True:
                pair = char.upper() + char.upper()
                alleles[pair] = name
            else:
                pair = char.lower() + char.lower()
                alleles[pair] = name

            storeToDict(x, char)
        char = incChar(char)

    return alleles

# This function takes two snakes and returns a list of the Punnett results
def breedResults(p1, p2):
    # Get comparable morph lists
    matched_lists = matchMorphs(p1, p2)

    # Convert the morph names into allele characters that can be used in a Punnett Square
    p1_alleles = "".join(getAllelesFromMorphList(matched_lists[0]))
    p2_alleles = "".join(getAllelesFromMorphList(matched_lists[1]))

    # Run the Punnet Square calculation and return the results
    results = punnettcalc.punnett(p1_alleles, p2_alleles)

    return results

# Gets a list of alleles from Punnett Results
def getAllelesFromResults(results):
    # Get a list of each character used for alleles
    alleles = wrap(results[0], 2)
    for i in range(len(alleles)):
        alleles[i] = alleles[i][0]

    return alleles

# Take the punnet results, sorts them into matching groups, returns a list of lists for translation
def sortPunnettResults(results, alleles, index):
    curr_char = alleles[index]

    upper = curr_char.upper() + curr_char.upper()
    mixed1 = curr_char.lower() + curr_char.upper()
    mixed2 = curr_char.upper() + curr_char.lower()
    lower = curr_char.lower() + curr_char.lower()

    total_list = []
    upper_list = []
    mixed_list = []
    lower_list = []

    # If all results are the same, return the bag as is
    if all(x == results[0] for x in results):
        return results
    else:
        for a in results:
            if upper in a:
                upper_list.append(a)
            elif mixed1 in a or mixed2 in a:
                mixed_list.append(a)
            elif lower in a:
                lower_list.append(a)

        if index < len(alleles) - 1:
            total_list.append(sortPunnettResults(upper_list, alleles, index + 1))
            total_list.append(sortPunnettResults(mixed_list, alleles, index + 1))
            total_list.append(sortPunnettResults(lower_list, alleles, index + 1))
        else:
            total_list.append(upper_list)
            total_list.append(mixed_list)
            total_list.append(lower_list)

        return total_list

# Takes the sorted Punnett results and translates them to plain English
def sortedPunnettToNames(sorted_results, total_num_results):
    global total_mutated
    result_string = ""
    for a in sorted_results:
        # If this item contains another list, recurse
        if type(a) == list:
            breakdown = sortedPunnettToNames(a, total_num_results)
            if breakdown != "":
                result_string = result_string + breakdown + "\n"
        # If a is not a list, format results and return as string
        else:
            global allele_dict

            # Get allele pairs
            pairs = wrap(a, 2)

            # Translate them into English
            for i in range(len(pairs)):
                pairs[i] = allele_dict[pairs[i]]

            # Remove any non-mutated alleles
            pairs = list(filter(("no mutation").__ne__, pairs))
            if len(pairs) < 1:
                return ""

            # Join the results
            complete_pairs = ", ".join(pairs)

            # Calculate total and return
            percentage = (len(sorted_results) / total_num_results) * 100
            total_mutated = total_mutated + percentage
            result = str(percentage) + "% " + complete_pairs
            return result
    return result_string

# This calculates the number of normal morphs AFTER the rest have been sorted
def addNumNormal():
    global total_mutated
    global allele_dict
    if total_mutated >= 100.0:
        return ""
    else:
        num_normal_results = 100 - total_mutated
        if "##" in allele_dict:
            return str(num_normal_results) + "% " + allele_dict["##"]
        else:
            return str(num_normal_results) + "% normal"

# Use this after completing calculations to clear global variables
def clearResults():
    global allele_dict
    global total_mutated
    allele_dict = {}
    total_mutated = 0

# Runs all necessary functions in order to get results
def run(p1, p2):

    # Get Punnett Square results
    breed_results = breedResults(p1, p2)

    # Translate the morph names to alleles
    result_alleles = getAllelesFromResults(breed_results)

    # Sort the results
    sorted = sortPunnettResults(breed_results, result_alleles, 0)

    # Translate back into names
    names = sortedPunnettToNames(sorted, len(breed_results)) + addNumNormal()
    final_ouput = "\n"
    for line in names.splitlines():
        if line != "":
            final_ouput = final_ouput + line + "\n\n"

    # Reset data for next calculation
    clearResults()

    return final_ouput[:-2]


############### Test Code ###############
p1 = Snake()
p2 = Snake()

# p1.addMorph(morphs.Morph("okeetee", 'N'))
# p2.addMorph(morphs.Morph("okeetee", 'N'))

# p1.addMorph(morphs.Morph("amelanistic", 'R', True))
# p1.addMorph(morphs.Morph("charcoal", 'R', True))
# p1.addMorph(morphs.Morph("hypomelanistic", 'R'))
# p2.addMorph(morphs.Morph("lavender", 'R', True))
# p2.addMorph(morphs.Morph("tessera", 'D'))
# p2.addMorph(morphs.Morph("caramel", 'R', True))

# p1.addMorph(morphs.Morph("amelanistic", 'R', True))
# p1.addMorph(morphs.Morph("microscale", 'R', True))
# p1.addMorph(morphs.Morph("keys", 'N'))
# p2.addMorph(morphs.Morph("amelanistic", 'R', True))
# p2.addMorph(morphs.Morph("microscale", 'R', True))

# print(run(p1, p2))