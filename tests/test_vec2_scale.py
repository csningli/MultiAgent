
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import vec2_scale

def test_vec2_scale() :
    '''
    >>> test_vec2_scale()
    2.0 * (1.0, 1.0) = (2.0, 2.0)
    -2.0 * (1.5, 1.5) = (-3.0, -3.0)
    '''
    print("2.0 * (1.0, 1.0) = (%.1f, %.1f)" % vec2_scale((1.0, 1.0), 2.0))
    print("-2.0 * (1.5, 1.5) = (%.1f, %.1f)" % vec2_scale((1.5, 1.5), -2.0))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_scale Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
