"""

Title : chrom_encode.py

Purpose : Set of functions responsible for handling the encode operations of a chromosome object's state

Development :
    - encode_buy_limit  : DONE
    - encode_sell_limit : DONE
    - encode_alleles    : DONE

Testing
    - encode_buy_limit  :
    - encode_sell_limit :
    - encode_alleles    :

"""


def encode_buy_limit(buy_limit):
    """ Converts the buy limit back to an encoding """
    # Check if buy limit is a valid int
    try:
        int(buy_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error encoding chromosome : Buy Limit : {}.".format(buy_limit))
        return None

    # Return buy_limit as string
    return str(buy_limit)


def encode_sell_limit(sell_limit):
    """ Converts the sell limit back to an encoding """
    # Check if buy limit is a valid int
    try:
        int(sell_limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Error encoding chromosome : Sell Limit : {}.".format(sell_limit))
        return None

    # Return sell_limit as string
    return str(sell_limit)


def encode_alleles(alleles):
    """ Converts the alleles back to an encoding """
    # Convert all alleles back to an encoding
    encodings = list([])
    for allele in alleles:

        # Dehydrate Allele
        encoding = allele.dehydrate()

        # Verify Allele Encoding
        if encoding is not None:
            encodings.append(encoding)

        else:
            # Otherwise, return NoneType
            print("< ERR > : Error encoding chromosome : Allele encoding failed : {}.".format(allele.encoding))
            return None

    # Return set of encoded alleles
    return encodings


