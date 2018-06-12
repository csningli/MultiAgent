
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_obj_basic() :
    '''
    >>> test_obj_basic()
    Initialization.
    Object: <<multiagent.Object name=0>>
    Mass : 0.5
    Radius : 5.0
    Change values of the properties.
    Name : 1
    Mass : 10.0
    Position : (1.0, 0.0)
    Angle : 0.785
    Rotation: (0.707, 0.707)
    Velocity: (1.0, 0.0)
    Angular Velocity: 2.0
    Force: (0.0, 5.0)
    '''
    print("Initialization.")
    obj = Object(name = "0", mass = 0.5, radius = 5.0)
    print("Object: %s" % obj.info())
    print("Mass : %.1f" % obj.mass)
    print("Radius : %.1f" % obj.radius)
    print("Change values of the properties.")
    obj.name = "1"
    print("Name : %s" % obj.name)
    obj.mass = 10.0
    print("Mass : %.1f" % obj.mass)
    obj.pos = (1.0, 0.0)
    print("Position : (%.1f, %.1f)" % (obj.pos[0], obj.pos[1]))
    obj.angle = 0.785
    print("Angle : %.3f" % obj.angle)
    print("Rotation: (%.3f, %.3f)" % (obj.rot[0], obj.rot[1]))
    obj.vel = (1.0, 0.0)
    print("Velocity: (%.1f, %.1f)" % (obj.vel[0], obj.vel[1]))
    obj.avel = 2.0
    print("Angular Velocity: %.1f" % obj.avel)
    obj.force = (0.0, 5.0)
    print("Force: (%.1f, %.1f)" % (obj.force[0], obj.force[1]))

def test_obj_prop() :
    '''
    >>> test_obj_prop()
    Initialization.
    Object: <<multiagent.Object name=0>>
    Mass : 1.0
    Radius : 10.0
    Change properties by directly apply 'obj.prop = prop', where 'prop' is a map storing the new values.
    Mass : 10.0
    Position : (1.0, 0.0)
    Angle : 0.785
    Rotation: (0.707, 0.707)
    Velocity: (1.0, 0.0)
    Angular Velocity: 2.0
    Force: (0.0, 5.0)
    Visible: True
    Pointer Color: (1, 0, 0, 255)
    Fill Color: (0, 1, 0, 255)
    Stroke Color: (0, 0, 1, 255)
    '''
    print("Initialization.")
    obj = Object(name = "0")
    print("Object: %s" % obj.info())
    print("Mass : %.1f" % obj.mass)
    print("Radius : %.1f" % obj.radius)
    print("Change properties by directly apply 'obj.prop = prop', where 'prop' is a map storing the new values.")
    prop = {}
    prop["mass"] = "10.0"
    prop["pos"] = "(1.0, 0.0)"
    prop["angle"] = "0.785"
    prop["vel"] = "(1.0, 0.0)"
    prop["avel"] = "2.0"
    prop["force"] = "(0.0, 5.0)"
    prop["visible"] = "True"
    prop["pcolor"] = "(1, 0, 0, 255)"
    prop["fcolor"] = "(0, 1, 0, 255)"
    prop["scolor"] = "(0, 0, 1, 255)"
    obj.prop = prop
    print("Mass : %.1f" % obj.mass)
    print("Position : (%.1f, %.1f)" % (obj.pos[0], obj.pos[1]))
    print("Angle : %.3f" % obj.angle)
    print("Rotation: (%.3f, %.3f)" % (obj.rot[0], obj.rot[1]))
    print("Velocity: (%.1f, %.1f)" % (obj.vel[0], obj.vel[1]))
    print("Angular Velocity: %.1f" % obj.avel)
    print("Force: (%.1f, %.1f)" % (obj.force[0], obj.force[1]))
    print("Visible: %r" % obj.visible)
    print("Pointer Color: (%d, %d, %d, %d)" % (obj.pointer_color[0], obj.pointer_color[1], obj.pointer_color[2], obj.pointer_color[3]))
    print("Fill Color: (%d, %d, %d, %d)" % (obj.fill_color[0], obj.fill_color[1], obj.fill_color[2], obj.fill_color[3]))
    print("Stroke Color: (%d, %d, %d, %d)" % (obj.stroke_color[0], obj.stroke_color[1], obj.stroke_color[2], obj.stroke_color[3]))


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Object Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
