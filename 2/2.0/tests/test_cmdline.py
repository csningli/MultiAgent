
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_cmdline_basic() :
    '''
    >>> test_cmdline_basic()
    Initialization.
    CommandLine: <<multiagent.instance database= has_connect=0>>
    '''
    print("Initialization.")
    cmdline = CommandLine(database = "")
    print("CommandLine: %s" % cmdline.info())

def test_cmdline_request() :
    '''
    >>> test_cmdline_request()
    Initialization.
    CommandLine: <<multiagent.instance database=./multiagent_commands.db has_connect=1>>
    Request msg: msg_key msg_value msg_more
    Added successfully.
    '''
    print("Initialization.")
    cmdline = CommandLine()
    print("CommandLine: %s" % cmdline.info())
    msg = "msg_key msg_value msg_more"
    print("Request msg: %s" % msg)
    cmdline.request(msg)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[CommandLine Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
