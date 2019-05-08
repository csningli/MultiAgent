
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import vec2_add

def test_vec2_add() :
    '''
    >>> test_vec2_add()
    (2.0, 1.0) + (1.0, 0.0) = (3.0, 1.0)
    (-1.0, 1.0) + (1.0, -1.0) = (0.0, 0.0)
    '''
    print("(2.0, 1.0) + (1.0, 0.0) = (%.1f, %.1f)" % vec2_add((2.0, 1.0), (1.0, 0.0)))
    print("(-1.0, 1.0) + (1.0, -1.0) = (%.1f, %.1f)" % vec2_add((-1.0, 1.0), (1.0, -1.0)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_add Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
