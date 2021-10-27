#######################################################################################
# Punnett Square Calculation
# Name: Hannah Moon
# Date: 10/25/2021
# Description: This calculates punnett square results used for breeding calculations
#######################################################################################

# This code was referenced for this function:
# https://stackoverflow.com/questions/15170551/punnett-square-function-matching-items-in-lists

import itertools
from itertools import product

# This will separate a set of alleles into a list with groups of two
# i.e. 'AaBBCc' becomes [[A, a], [B, B], [C, c]]
def allele(e):
    return [list(v) for _, v in itertools.groupby(e, key = str.lower)]

# This returns a list of all possible results from the cartesian product of the groups of alleles
# i.e. AaBb => AB, Ab, aB, ab
def punnett(a, b):
    return [''.join(e)
        for e in product(*([''.join(e) for e in product(*e)]
            for e in zip(allele(a), allele(b))))]

# Test code:

# p1 = "AaBb"
# p2 = "AaBb"
# p3 = "AAbb"
# allele_list = allele(p1)
# punnett_list = punnett(p1, p2)
#
# print(f"Allele list: {allele_list}")
# print(f"Punnett results: {punnett_list}")