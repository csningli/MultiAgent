
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *


def test_radiomod_basic() :
    '''
    >>> test_radiomod_basic()
    Initialization.
    RadioModule: <<multiagent.RadioModule memory_size=0>>
    '''
    print("Initialization.")
    mod = RadioModule()
    print("RadioModule: %s" % mod.info())


def test_radiomod_sense() :
    '''
    >>> test_radiomod_sense()
    Initialization.
    RadioModule: <<multiagent.RadioModule memory_size=1>>
    Prepare the request.
    Request: <<multiagent.Request content_len=1>>
    Message to '0': <<multiagent.Message src= dest=0 key=radio value=income message.>>
    Memory after sense.
    Radio in message in memory: income message.
    '''
    print("Initialization.")
    mod = RadioModule()
    mod.mem.reg(key = "name", value = "0")
    print("RadioModule: %s" % mod.info())
    print("Prepare the request.")
    reqt = Request()
    reqt.add_msg(Message(src = "", dest = "0", key = "radio", value = "income message."))
    print("Request: %s" % reqt.info())
    for msg in reqt.get_msgs(dest = "0") :
        print("Message to '0': %s" % msg.info())
    mod.sense(reqt)
    print("Memory after sense.")
    print("Radio in message in memory: %s" % mod.mem.read(key = "radio_in"))


def test_radiomod_act() :
    '''
    >>> test_radiomod_act()
    Initialization.
    RadioModule: <<multiagent.RadioModule memory_size=1>>
    Message to '': <<multiagent.Message src= dest= key=radio value=outgo message.>>
    '''
    print("Initialization.")
    mod = RadioModule()
    mod.mem.reg(key = "name", value = "0")
    print("RadioModule: %s" % mod.info())
    mod.mem.reg(key = "radio_out", value = "outgo message.")
    resp = Response()
    mod.act(resp)
    for msg in resp.get_msgs(dest = "") :
        print("Message to '': %s" % msg.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Request Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
