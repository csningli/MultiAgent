#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_context_init() :
    '''
    >>> test_context_init()
    Context: <<multiagent.Context has_oracle=1>>
    Add object: <<multiagent.Object name=0>>
    Oracle: <<multiagent.OracleSpace objs_num=1 obts_num=0>>
    Add object: <<multiagent.Object name=1>>
    Oracle: <<multiagent.OracleSpace objs_num=2 obts_num=0>>
    Add obstacle: <<multiagent.Obstacle name=0>>
    Oracle: <<multiagent.OracleSpace objs_num=2 obts_num=1>>
    '''
    oracle = OracleSpace()
    context = Context(oracle = oracle)
    print("Context: %s" % context.info())
    obj = Object(name = "0")
    print("Add object: %s" % obj.info())
    context.add_obj(obj)
    print("Oracle: %s" % oracle.info())
    obj = Object(name = "1")
    print("Add object: %s" % obj.info())
    context.add_obj(obj)
    print("Oracle: %s" % oracle.info())
    obt = Obstacle(name ="0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0)
    print("Add obstacle: %s" % obt.info())
    context.add_obt(obt)
    print("Oracle: %s" % oracle.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Context Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



