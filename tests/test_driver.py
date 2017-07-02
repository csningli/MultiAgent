#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 
from pymunk import Vec2d

def test_aggregator() :
    '''
    >>> test_aggregator()
    Object's status: {'pre': {}, 'mem': {}, 'post': {'force': (1.0, 1.0), 'time': '', 'transmit': 'msg', 'position': '', 'angle': '', 'spin': 10.0}, 'local': {}}
    Intention: {'0': {'force': (1.0, 1.0), 'time': '', 'transmit': 'msg', 'position': '', 'angle': '', 'spin': 10.0}}
    Object's status: {'pre': {'force': (1.0, 1.0), 'angle': '', 'time': '', 'transmit': 'msg', 'position': '', 'spin': 10.0}, 'mem': {}, 'post': {'force': (1.0, 1.0), 'time': '', 'transmit': 'msg', 'position': '', 'angle': '', 'spin': 10.0}, 'local': {}}
    '''
    obj = Object(name = "0", mods = [])
    obj.status["post"] = {"force" : (1.0, 1.0), "spin" : 10.0, "time" : "", "position" : "", "angle" : "", "transmit" : "msg"}
    print("Object's status: %s" % obj.status)
    aggr = Aggregator()
    intention = aggr.post(objects = [obj])
    print("Intention: %s" % intention)
    aggr.pre(objects = [obj], confirm = intention)
    print("Object's status: %s" % obj.status)


def test_driver() :
    '''
    >>> test_driver()
    Object's status: {'pre': {}, 'mem': {}, 'post': {}, 'local': {'spins': [100.0], 'forces': [(100.0, 100.0)]}}
    intention: {'0': {'force': (100.0, 100.0), 'angular_velocity': '', 'time': '', 'velocity': '', 'position': '', 'angle': '', 'spin': 100.0}}
    confirm: {'0': {'pos_x': 0.0, 'pos_y': 0.0, 'angle': 2.0, 'receive': {}, 'timer': {'value': 0.02}, 'velocity': (2.0, 2.0), 'angular_velocity': 100.0}}
    Object's status: {'pre': {}, 'mem': {}, 'post': {'force': (100.0, 100.0), 'angular_velocity': '', 'time': '', 'velocity': '', 'position': '', 'angle': '', 'spin': 100.0}, 'local': {'spins': [100.0], 'forces': [(100.0, 100.0)]}}
    intention: {'0': {'force': (100.0, 100.0), 'angular_velocity': '', 'time': '', 'velocity': '', 'position': '', 'angle': '', 'spin': 100.0}}
    confirm: {'0': {'pos_x': 0.04, 'pos_y': 0.04, 'angle': 4.0, 'receive': {}, 'timer': {'value': 0.04}, 'velocity': (4.0, 4.0), 'angular_velocity': 100.0}}
    Object's status: {'pre': {}, 'mem': {}, 'post': {'force': (100.0, 100.0), 'angular_velocity': '', 'time': '', 'velocity': '', 'position': '', 'angle': '', 'spin': 100.0}, 'local': {'spins': [100.0], 'forces': [(100.0, 100.0)]}}
    intention: {'0': {'force': (100.0, 100.0), 'angular_velocity': '', 'time': '', 'velocity': '', 'position': '', 'angle': '', 'spin': 100.0}}
    confirm: {'0': {'pos_x': 0.12, 'pos_y': 0.12, 'angle': 6.0, 'receive': {}, 'timer': {'value': 0.06}, 'velocity': (6.0, 6.0), 'angular_velocity': 100.0}}
    '''
    obj = Object(name = "0", mods = [MotionModule(), TimeSensorModule(), PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(), AngularVelSensorModule()])
    unit = Unit(name = "0")
    context = Context(delta = 1.0 / 50.0, units = [unit])
    driver = Driver(context = context, objects = [obj])
    for i in range(3) :
        obj.status["local"] = {"forces" : [(100.0, 100.0)], "spins" : [100.0]}
        print("Object's status: %s" % obj.status) 
        driver.step()
        print("intention: %s" % context.intention)
        print("confirm: %s" % context.confirm)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Driver Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 


