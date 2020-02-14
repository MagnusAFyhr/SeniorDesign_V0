"""

Title : allele_crossover.py

Purpose : Single function responsible for handling the crossover between two chromosome encodings

"""

from analysis import parameters as params

from genetics.chromosome.helper import chrom_structure
from genetics.chromosome.helper import chrom_encode as chr_enc
from genetics.chromosome.helper import chrom_decode as chr_dec

from genetics.allele.helper import allele_decode as ale_dec
from genetics.allele.helper import allele_crossover as ale_cro

import random


def crossover(chrom_encoding_a, chrom_encoding_b, dominance):
    """ Create an offspring from a random crossover between two chromosome encodings """

    # Establish a dominant parent, always allele_encoding_a
    parents = [chrom_encoding_a, chrom_encoding_b]
    for i in range(dominance-1):
        parents.append(chrom_encoding_a)

    # Inherit buy limit from a random parent
    cross_buy_limit = chr_enc.encode_buy_limit(chr_dec.decode_buy_limit(random.choice(parents)))

    # Inherit sell_limit from a random parent
    cross_sell_limit = chr_enc.encode_sell_limit(chr_dec.decode_sell_limit(random.choice(parents)))

    # Obtain allele encodings from chromosome encodings
    allele_encodings_a = chrom_encoding_a.split(chrom_structure.ENCODING_KEY)[chrom_structure.ALLELE_START:]
    allele_encodings_b = chrom_encoding_b.split(chrom_structure.ENCODING_KEY)[chrom_structure.ALLELE_START:]

    # Inherit crossover alleles from all compatible allele pairs
    cross_allele_encodings = list([])
    for a_enc in allele_encodings_a:
        for b_enc in allele_encodings_b:
            tech_ind_a = ale_dec.decode_tech_ind(a_enc)
            tech_ind_b = ale_dec.decode_tech_ind(b_enc)

            # Check if alleles are compatible for crossover
            if tech_ind_a == tech_ind_b:
                # If compatible, create crossover allele
                cross_allele = ale_cro.crossover(a_enc, b_enc, dominance)

                # Append crossover allele
                cross_allele_encodings.append(cross_allele)

                # Remove allele encoding from a and b
                try:
                    allele_encodings_a.remove(a_enc)
                    allele_encodings_b.remove(b_enc)
                except ValueError:
                    print("< ERR > : Error crossing chromosomes : Allele match, but not found in list : {} : {}."
                          .format(a_enc, b_enc))

                # Skip to next iteration
                break

    # Fill in rest of crossover alleles with alleles from random parents
    while len(cross_allele_encodings) < params.CHROM_ALLELE_COUNT:
        # Inherit random allele from random parent
        parent_of_allele = random.choice(parents)

        # Choose random allele from selected parent
        if parent_of_allele == chrom_encoding_a:
            # If random choice was chromosome a
            allele_encoding = random.choice(allele_encodings_a)
            cross_allele_encodings.append(allele_encoding)

        else:
            # If random choice was chromosome b
            allele_encoding = random.choice(allele_encodings_b)
            cross_allele_encodings.append(allele_encoding)

    # Verify crossover allele encodings list
    if len(cross_allele_encodings) != params.CHROM_ALLELE_COUNT:
        print("< ERR > : Error crossing chromosomes : Allele count invalid : {}.".format(len(cross_allele_encodings)))
        return None

    # Concatenate items for crossover encoding
    items = list([0, 0])
    items[chrom_structure.BUY_LIMIT_INDEX] = cross_buy_limit
    items[chrom_structure.SELL_LIMIT_INDEX] = cross_sell_limit
    for allele_encoding in cross_allele_encodings:
        items.append(allele_encoding)

    # Form crossover encoding
    cross_encoding = chrom_structure.ENCODING_KEY.join(items)

    # Return crossover encoding
    return cross_encoding
