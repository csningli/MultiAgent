#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_schedule_init() :
    '''
    >>> test_schedule_init()
    Schedule: <<multiagent.Schedule queue_len=0>>
    '''
    schedule = Schedule()
    print("Schedule: %s" % schedule.info())

def test_schedule_add_pop() :
    '''
    >>> test_schedule_add_pop()
    Schedule: <<multiagent.Schedule queue_len=0>>
    Add Agent: <<multiagent.Agent name=agent1 mods_num=0>>
    Schedule: <<multiagent.Schedule queue_len=1>>
    Add Agent: <<multiagent.Agent name=agent2 mods_num=0>>
    Schedule: <<multiagent.Schedule queue_len=2>>
    Pop Agent: ['<<multiagent.Agent name=agent1 mods_num=0>>']
    Pop Agent: []
    Pop Agent: ['<<multiagent.Agent name=agent2 mods_num=0>>']
    '''
    schedule = Schedule()
    print("Schedule: %s" % schedule.info())
    agent = Agent(name = "agent1")
    print("Add Agent: %s" % agent.info())
    schedule.add_agent(agent)
    print("Schedule: %s" % schedule.info())
    agent = Agent(name = "agent2")
    print("Add Agent: %s" % agent.info())
    schedule.add_agent(agent, delay = 2)
    print("Schedule: %s" % schedule.info())
    agents = schedule.queue_pop()["agents"]
    print("Pop Agent: %s" % [agent.info() for agent in agents])
    agents = schedule.queue_pop()["agents"]
    print("Pop Agent: %s" % [agent.info() for agent in agents])
    agents = schedule.queue_pop()["agents"]
    print("Pop Agent: %s" % [agent.info() for agent in agents])


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Schedule Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



