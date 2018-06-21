
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *


def test_agent_basic() :
    '''
    >>> test_agent_basic()
    Initialization.
    Agent: <<multiagent.Agent name=0 mods_num=1>>
    Memory: <<multiagent.Memory content_size=1>>
    Memory Content:
    Key: name - Value: 0
    Module: <<multiagent.ObjectModule memory_size=1>>
    Change values of the properties.
    Active: False
    '''
    print("Initialization.")
    agent = Agent(name = "0")
    print("Agent: %s" % agent.info())
    print("Memory: %s" % agent.mem.info())
    print("Memory Content:")
    for key, value in agent.mem.content.items() :
        print("Key: %s - Value: %s" % (key, value))
    for mod in agent.mods :
        print("Module: %s" % mod.info())
    print("Change values of the properties.")
    agent.active = False
    print("Active: %r" % agent.active)

def test_agent_memo() :
    '''
    >>> test_agent_memo()
    Initialization.
    Agent: <<multiagent.Agent name=0 mods_num=1>>
    Active: True
    Memory Content:
    Key: name - Value: 0
    Change properties by directly apply 'agent.memo = memo', where 'memo' is a map storing the new values.
    Active: False
    Memory Content:
    Key: name - Value: 0
    Key: key - Value: True
    '''
    print("Initialization.")
    agent = Agent(name = "0")
    print("Agent: %s" % agent.info())
    print("Active: %r" % agent.active)
    print("Memory Content:")
    for key, value in agent.mem.content.items() :
        print("Key: %s - Value: %s" % (key, value))
    print("Change properties by directly apply 'agent.memo = memo', where 'memo' is a map storing the new values.")
    memo = {
        "active" : False,
        "__mem" : {
            "name" : "0",
            "key" : True,
        }
    }
    agent.memo = memo
    print("Active: %r" % agent.active)
    print("Memory Content:")
    for key, value in agent.mem.content.items() :
        print("Key: %s - Value: %s" % (key, value))


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Agent Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
