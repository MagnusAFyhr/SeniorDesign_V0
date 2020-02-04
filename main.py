"""

Title : main.py
Author : Magnus Fyhr
Created : 11/22/2019

Purpose :



"""
# Debug Modes :
# 0 : Only Overall Simulation Progress; No Verifications Anywhere
# 1 : 0 +  Habitat Generational Statistics; No Verifications Anywhere
# 2 : 1 + Population Debug Console Logs; No Verification Anywhere
# 3 : 2 + Individual & Account Console Logs; WHAT ELSE                              ***** ***** *****
# 4 : Full System Debugging To Console; Genetic, Phenetic, Simulation Verification  ***** ***** *****
# 5 : Specialized Runtime Debugger, No Generational Statistics JUST RUNTIMES; No Verification Anywhere

from analysis.simulator import simulator as sim

simulator = sim.Simulator("MSFT", debug=1)
simulator.run_simulation()
