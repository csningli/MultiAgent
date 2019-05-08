
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import vec2_angle

def test_vec2_angle_positive_true() :
    '''
    >>> test_vec2_angle_positive_true()
    angle of (1.0, 0.0): 0.00
    angle of (0.0, 1.0): 1.57
    angle of (1.0, 1.0): 0.79
    angle of (-1.0, 0.0): 3.14
    angle of (0.0, -1.0): 4.71
    angle of (-1.0, -1.0): 3.93
    '''
    print("angle of (1.0, 0.0): %.2f" % vec2_angle((1.0, 0.0)))
    print("angle of (0.0, 1.0): %.2f" % vec2_angle((0.0, 1.0)))
    print("angle of (1.0, 1.0): %.2f" % vec2_angle((1.0, 1.0)))
    print("angle of (-1.0, 0.0): %.2f" % vec2_angle((-1.0, 0.0)))
    print("angle of (0.0, -1.0): %.2f" % vec2_angle((0.0, -1.0), positive = True))
    print("angle of (-1.0, -1.0): %.2f" % vec2_angle((-1.0, -1.0), positive = True))

def test_vec2_angle_positive_false() :
    '''
    >>> test_vec2_angle_positive_false()
    angle of (1.0, 0.0): 0.00
    angle of (0.0, 1.0): 1.57
    angle of (1.0, 1.0): 0.79
    angle of (-1.0, 0.0): 3.14
    angle of (0.0, -1.0): -1.57
    angle of (-1.0, -1.0): -2.36
    '''
    print("angle of (1.0, 0.0): %.2f" % vec2_angle((1.0, 0.0), positive = False))
    print("angle of (0.0, 1.0): %.2f" % vec2_angle((0.0, 1.0), positive = False))
    print("angle of (1.0, 1.0): %.2f" % vec2_angle((1.0, 1.0), positive = False))
    print("angle of (-1.0, 0.0): %.2f" % vec2_angle((-1.0, 0.0), positive = False))
    print("angle of (0.0, -1.0): %.2f" % vec2_angle((0.0, -1.0), positive = False))
    print("angle of (-1.0, -1.0): %.2f" % vec2_angle((-1.0, -1.0), positive = False))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_angle Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
