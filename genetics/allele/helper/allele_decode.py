"""

Title : allele_decode.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : Set of functions responsible for handling the decode operations of an allele's encoding.

Development :
    - decode_position   : DONE
    - decode_tech_ind   : DONE
    - decode_threshold  : DONE
    - decode_condition  : DONE
    - decode_power      : DONE

Testing
    - decode_position   : DONE
    - decode_tech_ind   : DONE
    - decode_threshold  : DONE
    - decode_condition  : DONE
    - decode_power      : DONE

"""
from genetics.allele.helper import allele_structure, allele_symbols
from analysis import parameters as params


def decode_position(allele_encoding):
    """ Obtains the position from the encoding """
    # Obtain position character from allele encoding
    pos_char = allele_encoding[allele_structure.POS_START:allele_structure.POS_END]

    # Check if character is a valid position
    if pos_char == allele_symbols.LONG:
        return int(1)

    elif pos_char == allele_symbols.SHORT:
        return int(-1)

    # Otherwise, return NoneType
    print("< ERR > : Allele : Error decoding Allele : Invalid Position : {} : {}.".format(pos_char, allele_encoding))
    return None


def decode_tech_ind(allele_encoding):
    """ Obtains the technical indicator from the encoding """
    # Obtain technical indicator character from allele encoding
    ti_char = allele_encoding[allele_structure.TECH_IND_START:allele_structure.TECH_IND_END]

    # Check if character is a valid technical indicator
    tech_ind = params.AVAIL_TECH_IND[ti_char]
    if tech_ind is not None:
        # Return key-value pair
        return tech_ind

    # Otherwise, return NoneType
    print("< ERR > : Allele : Error decoding Allele : Invalid Technical Indicator : {} : {}.".format(ti_char, allele_encoding))
    return None


def decode_threshold(allele_encoding):
    """ Obtains the threshold from the encoding """
    # Obtain threshold string from allele encoding
    thresh_string = allele_encoding[allele_structure.THRESH_START:allele_structure.THRESH_END]

    # Check if number string is a valid float
    try:
        float(thresh_string)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Allele : Error decoding Allele : Invalid Threshold : {} : {}.".format(thresh_string, allele_encoding))
        return None

    # Return thresh_string as float
    return float(thresh_string)


def decode_condition(allele_encoding):
    """ Obtains the condition from the encoding """
    # Obtain condition character from allele encoding
    cond_char = allele_encoding[allele_structure.COND_START:allele_structure.COND_END]

    # Check if character is a valid condition
    if cond_char == allele_symbols.LESS_THAN:
        return allele_symbols.LESS_THAN

    elif cond_char == allele_symbols.GREATER_THAN:
        return allele_symbols.GREATER_THAN

    # Otherwise, return NoneType
    print("< ERR > : Allele : Error decoding Allele : Invalid Condition : {} : {}.".format(cond_char, allele_encoding))
    return None


def decode_power(allele_encoding):
    """ Obtains the power from the encoding """
    # Obtain power character from allele encoding
    pow_char = allele_encoding[allele_structure.POW_START:allele_structure.POW_END]

    # Check if character is a valid int
    try:
        int(pow_char)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Allele : Error decoding Allele : Power : {} : {}.".format(pow_char, allele_encoding))
        return None

    # Return pow_char as integer
    return int(pow_char)
