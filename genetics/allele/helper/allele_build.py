"""

Title : allele_build.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : Set of functions responsible for building allele encodings from scratch.

Development :
    - random_encoding   : DONE

Testing :
    - random_encoding   : DONE

"""

from genetics.allele.helper import allele_structure, allele_symbols
from analysis import parameters as params
import random


def random_encoding(tech_ind=""):
    """ Builds a completely random encoding"""

    # Generate random position
    r_pos = random.randint(0, 1)
    if r_pos == 0:
        pos = allele_symbols.LONG
    else:
        pos = allele_symbols.SHORT

    # Generate random technical indicator
    if tech_ind not in params.AVAIL_TECH_IND:
        keys = list(params.AVAIL_TECH_IND.keys())
        tech_ind = random.choice(keys)

    # Generate random threshold
    n_thresh = random.uniform(params.ALLELE_THRESH_RAND_MIN, params.ALLELE_THRESH_RAND_MAX)
    thresh_len = allele_structure.THRESH_END - allele_structure.THRESH_START
    thresh = str(n_thresh)[0:thresh_len]

    # Generate random condition
    r_cond = random.randint(0, 1)
    if r_cond == 0:
        cond = allele_symbols.LESS_THAN
    else:
        cond = allele_symbols.GREATER_THAN

    # Obtain random power
    power = str(random.randint(0, 9))

    # Form random encoding
    encoding = pos + tech_ind + thresh[0:] + cond + power  # thresh_len

    # Return random encoding
    return encoding







