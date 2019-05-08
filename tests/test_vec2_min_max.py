
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time, math
import doctest

sys.path.append("..")
from mas.geometry import vec2_min_max

def test_vec2_min_max() :
    '''
    >>> test_vec2_min_max()
    fit (1.0, 1.0)'s length into [1.0, 1.5] : (1.00, 1.00)
    fit (1.0, 1.0)'s length into [0.5, 1.0] : (0.71, 0.71)
    fit (1.0, 1.0)'s length into [1.5, 2.0] : (1.06, 1.06)
    fit (-1.0, -1.0)'s length into [0.0, 0.5] : (-0.35, -0.35)
    '''
    print("fit (1.0, 1.0)'s length into [1.0, 1.5] : (%.2f, %.2f)" % vec2_min_max((1.0, 1.0), 1.0, 1.5))
    print("fit (1.0, 1.0)'s length into [0.5, 1.0] : (%.2f, %.2f)" % vec2_min_max((1.0, 1.0), 0.5, 1.0))
    print("fit (1.0, 1.0)'s length into [1.5, 2.0] : (%.2f, %.2f)" % vec2_min_max((1.0, 1.0), 1.5, 2.0))
    print("fit (-1.0, -1.0)'s length into [0.0, 0.5] : (%.2f, %.2f)" % vec2_min_max((-1.0, -1.0), 0.0, 0.5))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_min_max Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
