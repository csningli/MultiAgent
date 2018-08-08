
# MultiAgent 2.0
# copyright (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_obt_basic() :
    '''
    >>> test_obt_basic()
    Initialization.
    Obstacle: <<multiagent.Obstacle name=0>>
    A: (1.0, 0.0)
    B: (0.0, 1.0)
    Radius: 2.0
    Change values of the properties.
    Name : 1
    '''
    print("Initialization.")
    obt = Obstacle(name ="0", a = (1.0, 0.0), b = (0.0, 1.0), radius = 2.0)
    print("Obstacle: %s" % obt.info())
    print("A: (%.1f, %.1f)" % (obt.a[0], obt.a[1]))
    print("B: (%.1f, %.1f)" % (obt.b[0], obt.b[1]))
    print("Radius: %.1f" % obt.radius)
    print("Change values of the properties.")
    obt.name = "1"
    print("Name : %s" % obt.name)

def test_obt_prop() :
    '''
    >>> test_obt_prop()
    Initialization.
    Obstacle: <<multiagent.Obstacle name=0>>
    A: (1.0, 0.0)
    B: (0.0, 1.0)
    Radius: 1.0
    Change properties by directly apply 'obt.prop = prop', where 'prop' is a map storing the new values.
    Visible: True
    Pointer Color: (1, 0, 0, 255)
    Fill Color: (0, 1, 0, 255)
    Stroke Color: (0, 0, 1, 255)
    '''
    print("Initialization.")
    obt = Obstacle(name ="0", a = (1.0, 0.0), b = (0.0, 1.0))
    print("Obstacle: %s" % obt.info())
    print("A: (%.1f, %.1f)" % (obt.a[0], obt.a[1]))
    print("B: (%.1f, %.1f)" % (obt.b[0], obt.b[1]))
    print("Radius: %.1f" % obt.radius)
    print("Change properties by directly apply 'obt.prop = prop', where 'prop' is a map storing the new values.")
    prop = {}
    prop["visible"] = "True"
    prop["pcolor"] = "(1, 0, 0, 255)"
    prop["fcolor"] = "(0, 1, 0, 255)"
    prop["scolor"] = "(0, 0, 1, 255)"
    obt.prop = prop
    print("Visible: %r" % obt.visible)
    print("Pointer Color: (%d, %d, %d, %d)" % (obt.pointer_color[0], obt.pointer_color[1], obt.pointer_color[2], obt.pointer_color[3]))
    print("Fill Color: (%d, %d, %d, %d)" % (obt.fill_color[0], obt.fill_color[1], obt.fill_color[2], obt.fill_color[3]))
    print("Stroke Color: (%d, %d, %d, %d)" % (obt.stroke_color[0], obt.stroke_color[1], obt.stroke_color[2], obt.fill_color[3]))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Obstacle Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
