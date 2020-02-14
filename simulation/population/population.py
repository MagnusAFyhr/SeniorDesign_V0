"""

Title : population.py
Author : Magnus Fyhr
Created : 12/17/2019

Purpose : The Population class object, responsible for simulating a defined
            set of Individuals generationally, implementing proper Darwinian
            evolution.

Development :
    - init                          : DONE
    - step                          : DONE
    - verify                        : DONE
    - next_generation               : DONE
    - evaluate                      : DONE
    - reproduce                     : DONE
    - modify                        : DONE
    - metrics                       : DONE
    - status                        : DONE
    - initialize_rand_population    : DONE

Testing :
    - init                          : DONE
    - step                          : DONE
    - verify                        :
    - next_generation               : DONE
    - evaluate                      : DONE
    - reproduce                     : DONE
    - modify                        : DONE
    - metrics                       : DONE
    - status                        :
    - initialize_rand_population    : DONE

Cleaning :
    - init                          : DONE
    - step                          : DONE
    - verify                        : DONE
    - next_generation               : DONE
    - evaluate                      : DONE
    - reproduce                     : DONE
    - modify                        : DONE
    - metrics                       : DONE
    - status                        : DONE
    - initialize_rand_population    : DONE

Optimizing :
    - init                          :
    - step                          :
    - verify                        :
    - next_generation               :
    - evaluate                      :
    - reproduce                     :
    - modify                        :
    - metrics                       :
    - initialize_rand_population    :

TO-DO :
    - make population initialization not random (parameter!!!):
        + Should be evenly distributed
        + numbers spread out by some standard deviation
        + numbers could be given a default value that represents the center of the distribution


Comments :
    - check the pop_evaluate file; make sure that the rank_individuals function is working properly

    - evaluate() : relatively slow; see if it can be optimized
    - metrics()  : relatively slow; see if it can be optimized
    - reproduce(): does parents list need to be copied

    - does more diversity need to be tracked?
        + chromosome diversity should be tracked!!!
        + should average diversity across all allele variables? might be costly

Future Improvements :


"""

import analysis.parameters as params

import simulation.population.helper.pop_evaluate as pop_eval
import simulation.population.helper.pop_statistics as pop_stat

import genetics.chromosome.chromosome as chrom
import phenetics.individual.individual as indiv

import time


