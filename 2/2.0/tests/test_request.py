#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_request_init() :
    '''
    >>> test_request_init()
    Request: <<multiagent.Request content_len=0>>
    '''
    reqt = Request()
    print("Request: %s" % reqt.info())

def test_request_add() :
    '''
    >>> test_request_add()
    Request: <<multiagent.Request content_len=0>>
    Add Message: <<multiagent.Message src=src dest=dest key=key value=value>>
    Request: <<multiagent.Request content_len=1>>
    Get Messages: ['<<multiagent.Message src=src dest=dest key=key value=value>>']
    '''
    reqt = Request()
    print("Request: %s" % reqt.info())
    msg = Message(src = "src", dest = "dest", key = "key", value = "value")
    print("Add Message: %s" % msg.info())
    reqt.add_msg(msg)
    print("Request: %s" % reqt.info())
    msgs = reqt.get_msgs(dest = "dest")
    print("Get Messages: %s" % [msg.info() for msg in msgs])


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Request Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



