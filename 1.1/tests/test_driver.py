#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_driver() :
    '''
    >>> test_driver()
    Driver: <<multiagent.Driver context=<<multiagent.Context oracle=<<multiagent.OracleSpace objs=0 obts=0>>>> schedule=<<multiagent.Schedule agents_num=0>> timer=<<multiagent.Timer read=0.0000 delta=0.0100>> agents_num=0>>
    '''
    context = Context()
    schedule = Schedule()
    driver = Driver(context = context, schedule = schedule)
    print("Driver: %s" % driver.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Driver Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



