
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time, math
import doctest

sys.path.append("..")
from mas.geometry import vec2_rotate

def test_vec2_rotate() :
    '''
    >>> test_vec2_rotate()
    rotate (1.0, 1.0) by pi / 4 : (0.00, 1.41)
    rotate (1.0, 1.0) by - pi / 4 : (1.41, 0.00)
    rotate (1.0, 1.0) by pi / 2 : (-1.00, 1.00)
    rotate (1.0, 1.0) by - pi / 2 : (1.00, -1.00)
    rotate (1.0, 1.0) by pi : (-1.00, -1.00)
    rotate (1.0, 1.0) by - pi : (-1.00, -1.00)
    '''
    print("rotate (1.0, 1.0) by pi / 4 : (%.2f, %.2f)" % vec2_rotate((1.0, 1.0), math.pi / 4.0))
    print("rotate (1.0, 1.0) by - pi / 4 : (%.2f, %.2f)" % vec2_rotate((1.0, 1.0), - math.pi / 4.0))
    print("rotate (1.0, 1.0) by pi / 2 : (%.2f, %.2f)" % vec2_rotate((1.0, 1.0), math.pi / 2.0))
    print("rotate (1.0, 1.0) by - pi / 2 : (%.2f, %.2f)" % vec2_rotate((1.0, 1.0), - math.pi / 2.0))
    print("rotate (1.0, 1.0) by pi : (%.2f, %.2f)" % vec2_rotate((1.0, 1.0), math.pi))
    print("rotate (1.0, 1.0) by - pi : (%.2f, %.2f)" % vec2_rotate((1.0, 1.0), - math.pi))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_rotate Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
