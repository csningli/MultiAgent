#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 
from pymunk import Vec2d

def test_aggregator() :
    '''
    >>> test_aggregator()
    Object's status: {'pre': {}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'time': '', 'transmit': 'msg', 'force': (1.0, 1.0), 'spin': 10.0}, 'local': {}}
    Intention: {'0': {'angle': '', 'pos': '', 'time': '', 'transmit': 'msg', 'force': (1.0, 1.0), 'spin': 10.0}}
    Object's status: {'pre': {'force': (1.0, 1.0), 'pos': '', 'time': '', 'transmit': 'msg', 'angle': '', 'spin': 10.0}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'time': '', 'transmit': 'msg', 'force': (1.0, 1.0), 'spin': 10.0}, 'local': {}}
    '''
    obj = Object(name = "0", mods = [])
    obj.status["post"] = {"force" : (1.0, 1.0), "spin" : 10.0, "time" : "", "pos" : "", "angle" : "", "transmit" : "msg"}
    print("Object's status: %s" % obj.status)
    aggr = Aggregator()
    intention = aggr.post(objects = [obj])
    print("Intention: %s" % intention)
    aggr.pre(objects = [obj], confirm = intention)
    print("Object's status: %s" % obj.status)


def test_driver() :
    '''
    >>> test_driver()
    Object's status: {'pre': {}, 'mem': {}, 'post': {}, 'local': {'angle_buff': [''], 'avel': [''], 'pos_buff': [''], 'vel_buff': [''], 'time_buff': [''], 'spin_buff': [100.0], 'force_buff': [(100.0, 100.0)]}}
    intention: {'0': {'angle': '', 'pos': '', 'time': '', 'force': (100.0, 100.0), 'vel': '', 'spin': 100.0}}
    confirm: {'0': {'pos_result': (0.0, 0.0), 'time_result': 0.02, 'angle_result': 2.0, 'vel_result': (2.0, 2.0)}}
    Object's status: {'pre': {}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'time': '', 'force': (100.0, 100.0), 'vel': '', 'spin': 100.0}, 'local': {'angle_buff': [''], 'avel': [''], 'pos_buff': [''], 'vel_buff': [''], 'time_buff': [''], 'spin_buff': [100.0], 'force_buff': [(100.0, 100.0)]}}
    intention: {'0': {'angle': '', 'pos': '', 'time': '', 'force': (100.0, 100.0), 'vel': '', 'spin': 100.0}}
    confirm: {'0': {'pos_result': (0.04, 0.04), 'time_result': 0.04, 'angle_result': 4.0, 'vel_result': (4.0, 4.0)}}
    Object's status: {'pre': {}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'time': '', 'force': (100.0, 100.0), 'vel': '', 'spin': 100.0}, 'local': {'angle_buff': [''], 'avel': [''], 'pos_buff': [''], 'vel_buff': [''], 'time_buff': [''], 'spin_buff': [100.0], 'force_buff': [(100.0, 100.0)]}}
    intention: {'0': {'angle': '', 'pos': '', 'time': '', 'force': (100.0, 100.0), 'vel': '', 'spin': 100.0}}
    confirm: {'0': {'pos_result': (0.12, 0.12), 'time_result': 0.06, 'angle_result': 6.0, 'vel_result': (6.0, 6.0)}}
    '''
    obj = Object(name = "0", mods = [ForceModule(), SpinModule(), TimeSensorModule(), PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(), AngularVelSensorModule()])
    unit = Unit(name = "0")
    context = Context(delta = 1.0 / 50.0, units = [unit])
    driver = Driver(context = context, objects = [obj])
    for i in range(3) :
        obj.status["local"] = {"force_buff" : [(100.0, 100.0)], "spin_buff" : [100.0], "time_buff" : [""], "pos_buff" : [""], "angle_buff" : [""], "vel_buff" : [""], "avel" : [""]}
        print("Object's status: %s" % obj.status) 
        driver.step()
        print("intention: %s" % context.intention)
        print("confirm: %s" % context.confirm)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Driver Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 


