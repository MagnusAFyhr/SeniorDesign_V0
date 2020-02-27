"""

Title : chrom_mutate.py

Purpose : Single function responsible for handling the mutation of a chromosome's encoding

Development :
    - should_mutate     : DONE
    - mutate_limit      : DONE
    - mutate_alleles    : DONE

Testing :
    - should_mutate     :
    - mutate_limit      :
    - mutate_alleles    :

"""
import random


def should_mutate(mutate_prob):
    """ Determine if mutation should occur """

    # Generate random floating point number between [0,1]
    result = random.random()
    if result < mutate_prob:
        # Mutation should occur
        return True

    # Otherwise, mutation should not occur
    return False


def mutate_limit(limit, mutate_prob, mutate_size):
    """ Obtains mutation of long/short limit """

    # Check if mutation should occur
    if not should_mutate(mutate_prob):
        # No mutation
        return limit

    # Verify limit is an int
    try:
        int(limit)

    except ValueError:
        # Otherwise, return NoneType
        print("< ERR > : Chromosome : Error mutating Chromosome : Invalid Limit : {}.".format(limit))
        return None

    # Mutate limit
    mut_limit = int(limit)
    mutate_size = abs(mutate_size)
    mutation = random.randint(-mutate_size, mutate_size)
    mut_limit += mutation

    # Return mutated long/short limit
    return mut_limit


def mutate_alleles(alleles, mutate_prob):
    """ Obtains mutated set of alleles """

    # Create empty list of mutated alleles
    mut_alleles = list([])

    # For each allele, try to perform mutation
    for allele in alleles:
        # See if mutation should be performed
        if should_mutate(mutate_prob):
            # Should mutate
            mut_allele = allele.mutate()

            # Verify that mutated allele is valid
            if mut_allele is not None:
                # Valid mutation, append to list
                mut_alleles.append(allele.mutate())

            else:
                # Otherwise, return NoneType
                print("< ERR > : Chromosome : Error mutating Chromosome : Invalid Allele mutation : {}.".format(allele.encoding))
                return None

        else:
            # Should not mutate
            mut_alleles.append(allele)

    # Return mutated alleles
    return mut_alleles
