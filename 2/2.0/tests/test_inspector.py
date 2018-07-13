
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_insp_basic() :
    '''
    >>> test_insp_basic()
    Initialization.
    Inspector: <<multiagent.Inspector delay=1 count=1>>
    Set delay to 0.
    Delay: 0
    Reset count.
    Count: 0
    '''
    print("Initialization.")
    insp = Inspector(delay = 1)
    print("Inspector: %s" % insp.info())
    print("Set delay to 0.")
    insp.delay = 0
    print("Delay: %d" % insp.delay)
    print("Reset count.")
    insp.reset()
    print("Count: %d" % insp.count)

def test_insp_check() :
    '''
    >>> test_insp_check()
    Initialization.
    Inspector: <<multiagent.Inspector delay=0 count=0>>
    Check: pass
    '''
    print("Initialization.")
    insp = Inspector(delay = 0)
    print("Inspector: %s" % insp.info())
    print("Check: %s" % insp.check(Shot()))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Inspector Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
