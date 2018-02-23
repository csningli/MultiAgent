#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_context_init() :
    '''
    >>> test_context_init()
    Context: <<multiagent.Context oracle=<<multiagent.OracleSpace objs=0 obts=0>>>>
    '''
    context = Context()
    print("Context: %s" % context.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Context Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



