"""

Title : chrom_encode.py

Purpose : Set of functions responsible for handling the encode operations of a chromosome object's state

Development :
    - encode_long_limit  : DONE
    - encode_short_limit : DONE
    - encode_alleles    : DONE

Testing
    - encode_long_limit  :
    - encode_short_limit :
    - encode_alleles    :

"""


def encode_long_limit(long_limit):
    """ Converts the long limit back to an encoding """
    # Check if long limit is a valid int
    try:
        int(long_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Chromosome : Error encoding Chromosome : Buy Limit : {}.".format(long_limit))
        return None

    # Return long_limit as string
    return str(int(long_limit))


def encode_short_limit(short_limit):
    """ Converts the short limit back to an encoding """
    # Check if short limit is a valid int
    try:
        int(short_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Chromosome : Error encoding Chromosome : Sell Limit : {}.".format(short_limit))
        return None

    # Return short_limit as string
    return str(int(short_limit))


def encode_alleles(alleles):
    """ Converts the alleles back to an encoding """
    encodings = list([])
    for allele in alleles:

        # Dehydrate Allele
        encoding = allele.dehydrate()

        # Verify Allele Encoding
        if encoding is not None:
            encodings.append(encoding)

        else:
            # Otherwise, return NoneType
            print("< ERR > : Chromosome : Error encoding Chromosome : Allele encoding failed : {}.".format(allele.encoding))
            return None

    # Return set of encoded alleles
    return encodings


