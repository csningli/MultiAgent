
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


def test_agent_handle() :
    '''
    >>> test_agent_handle()
    Initialization.
    Agent: <<multiagent.Agent name=0 mods_num=1>>
    Prepare the request.
    Request: <<multiagent.Request content_len=1>>
    Message to '0': <<multiagent.Message src= dest=0 key=pos value=(10, 10)>>
    Message to '0': <<multiagent.Message src= dest=0 key=angle value=10>>
    Message to '0': <<multiagent.Message src= dest=0 key=vel value=(1, 1)>>
    Message to '0': <<multiagent.Message src= dest=0 key=avel value=1>>
    Message to '0': <<multiagent.Message src= dest=0 key=force value=(1, 1)>>
    Message to '0': <<multiagent.Message src= dest=0 key=color value=(1, 1, 1, 255)>>
    Memory Content:
    Key: force - Value: (1, 1)
    Key: name - Value: 0
    Key: avel - Value: 1
    Key: color - Value: (1, 1, 1, 255)
    Key: pos - Value: (10, 10)
    Key: angle - Value: 10
    Key: vel - Value: (1, 1)
    '''
    print("Initialization.")
    agent = Agent(name = "0")
    print("Agent: %s" % agent.info())
    print("Prepare the request.")
    reqt = Request()
    reqt.add_msg(Message(src = "", dest = "0", key = "pos", value = (10, 10)))
    reqt.add_msg(Message(src = "", dest = "0", key = "angle", value = 10))
    reqt.add_msg(Message(src = "", dest = "0", key = "vel", value = (1, 1)))
    reqt.add_msg(Message(src = "", dest = "0", key = "avel", value = 1))
    reqt.add_msg(Message(src = "", dest = "0", key = "force", value = (1, 1)))
    reqt.add_msg(Message(src = "", dest = "0", key = "color", value = (1, 1, 1, 255)))
    print("Request: %s" % reqt.info())
    for msg in reqt.get_msgs(dest = "0") :
        print("Message to '0': %s" % msg.info())
    resp = agent.handle_reqt(reqt)
    print("Memory Content:")
    for key, value in agent.mem.content.items() :
        print("Key: %s - Value: %s" % (key, value))


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Agent Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
