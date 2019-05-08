
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import vec2_norm

def test_vec2_norm() :
    '''
    >>> test_vec2_norm()
    normalize (1.0, 1.0): (0.71, 0.71)
    normalize (3.0, 4.0): (0.60, 0.80)
    normalize (-1.0, 1.0): (-0.71, 0.71)
    normalize (-3.0, -4.0): (-0.60, -0.80)
    '''
    print("normalize (1.0, 1.0): (%.2f, %.2f)" % vec2_norm((1.0, 1.0)))
    print("normalize (3.0, 4.0): (%.2f, %.2f)" % vec2_norm((3.0, 4.0)))
    print("normalize (-1.0, 1.0): (%.2f, %.2f)" % vec2_norm((-1.0, 1.0)))
    print("normalize (-3.0, -4.0): (%.2f, %.2f)" % vec2_norm((-3.0, -4.0)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_norm Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
