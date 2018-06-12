
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_timer_basic() :
    '''
    >>> test_timer_basic()
    Initialization.
    Timer: <<multiagent.Timer read=0.0000 delta=0.0100>>
    Change values of the properties.
    Delta: 0.0020
    Read: 0.0400
    '''
    print("Initialization.")
    timer = Timer()
    print("Timer: %s" % timer.info())
    print("Change values of the properties.")
    timer.delta = 0.002
    print("Delta: %.4f" % timer.delta)
    timer.read = 0.04
    print("Read: %.4f" % timer.read)

def test_timer_tick() :
    '''
    >>> test_timer_tick()
    Initialization.
    Timer: <<multiagent.Timer read=0.0000 delta=0.0100>>
    Tick
    Read: 0.0100
    '''
    print("Initialization.")
    timer = Timer()
    print("Timer: %s" % timer.info())
    print("Tick")
    timer.tick()
    print("Read: %.4f" % timer.read)



if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Timer Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
