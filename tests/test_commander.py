
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_cmd_basic() :
    '''
    >>> test_cmd_basic()
    Initialization.
    Commander: <<multiagent.Commander database=./multiagent_commands.db has_connect=1>>
    '''
    print("Initialization.")
    cmd = Commander()
    print("Commander: %s" % cmd.info())

def test_cmd_check() :
    '''
    >>> test_cmd_check()
    Initialization.
    Commander: <<multiagent.Commander database=./multiagent_commands.db has_connect=1>>
    Add msg to db: msg_key msg_value msg_more
    Added successfully.
    Messages:
    Message: msg_key msg_value msg_more
    '''
    print("Initialization.")
    cmd = Commander()
    print("Commander: %s" % cmd.info())
    cmdline = CommandLine()
    msg = "msg_key msg_value msg_more"
    print("Add msg to db: %s" % msg)
    cmdline.request(msg)
    msgs = cmd.check()
    print("Messages:")
    for msg in msgs :
        print("Message: %s" % msg)

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Commander Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
