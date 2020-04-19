"""

Title : main.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose :

TO-DO :

    - Sift through code and setup new console reporting system.
        + Simulator     :
        + Habitat       :
        + DataBook      :
        + Population    :

    - Finish Simulator
    - Test Account Class
    - Update README.md

Cleaning :
    - Optimizations
    - Add & Clean Comments Throughout Primary Code Base
    - Place Primary Code Base In a Sub-Directory; named 'algorithm' (after all branches are merged)
    - Fill in purposes for each class file header
    - Clean the following classes...
        + Habitat
        + Population
        + DataBook

TO-DO :


Comments :

    - Might want to check the debug test files; as a lot has changed
        + debug tests should test EVERY SINGLE FUNCTION; will need to enhance debug tests

    - helper files need to be optimized!

    - concerned about the set of alleles in a chromosome
        + is it ok to have multiple of the same tech_ind
        + what are the rules for chromosome crossovers
            * should they be forced to be diverse

    - rename 'simulation' directory to 'world' (after merge with Raaz's branch)
    - place all relevant directories in new 'simulation' directory
        + simulation
            + simulator
            + genetics
            + phenetics
            + world
            * settings.py
            * parameters.py

    - fix error messages to say what class the message is coming from

    - need to further understand technical indicators; and how to read them in order to code them

"""
# Debug Modes :
#  0 : Minimalistic Console Output                                  ***** ***** ***** *****
#       - Includes Generic Header Of Important Parameters                                       *****
#       - Useful For When Running Multiple Simulations At Once
#       - No Error Checking Anywhere
#  1 : 0 + Overall Simulation Progress                              ***** ***** ***** *****
#       - Includes Generic Header Of Important Parameters At Beginning Of Run                   *****
#       - Includes Detailed Description Of DataBook Being Used                                  *****
#       - Useful For When Running A Single Simulation
#       - Should Have Footer Message For Average Runtime, etc.
#       - Prints Progress & Completion Estimate
#       - No Error Checking Anywhere
#  2 : 1 + Habitat Console Reporting
#       - Generational Population Statistics
#       - Focuses On The Algorithm & Its Generational Status
#       - No Error Checking Anywhere
#  3 : 2 + Performance Console Reporting                            ***** ***** ***** *****
#       - Generational Account Performance & Relevant Statistics                                *****
#       - Focuses On The Financial Aspect Of Things
#       - No Error Checking Anywhere
#  4 : Specialized Runtime Debugger
#       - Outputs Population Level Runtimes To Console
#       - No Generational Statistics; JUST RUNTIMES
#       - No Error Checking Anywhere

#  5 : Habitat Error Checking
#  6 : 5 + DataBook Error Checking
#  7 : 6 + Population Error Checking
#  8 : 7 + Individual Error Checking
#  9 : 8 + Account Error Checking
# 10 : 9 + Allele & Chromosome Error Checking; Full System Debug Mode : doesn't work


# from analysis.simulator import simulator as sim
# simulator = sim.Simulator("MSFT", debug=2)
# simulator.run()

from analysis.experiment import experiment as exp

experiment = exp.Experiment(tickers=["AMD", "BK", "CI", "DD" "DVN", "ED", "IBM", "KO", "MRO", "PG", "MSFT"], sample_size=30, debug=1)
experiment.run()
