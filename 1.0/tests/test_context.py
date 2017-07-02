#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_context() :
    '''
    >>> test_context()
    intention: {'1': {'transmit': 'message'}, '0': {'position': '', 'angle': '', 'time': ''}}
    confirm: {'1': {'receive': {'1': 'message'}}, '0': {'receive': {'1': 'message'}, 'pos_x': 0.0, 'pos_y': 0.0, 'angle': 0.0, 'timer': {'value': 0.02}}}
    '''
    context = Context(delta = 1.0 / 50.0, units = {Unit(name = "0"), Unit(name = "1")})
    intention = {"0" : {"time" : "", "position" : "", "angle" : ""}, "1" : {"transmit" : "message"}}
    print("intention: %s" % intention)
    confirm = context.judge(intention = intention)
    print("confirm: %s" % confirm)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Context Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 


