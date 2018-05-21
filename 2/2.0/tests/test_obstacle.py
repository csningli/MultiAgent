
# MultiAgent 2.0
# copyright (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_obt() :
    '''
    >>> test_obt()
    Obstacle: <<multiagent.Obstacle name=test_obt>>
    A: (0.0, 1.0)
    B: (1.0, 0.0)
    Radius: 2.0
    Ends: (0.0, 1.0), (1.0, 0.0)
    '''
    obt = Obstacle(name ="test_obt", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0)
    print("Obstacle: %s" % obt.info())
    print("A: (%.1f, %.1f)" % (obt.a[0], obt.a[1]))
    print("B: (%.1f, %.1f)" % (obt.b[0], obt.b[1]))
    print("Radius: %.1f" % obt.radius)
    print("Ends: (%.1f, %.1f), (%.1f, %.1f)" % (obt.a[0], obt.a[1], obt.b[0], obt.b[1]))


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Obstacle Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
