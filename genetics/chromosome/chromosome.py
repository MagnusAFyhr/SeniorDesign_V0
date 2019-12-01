"""

Title : chromosome.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose : The Chromosome class object, responsible for providing proper
            functions and expected functionality for the Chromosome.

Development :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     : DONE
    - react         : DONE
    - as_string     : DONE

Testing :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     : DONE
    - react         : DONE
    - as_string     : DONE

"""
import random

import genetics.allele.allele as ale

from genetics.chromosome.helper import chrom_structure

from genetics.chromosome.helper import chrom_build as chr_bui

from genetics.chromosome.helper import chrom_decode as chr_dec
from genetics.chromosome.helper import chrom_encode as chr_enc

from genetics.chromosome.helper import chrom_mutate as chr_mut
from genetics.chromosome.helper import chrom_crossover as chr_cro

""" Mutation Variables """
LIMIT_MUT_PROB = 0.25
LIMIT_VOLATILITY = 0.10


class Chromosome(object):

    """
    Initialize & Verify The Chromosome
    """
    def __init__(self, encoding=None):

        # Verify Encoding
        if encoding is None:
            encoding = chr_bui.random_encoding()

        # Initialize The Chromosome With Default Values
        self.initialized = False
        self.encoding = encoding
        self.buy_limit = None
        self.sell_limit = None
        self.alleles = list([])

        # Hydrate The Chromosome (Initialize)
        if self.hydrate() is None:
            print("< ERR > : Failed to hydrate Chromosome, invalid encoding!\n{}\n".format(encoding))
            return

        # Verify The Chromosome
        if self.verify() is False:
            print("< ERR > : Failed to verify Chromosome, invalid encoding!\n{}\n".format(encoding))
            return

        # Done Initializing
        self.initialized = True
        return

    """
    Initializes Variables For Chromosome From Encoding
    """
    def hydrate(self):
        # Sanity Check
        if self.encoding is None:
            return None

        # Decode Buy & Sell Limits
        self.buy_limit = chr_dec.decode_buy_limit(self.encoding)
        self.sell_limit = chr_dec.decode_sell_limit(self.encoding)

        # Decode Alleles
        alleles = chr_dec.decode_alleles(self.encoding)
        for allele in alleles:
            self.alleles.append(allele)

        return 1

    """
    Encodes & Returns The Current State Of The Chromosome
    """
    def dehydrate(self):

        # Encode Buy Limit
        buy_limit = chr_enc.encode_buy_limit(self.buy_limit)

        # Encode Sell Limit
        sell_limit = chr_enc.encode_sell_limit(self.sell_limit)

        # Encode Alleles
        allele_encodings = []
        for allele in self.alleles:
            # Obtain encoding from allele
            allele_encoding = allele.dehydrate()

            # Check allele was properly encoded
            if allele_encoding is None:
                print("< ERR > : Failed to dehydrate Chromosome, invalid Allele state!")
                return None

            # Append allele encoding to list
            allele_encodings.append(allele_encoding)

        # Check That All Passed Encoding
        if buy_limit is None or sell_limit is None or len(allele_encodings) != chrom_structure.ALLELE_COUNT:
            print("< ERR > : Failed to dehydrate Chromosome, invalid Allele state!")
            return None

        # Concatenate items for random encoding
        items = list([0, 0])
        items[chrom_structure.BUY_LIMIT_INDEX] = buy_limit
        items[chrom_structure.SELL_LIMIT_INDEX] = sell_limit
        for allele_encoding in allele_encodings:
            items.append(allele_encoding)

        # Form Encoding
        encoding = chrom_structure.ENCODING_KEY.join(items)

        # Return Encoding
        return encoding

    """
    Verify The Initialization Of A Chromosome
    """
    def verify(self):

        # Verify Buy Limit
        if self.buy_limit is None:
            print("< ERR > : Failed to verify Chromosome : Buy Limit : {}.".format(self.buy_limit))
            return False

        else:
            try:
                int(self.buy_limit)

            except ValueError:
                print("< ERR > : Failed to verify Chromosome : Buy Limit : ({}){}."
                      .format(type(self.buy_limit), self.buy_limit))

        # Verify Sell Limit
        if self.sell_limit is None:
            print("< ERR > : Failed to verify Chromosome : Sell Limit : {}.".format(self.sell_limit))
            return False

        else:
            try:
                int(self.buy_limit)

            except ValueError:
                print("< ERR > : Failed to verify Chromosome : Sell Limit : ({}){}."
                      .format(type(self.sell_limit), self.sell_limit))

        # Verify Alleles
        if len(self.alleles) != chrom_structure.ALLELE_COUNT:
            print("< ERR > : Failed to verify Chromosome : Allele Count Invalid : {}.".format(len(self.alleles)))
            return False

        else:
            for allele in self.alleles:
                # Verify Each Allele
                if not allele.initialized:
                    print("< ERR > : Failed to verify Chromosome : Contains Invalid Allele : {}.".format(allele))
                    return False

        # Passed Verification
        return True

    """
    Returns A Mutation Of The Current Chromosome Encoding
    """
    def mutate(self, radiation=1.0):

        # Mutate Buy Limit
        buy_mut_size = self.buy_limit * LIMIT_VOLATILITY
        mut_buy_limit = chr_mut.mutate_limit(self.buy_limit,
                                             LIMIT_MUT_PROB * radiation,
                                             buy_mut_size * radiation)

        # Mutate Sell Limit
        sell_mut_size = self.sell_limit * LIMIT_VOLATILITY
        mut_sell_limit = chr_mut.mutate_limit(self.sell_limit,
                                              LIMIT_MUT_PROB * radiation,
                                              sell_mut_size * radiation)

        # Mutate Alleles
        mut_alleles = []
        for allele in self.alleles:
            mut_allele = allele.mutate()
            mut_alleles.append(mut_allele)

        # Check That All Passed Mutation
        if mut_buy_limit is None or mut_sell_limit is None:
            print("< ERR > : Failed to verify Chromosome : Contains Invalid Buy/Sell Limit.")
            return None
        for mut_allele in mut_alleles:
            # Check That Allele Passed Mutation
            if mut_allele is None:
                print("< ERR > : Failed to verify Chromosome : Contains Invalid Allele.")
                return None

        # Fix potential buy/sell limit overlap
        while mut_buy_limit < mut_sell_limit:
            # Normalize extreme limit
            rand = random.randint(0, 1)

            # Make adjustment based on random
            if rand == 0:
                mut_buy_limit += 1

            elif rand == 1:
                mut_sell_limit -= 1

        # Concatenate items for mutated encoding
        items = list([0, 0])
        items[chrom_structure.BUY_LIMIT_INDEX] = str(mut_buy_limit)
        items[chrom_structure.SELL_LIMIT_INDEX] = str(mut_sell_limit)
        for mut_allele in mut_alleles:
            items.append(mut_allele)

        # Form Mutated Encoding
        mut_encoding = chrom_structure.ENCODING_KEY.join(items)

        # Return Mutated Encoding
        return mut_encoding

    """
    Returns Two Offspring Encodings From Crossovers Between Two Parent Chromosomes
    """
    def crossover(self, mate_chrom):

        # Define 'dominance'
        dominance = 2  # this will incur a 3:1 dominance of chrom_a over chrom_b in crossover

        # Obtain parent encodings
        encoding_a = self.encoding
        encoding_b = mate_chrom.encoding

        # Create offspring
        offspring_a = chr_cro.crossover(encoding_a, encoding_b, dominance)
        offspring_b = chr_cro.crossover(encoding_b, encoding_a, dominance)

        # Return offspring
        return [offspring_a, offspring_b]

    """
    Returns A Reaction From The Chromosome
    """
    def react(self, row_dict):
        # Initialize pressure
        pressure = 0

        # Sum Pressure
        for allele in self.alleles:
            # Obtain technical indicator data from row data
            value = row_dict[allele.tech_ind]

            # Verify data
            if value is None:
                # Data corrupted
                print("< ERR > : Error in Chromosome reaction, data corrupted!"
                      "\n\tCould not find key {}.".format(allele.tech_id))

                return None

            # Add allele reaction to pressure
            pressure += allele.react(value)

        # Return Reaction
        if pressure > self.buy_limit and not (pressure < self.sell_limit):
            return "BUY"
        elif pressure < self.sell_limit and not (pressure > self.buy_limit):
            return "SELL"

        # Otherwise, Return Hold
        return "HOLD"

    """
    Returns String Representation Of The Chromosome
    """
    def as_string(self):
        # Create string representations of Chromosome variables
        header = "Chromosome : ".format(self.encoding)
        buy_limit = "\tBuy Limit  : ".format(self.buy_limit)
        sell_limit = "\tSell Limit  : ".format(self.sell_limit)
        alleles_header = "\tAlleles : "

        # Concatenate items for chromosome as string
        chrom_as_list = list([])
        chrom_as_list.append(header)
        chrom_as_list.append(buy_limit)
        chrom_as_list.append(sell_limit)
        chrom_as_list.append(alleles_header)
        for allele in self.alleles:
            chrom_as_list.append("\t\t" + allele.as_string())

        # Form Chromosome As String
        chrom_as_string = "\n".join(chrom_as_list)

        # Return Chromosome As String
        return chrom_as_string
