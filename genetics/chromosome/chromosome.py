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
    - status        :
    - as_string     : DONE

Testing :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     : DONE
    - react         : DONE
    - status        :
    - as_string     : DONE

Cleaning :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     :
    - react         : DONE
    - status        : DONE
    - as_string     :

TO-DO:


Comments :
    - good idea to clean, organize, optimize, comment, etc. all the 'helper' functions/files for the Chromosome
    - found potential new parameter; the space between the long and short limit; 'hold buffer'?
    - mutate() in this class does not apply mutation to itself!!! but allele does

Future Improvements :
    - add 'trigger_count' variable to track how and when a chromosome triggers an action.

"""
import random

import analysis.parameters as params

from genetics.chromosome.helper import chrom_structure

from genetics.chromosome.helper import chrom_build as chr_bui

from genetics.chromosome.helper import chrom_decode as chr_dec
from genetics.chromosome.helper import chrom_encode as chr_enc

from genetics.chromosome.helper import chrom_mutate as chr_mut
from genetics.chromosome.helper import chrom_crossover as chr_cro


class Chromosome(object):

    """
    Initialize & Verify The Chromosome
    """
    def __init__(self, encoding=None, debug=0):

        # Check Encoding
        if encoding is None:
            encoding = chr_bui.random_encoding()

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0
        self._is_debug = False

        self.encoding = encoding
        self.long_limit = None
        self.short_limit = None
        self.alleles = list([])

        # Setup Debug Mode
        self._debug_mode = debug
        if debug in params.CHROM_DEBUG:
            self._is_debug = True

        # Hydrate The Chromosome (Initialization)
        if not self.hydrate():
            print("< ERR > : Chromosome : Failed to hydrate Chromosome, invalid encoding!\n< ERR > : {}.".format(encoding))
            return

        # Verify The Chromosome
        if self._is_debug:
            if self.verify() is False:
                print("< ERR > : Chromosome : Failed to verify Chromosome, invalid encoding!\n< ERR > : {}.".format(encoding))
                return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Initializes Variables For Chromosome From Encoding
    """
    def hydrate(self):
        # Sanity Check
        if self.encoding is None:
            return False

        # Decode Long & Short Limit
        self.long_limit = chr_dec.decode_long_limit(self.encoding)
        self.short_limit = chr_dec.decode_short_limit(self.encoding)

        # Decode Alleles
        alleles = chr_dec.decode_alleles(self.encoding, self._is_debug)
        for allele in alleles:
            self.alleles.append(allele)

        # Hydration Complete!
        return True

    """
    Encodes & Returns The Current State Of The Chromosome
    """
    def dehydrate(self):

        # Encode Long Limit
        long_limit = chr_enc.encode_long_limit(self.long_limit)

        # Encode Short Limit
        short_limit = chr_enc.encode_short_limit(self.short_limit)

        # Encode Alleles
        allele_encodings = []
        for allele in self.alleles:
            # obtain encoding from allele
            allele_encoding = allele.dehydrate()

            # check that allele was properly encoded
            if self._is_debug:
                if allele_encoding is None:
                    print("< ERR > : Chromosome : Failed to dehydrate Chromosome, invalid Allele state!")
                    return None

            # append allele encoding to list
            allele_encodings.append(allele_encoding)

        # Check That All Passed Encoding
        if self._is_debug:
            if long_limit is None or short_limit is None or len(allele_encodings) != params.CHROM_ALLELE_COUNT:
                print("< ERR > : Chromosome : Failed to dehydrate Chromosome, invalid Allele state!")
                return None

        # Concatenate Items For Encoding
        items = list([0, 0])
        items[chrom_structure.LONG_LIMIT_INDEX] = long_limit
        items[chrom_structure.SHORT_LIMIT_INDEX] = short_limit
        for allele_encoding in allele_encodings:
            items.append(allele_encoding)

        # Form Encoding
        encoding = chrom_structure.ENCODING_KEY.join(items)

        # Dehydration Complete; Return Encoding!
        return encoding

    """
    Verifies The Initialization Of A Chromosome
    """
    def verify(self):

        # Verify Long Limit
        if self.long_limit is None:
            print("< ERR > : Chromosome : Failed to verify Chromosome : Long Limit : {}.".format(self.long_limit))
            return False

        else:
            # try and cast 'long_limit' to int
            try:
                int(self.long_limit)

            except ValueError:
                print("< ERR > : Chromosome : Failed to verify Chromosome : Long Limit : ({}){}.".format(
                    type(self.long_limit),
                    self.long_limit
                ))
                return False

        # Verify Short Limit
        if self.short_limit is None:
            print("< ERR > : Chromosome : Failed to verify Chromosome : Short Limit : {}.".format(self.short_limit))
            return False

        else:
            # try and cast 'short_limit' to int
            try:
                int(self.short_limit)

            except ValueError:
                print("< ERR > : Failed to verify Chromosome : Short Limit : ({}){}.".format(
                    type(self.short_limit),
                    self.short_limit
                ))
                return False

        # Verify Alleles
        if len(self.alleles) != params.CHROM_ALLELE_COUNT:
            print("< ERR > : Failed to verify Chromosome : Allele Count Invalid : {}.".format(len(self.alleles)))
            return False

        else:
            # verify each allele
            for allele in self.alleles:
                if not allele.initialized:
                    print("< ERR > : Failed to verify Chromosome : Contains Invalid Allele : {}.".format(
                        allele.encoding
                    ))
                    return False

        # Verification Complete!
        return True

    """
    Mutates The State Of The Chromosome & Returns The Encoding Of This Mutation
    """
    def mutate(self, radiation=1.0):

        # Mutate Long Limit
        long_mut_size = self.long_limit * params.CHROM_LIMIT_VOLATILITY
        mut_long_limit = chr_mut.mutate_limit(self.long_limit,
                                              params.CHROM_LIMIT_MUT_PROB * radiation,
                                              int(long_mut_size * radiation))

        # Mutate Short Limit
        short_mut_size = self.short_limit * params.CHROM_LIMIT_VOLATILITY
        mut_short_limit = chr_mut.mutate_limit(self.short_limit,
                                               params.CHROM_LIMIT_MUT_PROB * radiation,
                                               int(short_mut_size * radiation))

        # Mutate Alleles
        mut_alleles = []
        for allele in self.alleles:
            mut_allele = allele.mutate()
            mut_alleles.append(mut_allele)

        # Check That All Passed Mutation
        if self._is_debug:
            if mut_long_limit is None or mut_short_limit is None:
                print("< ERR > : Failed to verify Chromosome : Contains Invalid Long/Short Limit.")
                return None
            # check that all allele mutations were valid
            for mut_allele in mut_alleles:
                if mut_allele is None:
                    print("< ERR > : Failed to verify Chromosome : Contains Invalid Allele.")
                    return None

        # Fix Potential Long/Short Limit Overlap
        while mut_long_limit < mut_short_limit:
            # make random choice to adjust long or short
            rand = random.randint(0, 1)

            # make adjustment based on random
            if rand == 0:
                mut_long_limit += 1

            elif rand == 1:
                mut_short_limit -= 1

        # Concatenate Items For Mutated Encoding
        items = list([0, 0])
        items[chrom_structure.LONG_LIMIT_INDEX] = str(mut_long_limit)
        items[chrom_structure.SHORT_LIMIT_INDEX] = str(mut_short_limit)
        items.extend(mut_alleles)

        # Form Mutated Encoding
        mut_encoding = chrom_structure.ENCODING_KEY.join(items)

        # Mutation Complete; Return Mutated Encoding!
        return mut_encoding

    """
    Returns Two Offspring Encodings From Crossovers Between Two Parent Chromosomes
    """
    def crossover(self, mate_chrom):

        # Define 'dominance'; Incurs A 'n:1' Dominance Of Parent 1 Over Parent 2 In Crossover
        dominance = params.CHROM_CROSS_DOMINANCE

        # Obtain Parent Encodings
        encoding_a = self.encoding
        encoding_b = mate_chrom.encoding

        # Create Offspring
        offspring_a = chr_cro.crossover(encoding_a, encoding_b, dominance)
        offspring_b = chr_cro.crossover(encoding_b, encoding_a, dominance)

        # Crossover Complete; Return Offspring!
        return [offspring_a, offspring_b]

    """
    Returns A Reaction From The Chromosome
    """
    def react(self, row_dict):
        # Initialize Pressure
        pressure = 0

        # Calculate Pressure
        for allele in self.alleles:
            # obtain technical indicator data from row data
            value = row_dict[allele.tech_ind]

            # verify data
            if self._is_debug:
                if value is None:
                    # data corrupted
                    print("< ERR > : Error in Chromosome reaction, data corrupted!"
                          "\n\tCould not find key {}.".format(allele.tech_id))

                    return None

            # add allele reaction to pressure
            pressure += allele.react(value)

        # Return Long/Short Reaction
        if pressure > self.long_limit:
            # check double reaction
            if self._is_debug:
                if pressure < self.short_limit:
                    print("< ERR > : Error in Chromosome reaction, long and short limit triggered.")
                    return None

            return "LONG"

        elif pressure < self.short_limit:
            # check double reaction
            if self._is_debug:
                if pressure > self.long_limit:
                    print("< ERR > : Error in Chromosome reaction, short and long limit triggered.")
                    return None

            return "SHORT"

        # Otherwise, Return Hold
        return params.CHROM_HOLD_OR_EXIT

    """
    Returns Dictionary Representation Of Chromosome's Current State
    """
    def status(self):
        # Format Chromosome Into Dictionary Object
        state = {
            "init": self.initialized,
            "debug_mode": self._debug_mode,
            "is_debug": self._is_debug,

            "encoding": self.encoding,
            "long_limit": self.long_limit,
            "short_limit": self.short_limit,

            "alleles": [allele.status() for allele in self.alleles]
        }

        # Return Dictionary Object
        return state

    """
    Returns String Representation Of The Chromosome
    """
    def as_string(self):
        # Create string representations of Chromosome variables
        header = "Chromosome : ".format(self.encoding)
        long_limit = "\tLong Limit  : ".format(self.long_limit)
        short_limit = "\tShort Limit  : ".format(self.short_limit)
        alleles_header = "\tAlleles : "

        # Concatenate items for chromosome as string
        chrom_as_list = list([])
        chrom_as_list.append(header)
        chrom_as_list.append(long_limit)
        chrom_as_list.append(short_limit)
        chrom_as_list.append(alleles_header)
        for allele in self.alleles:
            chrom_as_list.append("\t\t" + allele.as_string())

        # Form Chromosome As String
        chrom_as_string = "\n".join(chrom_as_list)

        # Return Chromosome As String
        return chrom_as_string
