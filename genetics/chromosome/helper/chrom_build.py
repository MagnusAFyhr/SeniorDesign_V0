"""

Title : chrom_build.py

Purpose : Set of functions responsible for building chromosome encodings from scratch

"""

from genetics.chromosome.helper import chrom_structure
from genetics.allele.helper import allele_build as ale_bui, allele_decode as ale_dec
import random


def random_encoding():
    """ Builds a completely random encoding"""

    # Generate random allele encodings
    encodings = []
    for i in range(0, chrom_structure.ALLELE_COUNT):
        # Create random allele encoding
        encoding = ale_bui.random_encoding()

        # Append random allele encoding to encoding list
        encodings.append(encoding)

    # Calculate full buy and sell power
    full_buy_power = 0
    full_sell_power = 0
    for allele_encoding in encodings:
        # Obtain position from allele encoding
        position = ale_dec.decode_position(allele_encoding)

        # Obtain power from allele encoding
        power = ale_dec.decode_power(allele_encoding) + 1

        # Add/subtract power to corresponding buy/sell power
        if position == 1:
            # If its a buy allele
            full_buy_power += power

        elif position == -1:
            # If its a sell allele
            full_sell_power -= power

    # Generate two random numbers; will correspond to buy and sell limit
    buy_limit = random.randint(full_sell_power, full_buy_power)
    sell_limit = random.randint(full_sell_power, full_buy_power)

    # Make sure that the larger of the two is the buy limit, and smaller is the sell limit
    if buy_limit < sell_limit:
        buy_limit, sell_limit = sell_limit, buy_limit

    # Concatenate items for random encoding
    items = list([0, 0])
    items[chrom_structure.BUY_LIMIT_INDEX] = str(buy_limit)
    items[chrom_structure.SELL_LIMIT_INDEX] = str(sell_limit)
    for allele_encoding in encodings:
        items.append(allele_encoding)

    # Form random encoding
    encoding = chrom_structure.ENCODING_KEY.join(items)

    # Return random encoding
    return encoding
