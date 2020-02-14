"""

Title : allele_crossover.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : Single function responsible for handling the crossover between two allele encodings.

Development :
    - crossover   : DONE

Testing :
    - crossover   : DONE

"""
import random
from genetics.allele.helper import allele_encode as ale_enc
from genetics.allele.helper import allele_decode as ale_dec


def crossover(allele_encoding_a, allele_encoding_b, dominance, debug=0):
    """ Create an offspring from a random crossover between two allele encodings """

    # Establish a dominant parent, always allele_encoding_a
    parents = [allele_encoding_a, allele_encoding_b]
    for i in range(dominance-1):
        parents.append(allele_encoding_a)

    # Inherit position from a random parent
    cross_pos = ale_enc.encode_position(ale_dec.decode_position(random.choice(parents)))

    # Inherit technical indicator from a random parent
    cross_tech_ind = ale_enc.encode_tech_ind(ale_dec.decode_tech_ind(random.choice(parents)))

    # Inherit threshold from a random parent
    cross_thresh = ale_enc.encode_threshold(ale_dec.decode_threshold(random.choice(parents)))

    # Inherit condition from a random parent
    cross_cond = ale_enc.encode_condition(ale_dec.decode_condition(random.choice(parents)))

    # Inherit power from a random parent
    cross_pow = ale_enc.encode_power(ale_dec.decode_power(random.choice(parents)))

    # Check that all passed crossover
    if debug:
        if cross_pos is None or cross_tech_ind is None or cross_thresh is None \
                or cross_cond is None or cross_pow is None:
            print("< ERR > : Failed to produce offspring, invalid allele states!")
            return None

    # Form crossover encoding
    offspring = cross_pos + cross_tech_ind + cross_thresh + cross_cond + cross_pow

    # Return offspring
    return offspring
