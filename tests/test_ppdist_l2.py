
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import ppdist_l2

def test_ppdist_l2() :
    '''
    >>> test_ppdist_l2()
    l2 distance from (0.0, 0.0) to (1.0, 1.0) : 1.41
    l2 distance from (0.0, 0.0) to (-1.0, -1.0) : 1.41
    '''
    print("l2 distance from (0.0, 0.0) to (1.0, 1.0) : %.2f" % ppdist_l2((0.0, 0.0), (1.0, 1.0)))
    print("l2 distance from (0.0, 0.0) to (-1.0, -1.0) : %.2f" % ppdist_l2((0.0, 0.0), (-1.0, -1.0)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[ppdist_l2 Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
