"""

Title : allele.py
Author : Magnus Fyhr
Created : 11/20/2019

Purpose : A class responsible for encoding a technical indicator.

Development :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     : DONE
    - react         :
    - status        : DONE
    - as_string     : DONE

Testing :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     : DONE (further testing needed after pending update)
    - react         : DONE (further testing needed after pending update)
    - status        : DONE
    - as_string     : DONE

Cleaning :
    - init          : DONE
    - hydrate       : DONE
    - dehydrate     : DONE
    - verify        : DONE
    - mutate        : DONE
    - crossover     :
    - react         :
    - status        : DONE
    - as_string     :


TO-DO :
    - if 0 triggers happen then mutation should move towards the average value
    - add 'trigger_count' variable to track how and when an allele triggers an action.

Comments :
    - good idea to clean, organize, optimize, comment, etc. all the 'helper' functions/files for the Allele

Future Improvements :

"""
import analysis.parameters as params

from genetics.allele.helper import allele_structure as ale_str

from genetics.allele.helper import allele_build as ale_bui

from genetics.allele.helper import allele_decode as ale_dec
from genetics.allele.helper import allele_encode as ale_enc

from genetics.allele.helper import allele_react as ale_rct
from genetics.allele.helper import allele_mutate as ale_mut
from genetics.allele.helper import allele_crossover as ale_cro


