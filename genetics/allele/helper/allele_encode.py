"""

Title : allele_encode.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : Set of functions responsible for handling the encode operations of an allele object's state.

Development :
    - encode_position   : DONE
    - encode_tech_ind   : DONE
    - encode_threshold  : DONE
    - encode_condition  : DONE
    - encode_power      : DONE

Testing
    - encode_position   : DONE
    - encode_tech_ind   : DONE
    - encode_threshold  : DONE
    - encode_condition  : DONE
    - encode_power      : DONE

"""
from genetics.allele.helper import allele_structure, allele_symbols


def encode_position(position):
    """ Converts the position back to an encoding """

    # Check if position is valid
    if position == 1:
        return allele_symbols.BUY

    elif position == -1:
        return allele_symbols.SELL

    # Otherwise, return NoneType
    print("< ERR > : Error encoding allele : Invalid Position : {}.".format(position))
    return None


def encode_tech_ind(tech_ind):
    """ Converts the technical indicator back to an encoding """

    # Loop through 'tech_ind_dict'
    for ti in allele_symbols.TECHNICAL_INDICATORS:
        # Check for match
        if allele_symbols.TECHNICAL_INDICATORS[ti] == tech_ind:
            # Return key-value pair
            return ti

    # Otherwise, return NoneType
    print("< ERR > : Error encoding allele : Invalid Technical Indicator : {}.".format(tech_ind))
    return None


def encode_threshold(threshold):
    """ Converts the threshold back to an encoding """

    # Convert float to string
    thresh_string = str(threshold)

    # Trim threshold value to fit in encoding
    thresh_len = int(allele_structure.THRESH_END - allele_structure.THRESH_START)
    thresh_string = thresh_string[0:thresh_len]

    # Add leading or trailing 0 if the length of string threshold is off
    while len(thresh_string) < thresh_len:
        # Trailing '0' if string threshold contains a '.'
        if '.' in thresh_string:
            thresh_string += "0"
        else:
            thresh_string = "0" + thresh_string

    # Check if number string is a valid float, sanity check
    try:
        float(thresh_string)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error encoding allele : Invalid Threshold : {}.".format(thresh_string))
        return None

    # Return thresh_string
    return thresh_string


def encode_condition(condition):
    """ Converts the condition back to an encoding """

    # Check if condition is valid
    if condition == allele_symbols.LESS_THAN:
        return allele_symbols.LESS_THAN

    elif condition == allele_symbols.GREATER_THAN:
        return allele_symbols.GREATER_THAN

    # Otherwise, return NoneType
    print("< ERR > : Error encoding allele : Invalid Condition : {}.".format(condition))
    return None


def encode_power(power):
    """ Converts the power back to an encoding """

    # Check if power is valid
    try:
        int(power)
        if 0 <= power <= 9:
            # Return string representation of power
            return str(power)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error encoding allele : Power : Value Error : {}.".format(power))
        return None

    # Otherwise, return NoneType
    print("< ERR > : Error encoding allele : Power : {}.".format(power))
    return None
