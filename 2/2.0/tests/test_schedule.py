
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_schedule_basic() :
    '''
    >>> test_schedule_basic()
    Initialization.
    Schedule: <<multiagent.Schedule queue_len=1 last=-1>>
    '''
    print("Initialization.")
    schedule = Schedule()
    print("Schedule: %s" % schedule.info())

def test_schedule_add_pop() :
    '''
    >>> test_schedule_add_pop()
    Initialization.
    Schedule: <<multiagent.Schedule queue_len=1 last=-1>>
    Add Agent: <<multiagent.Agent name=0 mods_num=1>>
    Schedule: <<multiagent.Schedule queue_len=2 last=0>>
    Add Agent: <<multiagent.Agent name=1 mods_num=1>>
    Schedule: <<multiagent.Schedule queue_len=3 last=2>>
    Pop Agent: ['<<multiagent.Agent name=0 mods_num=1>>']
    Pop Agent: []
    Pop Agent: ['<<multiagent.Agent name=1 mods_num=1>>']
    Add Object: <<multiagent.Object name=0>>
    Schedule: <<multiagent.Schedule queue_len=4 last=0>>
    Add Object: <<multiagent.Object name=1>>
    Schedule: <<multiagent.Schedule queue_len=4 last=2>>
    Pop Object: ['<<multiagent.Object name=0>>']
    Pop Object: []
    Pop Object: ['<<multiagent.Object name=1>>']
    '''
    print("Initialization.")
    schedule = Schedule()
    print("Schedule: %s" % schedule.info())
    agent = Agent(name = "0")
    print("Add Agent: %s" % agent.info())
    schedule.add_agent(agent)
    print("Schedule: %s" % schedule.info())
    agent = Agent(name = "1")
    print("Add Agent: %s" % agent.info())
    schedule.add_agent(agent, delay = 2)
    print("Schedule: %s" % schedule.info())
    agents = schedule.queue_pop()["agent"]
    print("Pop Agent: %s" % [agent.info() for agent in agents])
    agents = schedule.queue_pop()["agent"]
    print("Pop Agent: %s" % [agent.info() for agent in agents])
    agents = schedule.queue_pop()["agent"]
    print("Pop Agent: %s" % [agent.info() for agent in agents])
    obj = Object(name = "0")
    print("Add Object: %s" % obj.info())
    schedule.add_obj(obj)
    print("Schedule: %s" % schedule.info())
    obj = Object(name = "1")
    print("Add Object: %s" % obj.info())
    schedule.add_obj(obj, delay = 2)
    print("Schedule: %s" % schedule.info())
    objs = schedule.queue_pop()["obj"]
    print("Pop Object: %s" % [obj.info() for obj in objs])
    objs = schedule.queue_pop()["obj"]
    print("Pop Object: %s" % [obj.info() for obj in objs])
    objs = schedule.queue_pop()["obj"]
    print("Pop Object: %s" % [obj.info() for obj in objs])


def test_schedule_get_gen() :
    '''
    >>> test_schedule_get_gen()
    Initialization.
    Schedule: <<multiagent.Schedule queue_len=1 last=-1>>
    Add Agent: <<multiagent.Agent name=0 mods_num=1>>
    Add Object: <<multiagent.Object name=0>>
    Schedule: <<multiagent.Schedule queue_len=2 last=0>>
    Agent Generator: <class 'multiagent.Agent'>
    Object Generator: <class 'multiagent.Object'>
    '''
    print("Initialization.")
    schedule = Schedule()
    print("Schedule: %s" % schedule.info())
    agent = Agent(name = "0")
    schedule.add_agent(agent)
    print("Add Agent: %s" % agent.info())
    obj = Object(name = "0")
    print("Add Object: %s" % obj.info())
    schedule.add_obj(obj)
    print("Schedule: %s" % schedule.info())
    print("Agent Generator: %s" % schedule.get_agent_gen(name = "0"))
    print("Object Generator: %s" % schedule.get_obj_gen(name = "0"))



if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Schedule Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
