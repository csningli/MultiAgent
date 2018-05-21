
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *


def test_obj_basic() :
    '''
    >>> test_obj()
    Object: <<multiagent.Object name=test_obj>>
    Mass : 10.0
    Radius : 10.0
    Position : (1.0, 0.0)
    Angle : 1.0
    Rotation: (0.54, 0.84)
    Velocity: (1.0, 0.0)
    Angular Velocity: 2.0
    Force: (0.0, 5.0)
    '''
    obj = Object(name = "0", mass = 0.5, radius = 5.0)
    print("Object: %s" % obj.info())
    print("Mass : %.1f" % obj.mass)
    print("Radius : %.1f" % obj.radius)
    obj.mass = 10.0
    print("New Mass : %.1f" % obj.mass)
    obj.pos = (1.0, 0.0)
    obj.angle = 1.0
    obj.vel = (1.0, 0.0)
    obj.avel = 2.0
    obj.force = (0.0, 5.0)
    print("Position : (%.1f, %.1f)" % (obj.pos[0], obj.pos[1]))
    print("Angle : %.1f" % obj.angle)
    print("Rotation: (%.2f, %.2f)" % (obj.rot[0], obj.rot[1]))
    print("Velocity: (%.1f, %.1f)" % (obj.vel[0], obj.vel[1]))
    print("Angular Velocity: %.1f" % obj.avel)
    print("Force: (%.1f, %.1f)" % (obj.force[0], obj.force[1]))


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Object Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
