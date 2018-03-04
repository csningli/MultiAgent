#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_msg() :
    '''
    >>> test_msg()
    Message: <<multiagent.Message src=src dest=dest key=key value=value>>
    '''
    msg = Message(src = "src", dest = "dest", key = "key", value = "value")
    print("Message: %s" % msg.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Message Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



