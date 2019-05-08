
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import pldist_l2

def test_pldist_l2() :
    '''
    >>> test_pldist_l2()
    l2 distance from (0.0, 0.0) to ((1.0, 0.0), (0.0, 1.0)) : 0.71
    l2 distance from (0.0, 0.0) to ((-1.0, 0.0), (0.0, -1.0)) : 0.71
    '''
    print("l2 distance from (0.0, 0.0) to ((1.0, 0.0), (0.0, 1.0)) : %.2f" % pldist_l2((0.0, 0.0), (1.0, 0.0), (0.0, 1.0)))
    print("l2 distance from (0.0, 0.0) to ((-1.0, 0.0), (0.0, -1.0)) : %.2f" % pldist_l2((0.0, 0.0), (-1.0, 0.0), (0.0, -1.0)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[pldist_l2 Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
