
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import vec2_dot

def test_vec2_dot() :
    '''
    >>> test_vec2_dot()
    (2.0, 1.0) * (1.0, 0.0) = 2.00
    (-1.0, 1.0) * (1.0, -1.0) = -2.00
    (-1.0, 2.0) * (-1.5, 2.5) = 6.50
    '''
    print("(2.0, 1.0) * (1.0, 0.0) = %.2f" % vec2_dot((2.0, 1.0), (1.0, 0.0)))
    print("(-1.0, 1.0) * (1.0, -1.0) = %.2f" % vec2_dot((-1.0, 1.0), (1.0, -1.0)))
    print("(-1.0, 2.0) * (-1.5, 2.5) = %.2f" % vec2_dot((-1.0, 2.0), (-1.5, 2.5)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_dot Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
