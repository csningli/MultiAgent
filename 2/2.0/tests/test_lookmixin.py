
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_lookmixin() :
    '''
    >>> test_lookmixin()
    Stroke Color : (0, 0, 0)
    Pointer Color : (0, 1, 0)
    Fill Color : (1, 1, 1)
    Pointer Color : False
    '''
    look = LookMixin()
    look.stroke_color = (0, 0, 0)
    print("Stroke Color : (%d, %d, %d)" % look.stroke_color)
    look.pointer_color = (0, 1, 0)
    print("Pointer Color : (%d, %d, %d)" % look.pointer_color)
    look.fill_color = (1, 1, 1)
    print("Fill Color : (%d, %d, %d)" % look.fill_color)
    look.visible = False
    print("Pointer Color : %r" % look.visible)

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[LookMixin Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
