#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_timer_init() :
    '''
    >>> test_timer_init()
    Timer: <<multiagent.Timer read=0.0000 delta=0.0100>>
    '''
    timer = Timer()
    print("Timer: %s" % timer.info())
    
def test_timer_tick_tack() :
    '''
    >>> test_timer_tick_tack()
    Timer: <<multiagent.Timer read=0.0000 delta=0.0100>>
    Tick
    Read: 0.0100
    Tack
    Read: 0.0000
    '''
    timer = Timer()
    print("Timer: %s" % timer.info())
    print("Tick")
    timer.tick()
    print("Read: %.4f" % timer.read)
    print("Tack")
    timer.tack()
    print("Read: %.4f" % timer.read)



if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Timer Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



