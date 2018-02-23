#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_sim_init() :
    '''
    >>> test_sim_init()
    Simulator: <<multiagent.Simulator driver=<<multiagent.Driver context=<<multiagent.Context oracle=<<multiagent.OracleSpace objs=0 obts=0>>>> schedule=<<multiagent.Schedule agents_num=0>> timer=<<multiagent.Timer read=0.0000 delta=0.0100>> agents_num=0>>>>
    '''
    driver = Driver(context = Context(), schedule = Schedule())
    sim = Simulator(driver = driver)
    print("Simulator: %s" % sim.info())

def test_sim_sim() :
    '''
    >>> test_sim_sim()
    '''
    driver = Driver(context = Context(), schedule = Schedule())
    sim = Simulator(driver = driver)
    print("Simulate")
    sim.simulate()



if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Simulator Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



