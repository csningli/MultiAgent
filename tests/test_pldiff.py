
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import pldiff

def test_pldiff() :
    '''
    >>> test_pldiff()
    difference from (0.0, 0.0) to ((1.0, 0.0), (0.0, 1.0)) : (0.50, 0.50)
    difference from (0.0, 0.0) to ((-1.0, 0.0), (0.0, -1.0)) : (-0.50, -0.50)
    '''
    print("difference from (0.0, 0.0) to ((1.0, 0.0), (0.0, 1.0)) : (%.2f, %.2f)" % pldiff((0.0, 0.0), (1.0, 0.0), (0.0, 1.0)))
    print("difference from (0.0, 0.0) to ((-1.0, 0.0), (0.0, -1.0)) : (%.2f, %.2f)" % pldiff((0.0, 0.0), (-1.0, 0.0), (0.0, -1.0)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[pldiff Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
