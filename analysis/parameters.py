"""

Title : parameters.py
Author : Magnus Fyhr
Created : 01/26/2020

Purpose :

"""


""" ALLELE """
ALLELE_POSITION_MUT_PROB = 0.25
ALLELE_TECH_IND_MUT_PROB = 0.25
ALLELE_THRESH_MUT_PROB = 0.25
ALLELE_THRESH_VOLATILITY = 0.10
ALLELE_CONDITION_MUT_PROB = 0.25
ALLELE_POWER_MUT_PROB = 0.25

""" CHROMOSOME """
CHROM_LIMIT_MUT_PROB = 0.25
CHROM_LIMIT_VOLATILITY = 0.10

""" ACCOUNT """
ACCOUNT_DEFAULT_VOLUME = 1000
ACCOUNT_DEFAULT_BALANCE = 10000.00
ACCOUNT_DEFAULT_TRADE_COOL_DOWN = 3


""" INDIVIDUAL """


""" POPULATION  """


""" HABITAT """
# 251 trading days per year
MAX_GEN = 40        # 40 generations; 2000 days of data; ~8 years of historical data
GEN_PERIOD = 50     # 50 days of trading
POP_SIZE = 1000     # 1,000 individuals

