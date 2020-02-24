"""

Title : chrom_build.py

Purpose : Set of functions responsible for building chromosome encodings from scratch

"""

from analysis import parameters as params
from genetics.chromosome.helper import chrom_structure
from genetics.allele.helper import allele_build as ale_bui, allele_decode as ale_dec
import random


def random_encoding():
    """ Builds a completely random encoding"""

    # Generate random allele encodings
    encodings = []
    for i in range(0, params.CHROM_ALLELE_COUNT):
        # Create random allele encoding
        encoding = ale_bui.random_encoding()

        # Append random allele encoding to encoding list
        encodings.append(encoding)

    # Calculate full long and short power
    full_long_power = 0
    full_short_power = 0
    for allele_encoding in encodings:
        # Obtain position from allele encoding
        position = ale_dec.decode_position(allele_encoding)

        # Obtain power from allele encoding
        power = ale_dec.decode_power(allele_encoding) + 1

        # Add/subtract power to corresponding long/short power
        if position == 1:
            # If its a long allele
            full_long_power += power

        elif position == -1:
            # If its a short allele
            full_short_power -= power

    # Generate two random numbers; will correspond to long and short limit
    long_limit = random.randint(0, full_long_power)
    short_limit = random.randint(full_short_power, 0)

    # Make sure that the larger of the two is the long limit, and smaller is the short limit
    if long_limit < short_limit:
        long_limit, short_limit = short_limit, long_limit

    # Concatenate items for random encoding
    items = list([0, 0])
    items[chrom_structure.LONG_LIMIT_INDEX] = str(long_limit)
    items[chrom_structure.SHORT_LIMIT_INDEX] = str(short_limit)
    for allele_encoding in encodings:
        items.append(allele_encoding)

    # Form random encoding
    encoding = chrom_structure.ENCODING_KEY.join(items)

    # Return random encoding
    return encoding
