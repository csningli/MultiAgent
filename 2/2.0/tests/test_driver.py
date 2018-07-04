
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_driver_basic() :
    '''
    >>> test_driver_basic()
    Initialization.
    Driver: <<multiagent.Driver has_context=1 has_schedule=1>>
    Request: None
    Response: None
    Context: <<multiagent.Context has_oracle=1>>
    Schedule: <<multiagent.Schedule queue_len=1 last=-1>>
    Number of Agents: 0
    Set Steps: 1
    Steps: 1
    Set Filename: multiagent.data
    Filename: multiagent.data
    Data: <<multiagent.Data size=0 filename=multiagent.data>>
    '''
    context = Context()
    schedule = Schedule()
    driver = Driver(context = context, schedule = schedule)
    print("Initialization.")
    print("Driver: %s" % driver.info())
    print("Request: %s" % driver.reqt)
    print("Response: %s" % driver.resp)
    print("Context: %s" % driver.context.info())
    print("Schedule: %s" % driver.schedule.info())
    print("Number of Agents: %d" % len(driver.agents))
    print("Set Steps: 1")
    driver.steps = 1
    print("Steps: %s" % driver.steps)
    print("Set Filename: multiagent.data")
    driver.filename = "multiagent.data"
    print("Filename: %s" % driver.filename)
    print("Data: %s" % driver.data.info())


def test_driver_go_and_back() :
    '''
    >>> test_driver_go_and_back()
    Initialization.
    Driver: <<multiagent.Driver has_context=1 has_schedule=1>>
    Context Parameters in shot at 0.00: {'time': '0.0'}
    Driver go.
    Context Parameters in shot at 0.01: {'time': '0.01'}
    Driver back.
    context_paras: {'time': '0.0'}
    Context Parameters in shot at 0.00: {'time': '0.0'}
    Apply shot at 0.01.
    context_paras: {'time': '0.01'}
    Context Parameters in shot at 0.01: {'time': '0.01'}
    '''
    context = Context()
    schedule = Schedule()
    driver = Driver(context = context, schedule = schedule)
    print("Initialization.")
    print("Driver: %s" % driver.info())
    shot0 = driver.take_shot()
    print("Context Parameters in shot at 0.00: %s" % shot0.context_paras)
    print("Driver go.")
    driver.go()
    shot1 = driver.take_shot()
    print("Context Parameters in shot at 0.01: %s" % shot1.context_paras)
    print("Driver back.")
    driver.back()
    shot0 = driver.take_shot()
    print("Context Parameters in shot at 0.00: %s" % shot0.context_paras)
    print("Apply shot at 0.01.")
    driver.apply_shot(shot1)
    driver.steps = 1
    shot0 = driver.take_shot()
    print("Context Parameters in shot at 0.01: %s" % shot0.context_paras)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Driver Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
