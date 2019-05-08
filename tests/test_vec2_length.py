
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.geometry import vec2_length

def test_vec2_length() :
    '''
    >>> test_vec2_length()
    length of (1.0, 1.0): 1.41
    length of (-1.0, 1.0): 1.41
    length of (-3.0, -4.0): 5.00
    '''
    print("length of (1.0, 1.0): %.2f" % vec2_length((1.0, 1.0)))
    print("length of (-1.0, 1.0): %.2f" % vec2_length((-1.0, 1.0)))
    print("length of (-3.0, -4.0): %.2f" % vec2_length((-3.0, -4.0)))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[vec2_length Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
