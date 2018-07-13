
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_cmd_basic() :
    '''
    >>> test_cmd_basic()
    Initialization.
    Commander: <<multiagent.Commander database=./multiagent_commands.db has_connect=True>>
    '''
    print("Initialization.")
    cmd = Commander()
    print("Commander: %s" % cmd.info())

def test_cmd_check() :
    '''
    >>> test_cmd_check()
    Initialization.
    Commander: <<multiagent.Commander database=./multiagent_commands.db has_connect=True>>
    Messages:
    '''
    print("Initialization.")
    cmd = Commander()
    print("Commander: %s" % cmd.info())
    msgs = cmd.check()
    print("Messages:")
    for msg in msgs :
        print("Message src=%s, dest=%s, key=%s, value=%s" % (msg.src, msg.dest, msg.key, msg.value))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Commander Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
