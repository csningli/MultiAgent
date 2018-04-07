
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *


def test_agent() :
    '''
    >>> test_agent()
    Agent: <<multiagent.Agent name=test_agent mods_num=0>>
    '''
    agent = Agent(name = "test_agent")
    print("Agent: %s" % agent.info())

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Agent Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
