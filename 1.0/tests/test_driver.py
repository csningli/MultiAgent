#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 
from pymunk import Vec2d

def test_aggregator() :
    '''
    >>> test_aggregator()
    Object's status: {'pre': {}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'set_avel': 10.0, 'time': '', 'transmit': 'msg', 'force': (1.0, 1.0)}, 'local': {}}
    Intention: {'0': {'angle': '', 'set_avel': 10.0, 'pos': '', 'time': '', 'transmit': 'msg', 'force': (1.0, 1.0)}}
    Object's status: {'pre': {'force': (1.0, 1.0), 'set_avel': 10.0, 'pos': '', 'time': '', 'transmit': 'msg', 'angle': ''}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'set_avel': 10.0, 'time': '', 'transmit': 'msg', 'force': (1.0, 1.0)}, 'local': {}}
    '''
    obj = Object(name = "0", mods = [])
    obj.status["post"] = {"force" : (1.0, 1.0), "set_avel" : 10.0, "time" : "", "pos" : "", "angle" : "", "transmit" : "msg"}
    print("Object's status: %s" % obj.status)
    aggr = Aggregator()
    intention = aggr.post(objects = [obj])
    print("Intention: %s" % intention)
    aggr.pre(objects = [obj], confirm = intention)
    print("Object's status: %s" % obj.status)


def test_driver() :
    '''
    >>> test_driver()
    Object's status: {'pre': {}, 'mem': {}, 'post': {}, 'local': {'force_buff': [(100.0, 100.0)], 'set_avel_buff': [100.0], 'pos_buff': [''], 'vel_buff': [''], 'avel': [''], 'time_buff': [''], 'angle_buff': ['']}}
    intention: {'0': {'angle': '', 'pos': '', 'set_avel': 100.0, 'time': '', 'force': (100.0, 100.0), 'vel': ''}}
    confirm: {'0': {'pos_result': (0.0, 0.0), 'time_result': 0.02, 'angle_result': 2.0, 'vel_result': (2.0, 2.0)}}
    Object's status: {'pre': {}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'set_avel': 100.0, 'time': '', 'force': (100.0, 100.0), 'vel': ''}, 'local': {'force_buff': [(100.0, 100.0)], 'set_avel_buff': [100.0], 'pos_buff': [''], 'vel_buff': [''], 'avel': [''], 'time_buff': [''], 'angle_buff': ['']}}
    intention: {'0': {'angle': '', 'pos': '', 'set_avel': 100.0, 'time': '', 'force': (100.0, 100.0), 'vel': ''}}
    confirm: {'0': {'pos_result': (0.04, 0.04), 'time_result': 0.04, 'angle_result': 4.0, 'vel_result': (4.0, 4.0)}}
    Object's status: {'pre': {}, 'mem': {}, 'post': {'angle': '', 'pos': '', 'set_avel': 100.0, 'time': '', 'force': (100.0, 100.0), 'vel': ''}, 'local': {'force_buff': [(100.0, 100.0)], 'set_avel_buff': [100.0], 'pos_buff': [''], 'vel_buff': [''], 'avel': [''], 'time_buff': [''], 'angle_buff': ['']}}
    intention: {'0': {'angle': '', 'pos': '', 'set_avel': 100.0, 'time': '', 'force': (100.0, 100.0), 'vel': ''}}
    confirm: {'0': {'pos_result': (0.12, 0.12), 'time_result': 0.06, 'angle_result': 6.0, 'vel_result': (6.0, 6.0)}}
    '''
    obj = Object(name = "0", mods = [ForceModule(), SetAVelModule(), TimeSensorModule(), PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(), AngularVelSensorModule()])
    unit = Unit(name = "0")
    context = Context(delta = 1.0 / 50.0, units = [unit])
    driver = Driver(context = context, objects = [obj])
    for i in range(3) :
        obj.status["local"] = {"force_buff" : [(100.0, 100.0)], "set_avel_buff" : [100.0], "time_buff" : [""], "pos_buff" : [""], "angle_buff" : [""], "vel_buff" : [""], "avel" : [""]}
        print("Object's status: %s" % obj.status) 
        driver.step()
        print("intention: %s" % context.intention)
        print("confirm: %s" % context.confirm)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Driver Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 


