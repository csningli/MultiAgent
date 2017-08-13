#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_module() :
    '''
    >>> test_module()
    msg: {'msg_key': 'msg_value'}
    ram: {'ram_key': 'ram_value'}
    perform result: {'post': {}, 'ram': {}, 'local': {}}
    '''
    mod = Module()
    msg = {"msg_key" : "msg_value"}
    ram = {"ram_key" : "ram_value"}
    print("msg: %s" % msg)
    print("ram: %s" % ram)
    result = mod.perform(msg = msg, ram = ram)
    print("perform result: %s" % result) 
    
def test_motion_module() :
    '''
    >>> test_motion_module()
    msg: {'force_buff': [(1.0, 1.0)]}
    ram: {'ram_key': 'ram_value'}
    perform result: {'post': {'force': (1.0, 1.0)}, 'ram': {}, 'local': {}}
    '''
    mod = ForceModule()
    msg = {"force_buff" : [(1.0, 1.0)]}
    ram = {"ram_key" : "ram_value"}
    print("msg: %s" % msg)
    print("ram: %s" % ram)
    result = mod.perform(msg = msg, ram = ram)
    print("perform result: %s" % result) 

def test_transmit_module() :
    '''
    >>> test_transmit_module()
    msg: {'transmit_buff': ['packet0', 'packet1', 'packet2']}
    ram: {'ram_key': 'ram_value'}
    perform result: {'post': {'transmit': 'packet0;packet1;packet2;'}, 'ram': {}, 'local': {}}
    '''
    mod = TransmitModule()
    msg = {"transmit_buff" : ['packet0', 'packet1', 'packet2']}
    ram = {"ram_key" : "ram_value"}
    print("msg: %s" % msg)
    print("ram: %s" % ram)
    result = mod.perform(msg = msg, ram = ram)
    print("perform result: %s" % result) 

def test_timesensor_module() :
    '''
    >>> test_timesensor_module()
    msg: {'time_buff': ['']}
    ram: {'ram_key': 'ram_value'}
    perform result: {'post': {'time': ''}, 'ram': {}, 'local': {}}
    '''
    mod = TimeSensorModule()
    msg = {"time_buff" : [""]}
    ram = {"ram_key" : "ram_value"}
    print("msg: %s" % msg)
    print("ram: %s" % ram)
    result = mod.perform(msg = msg, ram = ram)
    print("perform result: %s" % result) 

def test_positionsensor_module() :
    '''
    >>> test_positionsensor_module()
    msg: {'pos_buff': ['']}
    ram: {'ram_key': 'ram_value'}
    perform result: {'post': {'pos': ''}, 'ram': {}, 'local': {}}
    '''
    mod = PositionSensorModule()
    msg = {"pos_buff" : ['']}
    ram = {"ram_key" : "ram_value"}
    print("msg: %s" % msg)
    print("ram: %s" % ram)
    result = mod.perform(msg = msg, ram = ram)
    print("perform result: %s" % result) 

def test_anglesensor_module() :
    '''
    >>> test_anglesensor_module()
    msg: {'angle_buff': ['']}
    ram: {'ram_key': 'ram_value'}
    perform result: {'post': {'angle': ''}, 'ram': {}, 'local': {}}
    '''
    mod = AngleSensorModule()
    msg = {"angle_buff" : [""]}
    ram = {"ram_key" : "ram_value"}
    print("msg: %s" % msg)
    print("ram: %s" % ram)
    result = mod.perform(msg = msg, ram = ram)
    print("perform result: %s" % result)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Module Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



