#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_sim_init() :
    '''
    >>> test_sim_init()
    Simulator: <<multiagent.Simulator has_driver=1>>
    '''
    driver = Driver(context = Context(), schedule = Schedule())
    sim = Simulator(driver = driver)
    print("Simulator: %s" % sim.info())

def test_sim_sim() :
    '''
    >>> test_sim_sim()
    Simulate
    '''
    driver = Driver(context = Context(), schedule = Schedule())
    sim = Simulator(driver = driver)
    print("Simulate")
    sim.simulate(limit = 1)



if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Simulator Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



