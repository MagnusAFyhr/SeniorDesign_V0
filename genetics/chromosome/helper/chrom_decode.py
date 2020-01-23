"""

Title : chrom_decode.py

Purpose : Set of functions responsible for handling the decode operations of a chromosome's encoding

Development :
    - decode_buy_limit  : DONE
    - decode_sell_limit : DONE
    - decode_alleles    : DONE

Testing
    - decode_buy_limit  : DONE
    - decode_sell_limit : DONE
    - decode_alleles    :

"""
from genetics.chromosome.helper import chrom_structure
import genetics.allele.allele as ale


def decode_buy_limit(chrom_encoding):
    """ Obtain buy limit from the encoding """
    # Unwrap encoding
    items = chrom_encoding.split(chrom_structure.ENCODING_KEY)

    # Obtain buy limit from chromosome encoding
    buy_limit = items[chrom_structure.BUY_LIMIT_INDEX]

    # Check if buy limit is a valid int
    try:
        int(buy_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error decoding chromosome : Buy Limit : {}.".format(buy_limit))
        return None

    # Return buy_limit as integer
    return int(buy_limit)


def decode_sell_limit(chrom_encoding):
    """ Obtain sell limit from the encoding """
    # Unwrap encoding
    items = chrom_encoding.split(chrom_structure.ENCODING_KEY)

    # Obtain sell limit from chromosome encoding
    sell_limit = items[chrom_structure.SELL_LIMIT_INDEX]

    # Check if sell limit is a valid int
    try:
        int(sell_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error decoding chromosome : Sell Limit : {}.".format(sell_limit))
        return None

    # Return sell_limit as integer
    return int(sell_limit)


def decode_alleles(chrom_encoding, debug_mode):
    """ Obtain & initialize alleles from the encoding """
    # Unwrap encoding
    items = chrom_encoding.split(chrom_structure.ENCODING_KEY)

    # Obtain buy limit from chromosome encoding
    allele_codes = items[chrom_structure.ALLELE_START:]

    # Initialize all alleles
    alleles = list([])
    for encoding in allele_codes:
        # Initialize Allele
        allele = ale.Allele(encoding, debug_mode)

        # Verify Allele
        if allele.initialized:
            alleles.append(allele)

        else:
            # Otherwise, return NoneType
            print("< ERR > : Error decoding chromosome : Allele initialization failed : {}.".format(encoding))
            return None

    # Return set of initialized alleles
    return alleles
