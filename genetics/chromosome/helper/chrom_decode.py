"""

Title : chrom_decode.py

Purpose : Set of functions responsible for handling the decode operations of a chromosome's encoding

Development :
    - decode_long_limit  : DONE
    - decode_short_limit : DONE
    - decode_alleles    : DONE

Testing
    - decode_long_limit  : DONE
    - decode_short_limit : DONE
    - decode_alleles    :

"""
from genetics.chromosome.helper import chrom_structure
import genetics.allele.allele as ale


def decode_long_limit(chrom_encoding):
    """ Obtain long limit from the encoding """
    # Unwrap encoding
    items = chrom_encoding.split(chrom_structure.ENCODING_KEY)

    # Obtain long limit from chromosome encoding
    long_limit = items[chrom_structure.LONG_LIMIT_INDEX]

    # Check if long limit is a valid int
    try:
        int(long_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Chromosome : Error decoding Chromosome : Long Limit : {}.".format(long_limit))
        return None

    # Return long_limit as integer
    return int(long_limit)


def decode_short_limit(chrom_encoding):
    """ Obtain short limit from the encoding """
    # Unwrap encoding
    items = chrom_encoding.split(chrom_structure.ENCODING_KEY)

    # Obtain short limit from chromosome encoding
    short_limit = items[chrom_structure.SHORT_LIMIT_INDEX]

    # Check if short limit is a valid int
    try:
        int(short_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Chromosome : Error decoding Chromosome : Short Limit : {}.".format(short_limit))
        return None

    # Return short_limit as integer
    return int(short_limit)


def decode_alleles(chrom_encoding, debug_mode):
    """ Obtain & initialize alleles from the encoding """
    # Unwrap encoding
    items = chrom_encoding.split(chrom_structure.ENCODING_KEY)

    # Obtain long and short limit from chromosome encoding
    allele_codes = items[chrom_structure.ALLELE_START:]

    # Initialize all alleles
    alleles = list([])
    for encoding in allele_codes:
        # Initialize Allele
        allele = ale.Allele(encoding=encoding, debug=debug_mode)

        # Verify Allele
        if allele.initialized:
            alleles.append(allele)

        else:
            # Otherwise, return NoneType
            print("< ERR > : Chromosome : Error decoding Chromosome : Allele initialization failed : {}.".format(encoding))
            return None

    # Return set of initialized alleles
    return alleles
