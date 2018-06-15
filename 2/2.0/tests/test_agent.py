
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *


def test_agent_basic() :
    '''
    >>> test_agent_basic()
    Agent: <<multiagent.Agent name=0 mods_num=1>>
    '''
    print("Initialization.")
    agent = Agent(name = "0")
    print("Agent: %s" % agent.info())

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Agent Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
