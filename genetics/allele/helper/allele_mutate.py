"""

Title : allele_mutate.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : Set of functions responsible for handling the mutation of an allele's encoding.

Development :
    - should_mutate     : DONE
    - mutate_position   : DONE
    - mutate_tech_ind   : DONE
    - mutate_threshold  : DONE
    - mutate_condition  : DONE
    - mutate_power      : DONE

Testing :
    - should_mutate     : DONE
    - mutate_position   : DONE
    - mutate_tech_ind   : DONE
    - mutate_threshold  : DONE
    - mutate_condition  : DONE
    - mutate_power      : DONE

"""
from genetics.allele.helper import allele_structure, allele_symbols
import random


def should_mutate(mutate_prob):
    """ Determine if mutation should occur """

    result = random.random()
    if result < mutate_prob:
        # Mutation should occur
        return True

    # Otherwise, mutation should not occur
    return False


def mutate_position(position, mutate_prob):
    """ Obtains mutation of position """

    # Check if mutation should occur
    if not should_mutate(mutate_prob):
        # No mutation
        return position

    # Mutate position
    if position == allele_symbols.RAW_BUY:
        return allele_symbols.RAW_SELL

    elif position == allele_symbols.RAW_SELL:
        return allele_symbols.RAW_BUY

    # Otherwise, return NoneType
    print("< ERR > : Error mutating allele : Invalid Position : {}.".format(pos_char))
    return None


def mutate_tech_ind(tech_ind, mutate_prob):
    """ Obtains mutation of technical indicator """

    # Check if mutation should occur
    if not should_mutate(mutate_prob):
        # No mutation
        return tech_ind

    # Mutate technical indicator
    values = list(allele_symbols.TECHNICAL_INDICATORS.values())
    tech_ind = random.choice(values)

    # Return mutated technical indicator
    return tech_ind


def mutate_threshold(threshold, mutate_prob, mutate_size):
    """ Obtains mutation of threshold """

    # Check if mutation should occur
    if not should_mutate(mutate_prob):
        # No mutation
        return threshold

    # Verify threshold is a float
    try:
        float(threshold)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error mutating allele : Invalid Threshold : {}.".format(threshold))
        return None

    # Mutate threshold
    mut_threshold = float(threshold)
    mutation = random.uniform(-mutate_size, mutate_size)
    mut_threshold += mutation

    # Return mutated threshold
    return mut_threshold


def mutate_condition(condition, mutate_prob):
    """ Obtains mutation of condition """

    # Check if mutation should occur
    if not should_mutate(mutate_prob):
        # No mutation
        return condition

    # Mutate condition
    if condition == allele_symbols.LESS_THAN:
        return allele_symbols.GREATER_THAN

    elif condition == allele_symbols.GREATER_THAN:
        return allele_symbols.LESS_THAN

    # Otherwise, return NoneType
    print("< ERR > : Error mutating allele : Invalid Condition : {}.".format(condition))
    return None


def mutate_power(power, mutate_prob):
    """ Obtains mutation of power """

    # Check if mutation should occur
    if not should_mutate(mutate_prob):
        # No mutation
        return power

    # Verify power is a number
    try:
        int(power)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error mutating allele : Invalid Power : {}.".format(power))
        return None

    # Mutate Power
    mut_power = int(power)
    mutation = random.choice([-1, 1])
    mut_power += mutation

    # Bound Mutation
    if mut_power < 0:
        mut_power = 0

    elif mut_power > 9:
        mut_power = 9

    # Return mutated power
    return mut_power
