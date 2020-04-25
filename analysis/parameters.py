"""

Title : parameters.py
Author : Magnus Fyhr
Created : 01/26/2020

Purpose :

TO-DO :
    - move system logging, console output, and system debug somewhere else

"""

SUPP_TICKERS = [
<<<<<<< HEAD
    "MSFT",
    "TEST",
=======
>>>>>>> d29cf94316e7c1f36aa8ea01d912703eaa951d78
    "AMD",
    "BK",
    "CI",
    "DD",
    "DVN",
    "ED",
    "IBM",
    "KO",
    "MRO",
    "PG"
<<<<<<< HEAD

=======
    "TEST"
>>>>>>> d29cf94316e7c1f36aa8ea01d912703eaa951d78
]

""" SYSTEM LOGGING """


"""" CONSOLE LOGGING """
SIMULATION_CONSOLE = list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
HABITAT_CONSOLE = list([2, 3])
ACCOUNT_CONSOLE = list([3])
DATABOOK_CONSOLE = list([2, 3])
POPULATION_CONSOLE = list([4])

""" SYSTEM DEBUG """
HABITAT_DEBUG = list([5, 6, 7, 8, 9, 10])
DATABOOK_DEBUG = list([6, 7, 8, 9, 10])
POPULATION_DEBUG = list([7, 8, 9, 10])
INDIVIDUAL_DEBUG = list([8, 9, 10])
ACCOUNT_DEBUG = list([9, 10])
CHROM_DEBUG = list([10])


""" ALLELE """
ALLELE_POSITION_MUT_PROB = 0.25
ALLELE_TECH_IND_MUT_PROB = 0.25
ALLELE_THRESH_MUT_PROB = 0.80
ALLELE_THRESH_VOLATILITY = 0.10
ALLELE_THRESH_RAND_MAX = 200
ALLELE_THRESH_RAND_MIN = -200
ALLELE_CONDITION_MUT_PROB = 0.25
ALLELE_POWER_MUT_PROB = 0.25
ALLELE_CROSS_DOMINANCE = 3


""" CHROMOSOME """
CHROM_HOLD_OR_EXIT = "EXIT"
CHROM_LIMIT_MUT_PROB = 0.25
CHROM_LIMIT_VOLATILITY = 0.10
CHROM_CROSS_DOMINANCE = 3
CHROM_LONG_SHORT_GAP = 0
CHROM_ALLELE_COUNT = 10


""" ACCOUNT """
ACCOUNT_TRADE_VOLUME = 1000
ACCOUNT_INIT_BALANCE = 10000.00
ACCOUNT_TRADE_COOL_DOWN = 0
ACCOUNT_MAX_STREAK = 3
ACCOUNT_STREAK_COOL_DOWN = 3


""" INDIVIDUAL """


""" POPULATION  """
POP_SIZE = 1000
POP_ELITE_RATIO = 0.2


""" ENVIRONMENT (DATABOOK) """
GEN_COUNT = 100  # 50 generations @ 50 period; 2500 days of data; ~8 years of historical data
AVAIL_TECH_IND = dict()


""" HABITAT """  # 251 trading days per year
MAX_GEN = 1000
GEN_PERIOD = 30     # 50 days of trading

