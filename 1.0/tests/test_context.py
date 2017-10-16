#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_context() :
    '''
    >>> test_context()
    intention: {'1': {'transmit': 'message', 'listen': ''}, '0': {'listen': '', 'angle': '', 'avel': '', 'time': ''}}
    confirm: {'1': {'listen_result': ['message']}, '0': {'listen_result': ['message'], 'time_result': 0.02, 'angle_result': 0.0, 'avel_result': 0.0}}
    '''
    context = Context(delta = 1.0 / 50.0, units = {Unit(name = "0"), Unit(name = "1")})
    intention = {"0" : {"time" : "", "avel" : "", "angle" : "", "listen" : ""}, "1" : {"transmit" : "message", "listen" : ""}}
    print("intention: %s" % intention)
    confirm = context.judge(intention = intention)
    print("confirm: %s" % confirm)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Context Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 


