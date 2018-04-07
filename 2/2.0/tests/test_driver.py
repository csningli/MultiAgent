
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_driver() :
    '''
    >>> test_driver()
    Driver: <<multiagent.Driver has_context=1 has_schedule=1 has_timer=1 agents_num=0>>
    '''
    context = Context()
    schedule = Schedule()
    driver = Driver(context = context, schedule = schedule)
    print("Driver: %s" % driver.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Driver Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
