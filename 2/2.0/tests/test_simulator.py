
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_sim_basic() :
    '''
    >>> test_sim_basic()
    Initialization.
    Simulator: <<multiagent.Simulator has_driver=1>>
    '''
    print("Initialization.")
    driver = Driver(context = Context(), schedule = Schedule())
    sim = Simulator(driver = driver)
    print("Simulator: %s" % sim.info())

def test_sim_sim() :
    '''
    >>> test_sim_sim()
    Initialization.
    Simulator: <<multiagent.Simulator has_driver=1>>
    Simulate.
    '''
    print("Initialization.")
    driver = Driver(context = Context(), schedule = Schedule())
    sim = Simulator(driver = driver)
    print("Simulator: %s" % sim.info())
    print("Simulate.")
    sim.simulate(limit = 1, filename = "")



if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Simulator Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
