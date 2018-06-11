
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_reqt_basic() :
    '''
    >>> test_reqt_basic()
    Initialization.
    Request: <<multiagent.Request content_len=0>>
    Destinations: []
    Content:
    '''
    print("Initialization.")
    reqt = Request()
    print("Request: %s" % reqt.info())
    print("Destinations: %s" % reqt.dests)
    print("Content:")
    for dest, msgs in reqt.content.items() :
        print("\tDestination: %s " % dest)
        for msg in msgs :
            print("\t\tMessage: %s" % msg.info())

def test_reqt_add_get() :
    '''
    >>> test_reqt_add_get()
    Initialization.
    Request: <<multiagent.Request content_len=0>>
    Destinations: ['1']
    Content:
    --Destination: 1
    ----Message: <<multiagent.Message src=0 dest=1 key=key1 value=value1>>
    ----Message: <<multiagent.Message src=2 dest=1 key=key2 value=value2>>
    Get Messages to Destinations: 1
    Message: <<multiagent.Message src=0 dest=1 key=key1 value=value1>>
    Message: <<multiagent.Message src=2 dest=1 key=key2 value=value2>>
    '''
    print("Initialization.")
    reqt = Request()
    print("Request: %s" % reqt.info())
    reqt.add_msg(Message(src = "0", dest = "1", key = "key1", value = "value1"))
    reqt.add_msg(Message(src = "2", dest = "1", key = "key2", value = "value2"))
    print("Destinations: %s" % reqt.dests)
    print("Content:")
    for dest, msgs in reqt.content.items() :
        print("--Destination: %s" % dest)
        for msg in msgs :
            print("----Message: %s" % msg.info())
    print("Get Messages to Destinations: 1")
    msgs = reqt.get_msgs(dest = "1")
    for msg in msgs :
        print("Message: %s" % msg.info())

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Request Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
