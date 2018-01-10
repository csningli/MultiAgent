#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 


def test_obj() :
    '''
    >>> test_obj()
    Object: <multiagent.Object name=test_obj>
    Mass : 10.0
    Radius : 10.0
    Position : (1.0, 0.0)
    Angle : 1.0
    Rotation: (0.54, 0.84)
    Velocity: (1.0, 0.0)
    Angular Velocity: 2.0
    Force: (0.0, 5.0)
    '''
    obj = Object(name = "test_obj")
    obj.mass = 10.0
    obj.pos = (1.0, 0.0)
    obj.angle = 1.0
    obj.vel = (1.0, 0.0)
    obj.avel = 2.0
    obj.force = (0.0, 5.0)
    print("Object: %s" % obj)
    print("Mass : %.1f" % obj.mass)
    print("Radius : %.1f" % obj.radius)
    print("Position : (%.1f, %.1f)" % (obj.pos[0], obj.pos[1]))
    print("Angle : %.1f" % obj.angle)
    print("Rotation: (%.2f, %.2f)" % (obj.rot[0], obj.rot[1]))
    print("Velocity: (%.1f, %.1f)" % (obj.vel[0], obj.vel[1]))
    print("Angular Velocity: %.1f" % obj.avel)
    print("Force: (%.1f, %.1f)" % (obj.force[0], obj.force[1]))


def test_obt() :
    '''
    >>> test_obt()
    Obstacle: <multiagent.Obstacle name=test_obt>
    A: (0.0, 1.0)
    B: (1.0, 0.0)
    Radius: 2.0
    Ends: (0.0, 1.0), (1.0, 0.0)
    '''
    obs = Obstacle(name ="test_obt", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0)
    print("Obstacle: %s" % obs)
    print("A: (%.1f, %.1f)" % (obs.a[0], obs.a[1]))
    print("B: (%.1f, %.1f)" % (obs.b[0], obs.b[1]))
    print("Radius: %.1f" % obs.radius)
    print("Ends: (%.1f, %.1f), (%.1f, %.1f)" % (obs.ends[0][0], obs.ends[0][1], obs.ends[1][0], obs.ends[1][1]))


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Object Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