class Allele(object):

    """
    Initialize & Verify The Allele
    """
    def __init__(self, encoding=None, debug=False):

        # Check Encoding
        if encoding is None:
            encoding = ale_bui.random_encoding()

        # Pre-Initialization
        self.initialized = False
        self._is_debug = debug

        self.encoding = encoding
        self.position = None
        self.tech_ind = None
        self.threshold = None
        self.condition = None
        self.power = None

        # Hydrate The Allele (Initialization)
        if not self.hydrate():
            print("< ERR > : Allele : Failed to hydrate Allele, invalid encoding! {}".format(encoding))
            return

        # Verify The Allele
        if self._is_debug:
            if self.verify() is False:
                print("< ERR > : Allele : Failed to verify Allele, invalid encoding! {}".format(encoding))
                return

        # Initialization Complete!
        self.initialized = True
        return

    """
    Initializes Variables For Allele From Encoding
    """
    def hydrate(self):
        # Sanity Check
        if self.encoding is None:
            return False

        # Decode Position (long:short)
        self.position = ale_dec.decode_position(self.encoding)

        # Decode Technical Indicator
        self.tech_ind = ale_dec.decode_tech_ind(self.encoding)

        # Decode Threshold (for technical indicator)
        self.threshold = ale_dec.decode_threshold(self.encoding)

        # Decode Condition
        self.condition = ale_dec.decode_condition(self.encoding)

        # Decode Power (of decision)
        self.power = ale_dec.decode_power(self.encoding)

        # Hydration Complete!
        return True

    """
    Encodes & Returns The Current State Of The Allele
    """
    def dehydrate(self):

        # Encode Position (long:short)
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
        if self._is_debug:
            if position is None or tech_ind is None or threshold is None\
                    or condition is None or power is None:
                print("< ERR > : Allele : Failed to dehydrate Allele, invalid Allele state!")
                return None

        # Form Encoding
        encoding = position + tech_ind + threshold + condition + power

        # Dehydration Complete; Return Encoding!
        return encoding

    """
    Verifies The Initialization Of An Allele
    """
    def verify(self):

        # Verify Encoding
        if len(self.encoding) is not ale_str.ENCODING_SIZE:
            return False

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

        # Verification Complete!
        return True

    """
    Mutates The State Of The Allele & Returns The Encoding Of This Mutation
    """
    def mutate(self, radiation=1.0):

        # Mutate Position
        mut_position = ale_mut.mutate_position(self.position,
                                               params.ALLELE_POSITION_MUT_PROB * radiation)

        # Mutate Technical Indicator
        mut_tech_ind = ale_mut.mutate_tech_ind(self.tech_ind,
                                               params.ALLELE_TECH_IND_MUT_PROB * radiation)

        # Mutate Threshold
        mut_threshold = ale_mut.mutate_threshold(self.threshold,
                                                 params.ALLELE_THRESH_MUT_PROB * radiation,
                                                 self.threshold * params.ALLELE_THRESH_VOLATILITY)

        # Mutate Condition
        mut_condition = ale_mut.mutate_condition(self.condition,
                                                 params.ALLELE_CONDITION_MUT_PROB * radiation)

        # Mutate Power
        mut_power = ale_mut.mutate_power(self.power,
                                         params.ALLELE_POWER_MUT_PROB * radiation)

        # Check That All Passed Mutation
        if self._is_debug:
            if mut_position is None or mut_tech_ind is None or mut_threshold is None\
                    or mut_condition is None or mut_power is None:
                print("< ERR > : Allele : Failed to mutate Allele, invalid Allele state!")
                return None

        # Encode Mutated Parameters
        enc_mut_pos = ale_enc.encode_position(mut_position)
        enc_mut_ti = ale_enc.encode_tech_ind(mut_tech_ind)
        enc_mut_thresh = ale_enc.encode_threshold(mut_threshold)
        enc_mut_cond = ale_enc.encode_condition(mut_condition)
        enc_mut_power = ale_enc.encode_power(mut_power)

        # Check That All Mutations Passed Encoding
        if self._is_debug:
            if enc_mut_pos is None or enc_mut_ti is None or enc_mut_thresh is None\
                    or enc_mut_cond is None or enc_mut_power is None:
                print("< ERR > : Allele : Failed to encode mutated Allele, invalid mutation variables!")
                return None

        # Form Mutated Encoding
        mut_encoding = enc_mut_pos + enc_mut_ti + enc_mut_thresh + enc_mut_cond + enc_mut_power

        # Apply Mutation To Itself
        self.encoding = mut_encoding
        self.position = mut_position
        self.tech_ind = mut_tech_ind
        self.threshold = mut_threshold
        self.condition = mut_condition
        self.power = mut_power

        # Verify Mutation
        if self._is_debug:
            if self.verify() is False:
                print("< ERR > : Allele : Failed to verify Allele, invalid mutation! {}".format(mut_encoding))
                return

        # Mutation Complete; Return Mutated Encoding!
        return mut_encoding

    """
    Returns Two Offspring Encodings From Crossover(s) Between Two Parent Alleles
    """
    def crossover(self, mate_allele):

        # Define 'dominance'; Incurs A 'n:1' Dominance Of Parent 1 Over Parent 2 In Crossover
        dominance = params.ALLELE_CROSS_DOMINANCE

        # Obtain Parent Encodings
        encoding_a = self.encoding
        encoding_b = mate_allele.encoding

        # Create Offspring
        offspring_a = ale_cro.crossover(encoding_a, encoding_b, dominance)
        offspring_b = ale_cro.crossover(encoding_b, encoding_a, dominance)

        # Crossover Complete; Return Offspring!
        return [offspring_a, offspring_b]

    """
    Returns A Reaction From The Allele
    """
    def react(self, close_price, raw_input_data):

        # Convert raw input data
        input_data = None
        try:
            if isinstance(raw_input_data, str):
                input_data = raw_input_data.strip('][').split(',')
                input_data = [float(data) for data in input_data]
            else:
                input_data = float(raw_input_data)

        except TypeError:
            print("< ERR > : Allele : Error in Allele reaction, invalid input data! {} : {}".format(
                raw_input_data, input_data
            ))
            print(type(input_data))
            return None

        # Verify Input Data
        if self._is_debug:
            try:
                if isinstance(input_data, list):
                    for data in input_data:
                        float(data)
                else:
                    float(input_data)

            except ValueError:
                # Otherwise, return NoneType
                print("< ERR > : Allele : Error in Allele reaction, invalid input data! {}".format(input_data))
                return None

        # Determine Reaction
        if isinstance(input_data, list):

            power = ale_rct.react(self, close_price, input_data) * self.position
            if self._is_debug:
                try:
                    int(power)
                    if power is None:
                        raise ValueError

                except ValueError:
                    print("< ERR > : Allele : Error in Allele reaction, invalid special reaction! {} : {}".format(
                        self.tech_ind, input_data
                    ))
            return power

        else:

            if self.condition == '<':  # Less Than

                if float(input_data) < self.threshold:  # Condition Met
                    return (1 + self.power) * self.position

                return 0  # Condition Not Met

            elif self.condition == '>':  # Greater Than

                if float(input_data) > self.threshold:  # Condition Met
                    return (1 + self.power) * self.position

                return 0  # Condition Not Met

        # Allele Corrupted; Sanity Check
        print("< ERR > : Allele : Error in Allele reaction, invalid condition! {}".format(self.condition))
        return None

    """
    Returns Dictionary Representation Of Allele's Current State
    """
    def status(self):
        # Format Allele Into Dictionary Object
        state = {
            "initialized": self.initialized,
            "encoding": self.encoding,
            "position": self.position,
            "tech_ind": self.tech_ind,
            "threshold": self.threshold,
            "condition": self.condition,
            "power": self.power,
            "mut_rate": {
                "position": params.ALLELE_POSITION_MUT_PROB,
                "tech_ind": params.ALLELE_TECH_IND_MUT_PROB,
                "threshold": params.ALLELE_THRESH_MUT_PROB,
                "thresh_volatility": params.ALLELE_THRESH_VOLATILITY,
                "condition": params.ALLELE_CONDITION_MUT_PROB,
                "power": params.ALLELE_POWER_MUT_PROB
            }
        }

        # Return Dictionary Object
        return state

    """
    Returns String Representation Of The Allele
    """
    def as_string(self):
        position = "SHORT"
        if self.position == 1:
            position = "LONG"

        return "if ( {}(t) {} {} ) -> VOTE {}({})".format(self.tech_ind,
                                                          self.condition,
                                                          self.threshold,
                                                          position,
                                                          self.power + 1)
