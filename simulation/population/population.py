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
    - initialize_dist_population    :

Testing :
    - init                          :
    - step                          :
    - verify                        :
    - next_generation               :
    - evaluate                      :
    - reproduce                     :
    - modify                        :
    - metrics                       :
    - status                        :
    - initialize_rand_population    :
    - initialize_dist_population    :

Cleaning :
    - init                          :
    - step                          :
    - verify                        :
    - next_generation               :
    - evaluate                      : DONE
    - reproduce                     : DONE
    - modify                        : DONE
    - metrics                       : DONE
    - status                        : DONE
    - initialize_rand_population    : DONE
    - initialize_dist_population    :

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
    - initialize_dist_population    :

TO-DO :
    - make population initialization not random (parameter!!!):
        + Should be evenly distributed across alleles then chromosomes
        + numbers spread out by some standard deviation
        + numbers could be given a default value that represents the center of the distribution


Comments :
    - reproduce(): does parents list need to be copied;
        - all copying should actually be removed
    - should observation be verified in step?

Future Improvements :


"""

import analysis.parameters as params

import simulation.population.helper.pop_generate as pop_gen
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

        self.open_date = None
        self.close_date = None
        self.open_price = None
        self.close_price = None

        # Initialization
        self.size = pop_size
        self.elite_count = int(pop_size * params.POP_ELITE_RATIO)
        self.citizens = pop_gen.generate_normal_population(pop_size, self._debug_mode)

        # Setup Debug Mode
        self._debug_mode = debug
        if debug in params.POPULATION_DEBUG:
            self._is_debug = True

        # Verify Population
        if self._is_debug:
            if not self.verify():
                print("< ERR > : Population : Failed to initialize Population; verification failed!")
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
        # Verify Observation
        if self._is_debug:
            pass

        # If First Step Of Generation; Update Birth Date
        if self.step_count == 0:
            self.open_date = observation['Date']
            self.open_price = observation['Close']

        # Simulate Step Across Each Population Member
        for citizen in self.citizens:
            # simulate step on citizen
            citizen.step(observation)
            # increment iteration count; tracks total steps taken; pop_size * gen_count
            self.iter_count += 1

        # Track Last Date Data Was Simulated
        self.close_date = observation['Date']
        self.close_price = observation['Close']

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
        if self._is_debug and self.gen_count > 0:
            for key, stat in statistics.items():
                if stat is None:
                    print("< WRN > : Population : Failed to obtain metrics(); "
                          "NoneType found! ({})".format(key))

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

        offspring = self.reproduce(parents)
        # Optional Debug Step
        if self._is_debug:
            if len(offspring) != self.size - self.elite_count:
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
            if len(offspring) != self.size - self.elite_count:
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
        citizens = list([])
        for elite in elites:
            elite.refresh()
            citizens.append(elite)
        citizens.extend([indiv.Individual(chromosome=chromosome, debug=self._debug_mode) for chromosome in offspring])
        self.citizens = citizens

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
        self.open_date = None
        self.close_date = None
        self.open_price = None
        self.close_price = None

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
    def reproduce(self, parents):
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
        offspring = offspring[:len(offspring) - self.elite_count]
        # offspring.extend([elite.clone() for elite in elites])

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
        statistics["pop_size"] = self.size
        statistics["gen_count"] = self.gen_count
        statistics["step_count"] = self.step_count
        statistics["iter_count"] = self.iter_count
        statistics["open_date"] = self.open_date
        statistics["close_date"] = self.close_date
        statistics["open_price"] = self.open_price
        statistics["close_price"] = self.close_price
        statistics["market_fit"] = self.close_price / self.open_price

        # Return Dictionary Object
        return statistics

    """
    Returns Dictionary Representation Of Population's Current State; Useful For System Testing
    """
    def status(self):
        # Format Population Into Dictionary Object
        state = {
            "init": self.initialized,
            "debug_mode": self._debug_mode,
            "is_debug": self._is_debug,

            "gen_count": self.gen_count,
            "iter_count": self.iter_count,

            "pop_size": self.size,
            "members": [individual.status() for individual in self.citizens],
            "elite_count": self.elite_count,
            "elites": [individual.status() for individual in self.citizens if individual.is_elite]
        }

        # Return Dictionary Object
        return state
