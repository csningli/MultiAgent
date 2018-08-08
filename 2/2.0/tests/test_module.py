
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_mod_basic() :
    '''
    >>> test_mod_basic()
    Initialization.
    Module: <<multiagent.Module memory_size=0>>
    '''
    print("Initialization.")
    mod = Module()
    print("Module: %s" % mod.info())

def test_mod_get() :
    '''
    >>> test_mod_get()
    Initialization.
    Module: <<multiagent.Module memory_size=0>>
    Position: None
    Angle: None
    Velocity: None
    Angular Velocity: None
    Force: None
    Color: None
    Radio In Messages: []
    Radio Out Message: None
    Radar Detect: []
    Radar Distance: None
    '''
    print("Initialization.")
    mod = Module()
    print("Module: %s" % mod.info())
    print("Position: %s" % mod.get_pos())
    print("Angle: %s" % mod.get_angle())
    print("Velocity: %s" % mod.get_vel())
    print("Angular Velocity: %s" % mod.get_avel())
    print("Force: %s" % mod.get_force())
    print("Color: %s" % mod.get_color())
    print("Radio In Messages: %s" % mod.get_radio_in_msgs())
    print("Radio Out Message: %s" % mod.get_radio_out_msg())
    print("Radar Detect: %s" % mod.get_radar_detect())
    print("Radar Distance: %s" % mod.get_radar_dist())


def test_mod_apply() :
    '''
    >>> test_mod_apply()
    Initialization.
    Module: <<multiagent.Module memory_size=0>>
    Apply velocity: (10, 10)
    Velocity : (10.0, 10.0)
    Apply angular velocity: 10
    Angular Velocity: 10
    Apply force: (10, 10)
    Force : (10.0, 10.0)
    Apply color: (10, 10)
    Force : (10.0, 10.0)
    Color : (1, 1, 1, 255)
    '''
    print("Initialization.")
    mod = Module()
    print("Module: %s" % mod.info())
    print("Apply velocity: (10, 10)")
    mod.apply_vel(vel = (10, 10))
    print("Velocity : (%.1f, %.1f)" % (mod.get_vel()[0], mod.get_vel()[1]))
    print("Apply angular velocity: 10")
    mod.apply_avel(avel = 10)
    print("Angular Velocity: %s" % mod.get_avel())
    print("Apply force: (10, 10)")
    mod.apply_force(force = (10, 10))
    print("Force : (%.1f, %.1f)" % (mod.get_force()[0], mod.get_force()[1]))
    print("Apply color: (10, 10)")
    mod.apply_force(force = (10, 10))
    print("Force : (%.1f, %.1f)" % (mod.get_force()[0], mod.get_force()[1]))
    mod.apply_color(color = (1, 1, 1, 255))
    print("Color : (%d, %d, %d, %d)" % (mod.get_color()[0], mod.get_color()[1], mod.get_color()[2], mod.get_color()[3]))


def test_mod_set() :
    '''
    >>> test_mod_set()
    Initialization.
    Module: <<multiagent.Module memory_size=0>>
    Set radio out message to <<multiagent.Message src= dest= key= value=>>
    Get radio out message: <<multiagent.Message src= dest= key= value=>>
    Set radar distance to 10
    Get radar distance: 10
    '''
    print("Initialization.")
    mod = Module()
    print("Module: %s" % mod.info())
    msg = Message()
    print("Set radio out message to %s" % msg.info())
    mod.set_radio_out_msg(msg = msg)
    print("Get radio out message: %s" % mod.get_radio_out_msg().info())
    print("Set radar distance to 10")
    mod.set_radar_dist(dist = 10)
    print("Get radar distance: %d" % mod.get_radar_dist())

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Module Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
