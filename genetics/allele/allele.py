"""

Title : allele.py

Purpose : The Allele class object, responsible for providing proper
            functions and expected functionality for the Allele.

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
    - init          :
    - hydrate       :
    - dehydrate     :
    - verify        :
    - mutate        :
    - crossover     :
    - react         :
    - as_string     :

"""
from genetics.allele.helper import allele_structure

from genetics.allele.helper import allele_build as ale_bui

from genetics.allele.helper import allele_decode as ale_dec
from genetics.allele.helper import allele_encode as ale_enc

from genetics.allele.helper import allele_mutate as ale_mut
from genetics.allele.helper import allele_crossover as ale_cro


""" Mutation Variables """
POS_MUT_PROB = 0.25
TECH_IND_MUT_PROB = 0.25
THRESHOLD_MUT_PROB = 0.25
THRESHOLD_VOLATILITY = 0.10
CONDITION_MUT_PROB = 0.25
POWER_MUT_PROB = 0.25


class Allele(object):

    """
    Initialize & Verify The Allele
    """
    def __init__(self, encoding=None):

        if encoding is None:
            encoding = ale_bui.random_encoding()

        # Initialize class variables to default
        self.initialized = False
        self.encoding = encoding
        self.position = None
        self.tech_ind = None
        self.threshold = None
        self.condition = None
        self.power = None

        # Hydrate The Allele (Initialize)
        if self.hydrate() is None:
            print("< ERR > : Failed to hydrate allele, invalid encoding! {}".format(encoding))
            return

        # Verify The Allele
        if self.verify() is False:
            print("< ERR > : Failed to verify allele, invalid encoding! {}".format(encoding))
            return

        # Done Initializing
        self.initialized = True
        return

    """
    Initializes Variables For Allele From Encoding
    """
    def hydrate(self):
        # Sanity Check
        if self.encoding is None:
            return None

        # Decode Position (buy:sell)
        self.position = ale_dec.decode_position(self.encoding)

        # Decode Technical Indicator
        self.tech_ind = ale_dec.decode_tech_ind(self.encoding)

        # Decode Threshold (for technical indicator)
        self.threshold = ale_dec.decode_threshold(self.encoding)

        # Decode Condition
        self.condition = ale_dec.decode_condition(self.encoding)

        # Decode Power (of decision)
        self.power = ale_dec.decode_power(self.encoding)

        return 1

    """
    Encodes & Returns The Current State Of The Allele
    """
    def dehydrate(self):

        # Encode Position (buy:sell)
        position = ale_enc.encode_position(self.position)

        # Encode Technical Indicator
        tech_ind = ale_enc.encode_tech_ind(self.tech_ind)

        # Encode Threshold (for technical indicator)
        threshold = ale_enc.encode_threshold(self.threshold)

        # Encode Condition
        condition = ale_enc.encode_condition(self.condition)

        # Encode Power (of decision)
        power = ale_enc.encode_power(self.power)

        # Check That All Passed Encoding
        if position is None or tech_ind is None or threshold is None\
                or condition is None or power is None:
            print("< ERR > : Failed to dehydrate allele, invalid allele state!")
            return None

        # Form Encoding
        encoding = position + tech_ind + threshold + condition + power

        # Return Encoding
        return encoding

    """
    Verifies The Initialization Of An Allele
    """
    def verify(self):
        # Verify Encoding
        if len(self.encoding) is not allele_structure.ENCODING_SIZE:
            return None

        # Verify Position
        if self.position is None:
            return False

        # Verify Technical Indicator
        if self.tech_ind is None:
            return False

        # Verify Threshold
        if self.threshold is None:
            return False

        # Verify Condition
        if self.condition is None:
            return False

        # Verify Power
        if self.power is None:
            return False

        # Passed Verification
        return True

    """
    Mutates The State Of The Current Allele & Returns A Mutation Of The Allele As An Encoding
    """
    def mutate(self, radiation=1.0):

        # Mutate Position
        mut_position = ale_mut.mutate_position(self.position, POS_MUT_PROB * radiation)

        # Mutate Technical Indicator
        mut_tech_ind = ale_mut.mutate_tech_ind(self.tech_ind, TECH_IND_MUT_PROB * radiation)

        # Mutate Threshold
        mut_size = self.threshold * THRESHOLD_VOLATILITY
        mut_threshold = ale_mut.mutate_threshold(self.threshold, THRESHOLD_MUT_PROB * radiation, mut_size)

        # Mutate Condition
        mut_condition = ale_mut.mutate_condition(self.condition, CONDITION_MUT_PROB * radiation)

        # Mutate Power
        mut_power = ale_mut.mutate_power(self.power, POWER_MUT_PROB * radiation)
        if mut_power == 10:
            print("mutate power = 10")

        # Check That All Passed Mutation
        if mut_position is None or mut_tech_ind is None or mut_threshold is None\
                or mut_condition is None or mut_power is None:
            print("< ERR > : Failed to mutate allele, invalid allele state!")
            return None

        # Form Mutated Encoding
        enc_pos = ale_enc.encode_position(mut_position)
        enc_ti = ale_enc.encode_tech_ind(mut_tech_ind)
        enc_thresh = ale_enc.encode_threshold(mut_threshold)
        enc_cond = ale_enc.encode_condition(mut_condition)
        enc_power = ale_enc.encode_power(mut_power)

        # Check That All Passed Encoding
        if enc_pos is None or enc_ti is None or enc_thresh is None\
                or enc_cond is None or enc_power is None:
            print("< ERR > : Failed to encode mutated allele, invalid mutation variables!")
            return None

        mut_encoding = enc_pos + enc_ti + enc_thresh + enc_cond + enc_power

        # Apply Mutation
        self.encoding = mut_encoding
        self.position = mut_position
        self.tech_ind = mut_tech_ind
        self.threshold = mut_threshold
        self.condition = mut_condition
        self.power = mut_power

        # Verify Mutation
        if self.verify() is False:
            print("< ERR > : Failed to verify allele, invalid mutation! {}".format(mut_encoding))
            return

        # Return Mutated Encoding
        return mut_encoding

    """
    Returns Two Offspring Encodings From Crossover(s) Between Two Parent Alleles
    """
    def crossover(self, mate_allele):

        # Define 'dominance'
        dominance = 2  # this will incur a 3:1 dominance of allele_a over allele_b in crossover

        # Obtain parent encodings
        encoding_a = self.encoding
        encoding_b = mate_allele.encoding

        # Create offspring
        offspring_a = ale_cro.crossover(encoding_a, encoding_b, dominance)
        offspring_b = ale_cro.crossover(encoding_b, encoding_a, dominance)

        # Return offspring
        return [offspring_a, offspring_b]

    """
    Returns A Reaction From The Allelex
    """
    def react(self, input_data):

        # Verify Input Data
        try:
            int(input_data)

        except ValueError:
            # Otherwise, return NoneType
            print("< ERR > : Error in allele reaction, invalid input data! {}".format(input_data))
            return None

        if self.condition == '<':  # Less Than

            if input_data < self.threshold:  # Condition Met
                return 1 + self.power

            return 0  # Condition Not Met

        elif self.condition == '>':  # Greater Than

            if input_data > self.threshold:  # Condition Met
                return 1 + self.power

            return 0  # Condition Not Met

        # Allele Corrupted
        print("< ERR > : Error in allele reaction, invalid condition! {}".format(self.condition))
        return None

    """
    Returns String Representation Of The Allele
    """
    def as_string(self):
        position = "SELL"
        if self.position == 1:
            position = "BUY"

        return "if ( {}(t) {} {} ) -> VOTE {}({})".format(self.tech_ind,
                                                          self.condition,
                                                          self.threshold,
                                                          position,
                                                          self.power + 1)
