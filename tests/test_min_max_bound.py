
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import min_max_bound

def test_min_max_bound() :
    '''
    >>> test_min_max_bound()
    [0, 1] bound of 0.5: 0.5
    [0, 1] bound of 1.5: 1.0
    [0, 1] bound of -0.5: 0.0
    '''
    print("[0, 1] bound of 0.5: %.1f" % min_max_bound(0.5, 0, 1))
    print("[0, 1] bound of 1.5: %.1f" % min_max_bound(1.5, 0, 1))
    print("[0, 1] bound of -0.5: %.1f" % min_max_bound(-0.5, 0, 1))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[min_max_bound Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