class Population:

    """
    Initialize Population
    """
    def __init__(self, pop_size, debug=0):

        # Pre-Initialization
        self.initialized = False
        self._debug_mode = 0
        self._is_debug = False

        self.gen_count = 0
        self.step_count = 0
        self.iter_count = 0
        self.birth_date = None
        self.last_date = None

        # Initialization
        self.size = pop_size
        self.elite_count = int(pop_size * params.POP_ELITE_RATIO)
        self.citizens = self.initialize_random_population(pop_size)

        # Setup Debug Mode
        self._debug_mode = debug
        if debug in params.POPULATION_DEBUG:
            self._is_debug = True

        # Verify Population
        if self._is_debug:
            if not self.verify():
                print("< ERR > : Failed to initialize Population; verification failed!")
                return

        # Done Initializing!
        self.initialized = True
        return

    """
    Verify Population
    """
    def verify(self):
        # Check That Population Size Is Correct
        if self.size != len(self.citizens):
            return False

        # Check Elite Count Is Less Than Population Size
        if self.elite_count > self.size:
            return False

        # Check That All Citizens Are Initialized
        for individual in self.citizens:
            if not individual.initialized:
                return False

        # Verification Complete!
        return True

    """
    Simulates A Step In The Population With A Given Observation
    """
    def step(self, observation):
        # If First Step Of Generation; Update Birth Date
        if self.step_count == 0:
            self.birth_date = observation['Date']

        # Simulate Step Across Each Population Member
        for citizen in self.citizens:
            # simulate step on citizen
            citizen.step(observation)
            # increment iteration count; tracks total steps taken; pop_size * gen_count
            self.iter_count += 1

        # Track Last Date Data Was Simulated
        self.last_date = observation['Date']

        # Step Complete; Increment Step Count!
        self.step_count += 1
        return

    """
    Generates The Next Population
    """
    def next_generation(self):
        #
        # Obtain Population Statistics
        #
        if self._is_debug:
            print("\t\t< POP > : Calculating Population Statistics...")
        start_t = time.time_ns()

        statistics = self.metrics()
        # Optional Debug Step
        if self._is_debug:
            for key, stat in statistics.items():
                if stat is None:
                    print("< ERR > : Population : Failed to obtain metrics(); "
                          "NoneType found! ({})".format(key))
                    return None

        end_t = time.time_ns()
        elapsed = end_t - start_t
        elapsed /= pow(10, 9)
        if self._debug_mode in params.POPULATION_CONSOLE:
            print("\t\t< POP > : Calculated Population Statistics\t\t\t\t\t\t: {} s.".format(elapsed))

        #
        # Obtain Elites & Parents From Current Population
        #
        if self._is_debug:
            print("\t\t< POP > : Evaluating Population; Selecting Elites & Parents...")
        start_t = time.time_ns()

        elites, parents = self.evaluate()
        # Optional Debug Step
        if self._is_debug:
            if len(elites) != self.elite_count or len(parents) != self.size:
                print("< ERR > : Population : Failed to evaluate(); "
                      "elites or parents size is off! ({},{}).".format(len(elites), len(parents)))
                return None

        end_t = time.time_ns()
        elapsed = end_t - start_t
        elapsed /= pow(10, 9)
        if self._debug_mode in params.POPULATION_CONSOLE:
            print("\t\t< POP > : Evaluated Population; Selected Elites & Parents\t\t: {} s.".format(elapsed))

        #
        # Create Offspring Using Parents
        #
        if self._is_debug:
            print("\t\t< POP > : Producing Offspring; Applying Crossovers...")
        start_t = time.time_ns()

        offspring = self.reproduce(elites, parents)
        # Optional Debug Step
        if self._is_debug:
            if len(offspring) != self.size:
                print("< ERR > : Population : Failed to reproduce(); "
                      "offspring size is off! ({})".format(len(offspring)))
                return None

        end_t = time.time_ns()
        elapsed = end_t - start_t
        elapsed /= pow(10, 9)
        if self._debug_mode in params.POPULATION_CONSOLE:
            print("\t\t< POP > : Produced Offspring; Applied Crossovers\t\t\t\t: {} s.".format(elapsed))

        #
        # Apply Mutations To Offspring
        #
        if self._is_debug:
            print("\t\t< POP > : Modifying Offspring; Applying Mutations...")
        start_t = time.time_ns()

        offspring = self.modify(offspring)
        # Optional Debug Step
        if self._is_debug:
            if len(offspring) != self.size:
                print("< ERR > : Population : Failed to modify(); offspring size is off!")
                return None
            for child in offspring:
                if not child.initialized:
                    print("< ERR > : Population : Failed to modify(); Offspring contains bad Chromosome!")
                    return None

        end_t = time.time_ns()
        elapsed = end_t - start_t
        elapsed /= pow(10, 9)
        if self._debug_mode in params.POPULATION_CONSOLE:
            print("\t\t< POP > : Modified Offspring; Applied Mutations\t\t\t\t\t: {} s.".format(elapsed))

        #
        # Create New Set Of Citizens In Population
        #
        if self._is_debug:
            print("\t\t< POP > : Initializing Next Population...")
        start_t = time.time_ns()

        self.citizens.clear()
        self.citizens = [indiv.Individual(chromosome=chromosome, debug=self._debug_mode) for chromosome in offspring]
        # Optional Debug Step
        if self._is_debug:
            if len(self.citizens) != self.size:
                print("< ERR > : Population : Failed to initialize next population; "
                      "population size is off! ({})".format(len(self.citizens)))
                return None
            for member in self.citizens:
                if not member.initialized:
                    print("< ERR > : Population : Failed to initialize next population; "
                          "Citizens contains bad Individual!")
                    return None

        end_t = time.time_ns()
        elapsed = end_t - start_t
        elapsed /= pow(10, 9)
        if self._debug_mode in params.POPULATION_CONSOLE:
            print("\t\t< POP > : Initialized Next Population\t\t\t\t\t\t\t: {} s.".format(elapsed))

        # Reset Generational Tracker Variables
        self.step_count = 0
        self.gen_count += 1
        self.birth_date = None
        self.last_date = None

        # Next Generation Ready; Return Previous Generation Statistics!
        return statistics

    """
    Selection Mechanism For The Population 
    """
    def evaluate(self):
        # Determine Elites & Parents For Offspring; Return [Elites, Parents]
        return pop_eval.evaluate_individuals(self.citizens, self.elite_count)

    """
    Reproduction Mechanism For The Population 
    """
    def reproduce(self, elites, parents):
        # Copy List Of Parents
        pool = parents.copy()

        # Create Empty List For Future Offspring
        offspring = list([])

        # Iterate Until There Are No Longer At Least Two Parents
        while len(pool) > 1:
            # select alpha parent; remove from list
            parent_a = pool.pop()

            # select beta parent; remove from list
            parent_b = pool.pop()

            # create offspring pair
            pair = parent_a.mate(parent_b)

            # append offspring to list
            offspring.extend(pair)

            # advance to next iteration
            continue

        # Trim Off N Trailing Chromosomes; Append N Elites To Offspring
        offspring = offspring[:len(offspring) - len(elites)]
        offspring.extend([elite.clone() for elite in elites])

        # Reproduction Complete; Return Offspring!
        return offspring

    """
    Mutation Operator For The Population
    """
    def modify(self, offspring):
        # Create Empty List For Future Mutated Offspring
        mod_offspring = list([])

        # Iterate Through Offspring; Apply Mutations & Initialize New Chromosomes
        for chromosome in offspring:
            encoding = chromosome.mutate()
            mod_chromosome = chrom.Chromosome(encoding, debug=self._debug_mode)
            mod_offspring.append(mod_chromosome)

        # Return Mutated Offspring
        return mod_offspring

    """
    Calculate The Population Metrics
    """
    def metrics(self):
        # Calculate Statistics & Place In Dictionary Object
        statistics = pop_stat.population_statistics(self.citizens)
        statistics["gen_count"] = self.gen_count
        statistics["step_count"] = self.step_count
        statistics["iter_count"] = self.iter_count
        statistics["start_date"] = self.birth_date
        statistics["end_date"] = self.last_date

        # Return Dictionary Object
        return statistics

    """
    Returns Dictionary Representation Of Population's Current State
    """
    def status(self):
        # Format Population Into Dictionary Object
        state = {
            "init": self.initialized,
            "gen_count": self.gen_count,
            "iter_count": self.iter_count,
            "pop_size": self.size,
            "elite_count": self.elite_count,
            "members": [individual.status() for individual in self.citizens]
        }

        # Return Dictionary Object
        return state

    """
    Initialize A Random Population Of Individuals 
        - might want to implement logic to force evenly distributed population
    """
    def initialize_random_population(self, pop_size):
        # Create Empty List
        random_pop = list([])

        # Initialize & Append Random Individuals
        for i in range(0, pop_size):
            random_pop.append(indiv.Individual(debug=self._debug_mode))

        # Return Random Population
        return random_pop
