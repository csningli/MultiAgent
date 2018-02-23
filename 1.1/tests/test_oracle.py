#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_oracle_init() :
    '''
    >>> test_oracle_init()
    Oracle: <<multiagent.OracleSpace objs=0 obts=0>>
    '''
    oracle = OracleSpace()
    print("Oracle: %s" % oracle.info())

def test_oracle_add() :
    '''
    >>> test_oracle_add()
    Oracle: <<multiagent.OracleSpace objs=1 obts=1>>
    Add Object: <<multiagent.Object name=obj2>>
    Oracle: <<multiagent.OracleSpace objs=2 obts=1>>
    Add Obstacle: <<multiagent.Obstacle name=obt2>>
    Oracle: <<multiagent.OracleSpace objs=2 obts=2>>
    Oracle Clear
    Oracle: <<multiagent.OracleSpace objs=0 obts=0>>
    '''
    oracle = OracleSpace(
            objs = [Object(name = "obj1"),], 
            obts = [Obstacle(name = "obt1", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0)])
    print("Oracle: %s" % oracle.info())
    obj = Object(name = "obj2")
    print("Add Object: %s" % obj.info())
    oracle.add_obj(obj)
    print("Oracle: %s" % oracle.info())
    obt = Obstacle(name = "obt2", a = (0.0, -1.0), b = (1.0, 0.0), radius = 2.0)
    print("Add Obstacle: %s" % obt.info())
    oracle.add_obt(obt)
    print("Oracle: %s" % oracle.info())
    print("Oracle Clear")
    oracle.clear()
    print("Oracle: %s" % oracle.info())

def test_oracle_get() :
    '''
    >>> test_oracle_get()
    Oracle: <<multiagent.OracleSpace objs=0 obts=0>>
    '''
    oracle = OracleSpace()
    print("Oracle: %s" % oracle.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Oracle Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



