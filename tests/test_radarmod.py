
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *


def test_radarmod_basic() :
    '''
    >>> test_radarmod_basic()
    Initialization.
    RadarModule: <<multiagent.RadarModule memory_size=0>>
    '''
    print("Initialization.")
    mod = RadarModule()
    print("RadarModule: %s" % mod.info())


def test_radarmod_sense() :
    '''
    >>> test_radarmod_sense()
    Initialization.
    RadarModule: <<multiagent.RadarModule memory_size=1>>
    Prepare the request.
    Request: <<multiagent.Request content_len=1>>
    Message to '0': <<multiagent.Message src= dest=0 key=radar value=[(0, 0), (1, 1)]>>
    Memory after sense.
    Radio in message in memory: [(0, 0), (1, 1)]
    '''
    print("Initialization.")
    mod = RadarModule()
    mod.mem.reg(key = "name", value = "0")
    print("RadarModule: %s" % mod.info())
    print("Prepare the request.")
    reqt = Request()
    reqt.add_msg(Message(src = "", dest = "0", key = "radar", value = [(0, 0), (1, 1)]))
    print("Request: %s" % reqt.info())
    for msg in reqt.get_msgs(dest = "0") :
        print("Message to '0': %s" % msg.info())
    mod.sense(reqt)
    print("Memory after sense.")
    print("Radio in message in memory: %s" % mod.get_radar_detect())


def test_radarmod_act() :
    '''
    >>> test_radarmod_act()
    Initialization.
    RadarModule: <<multiagent.RadarModule memory_size=1>>
    Message to '': <<multiagent.Message src= dest= key=radar value=1>>
    '''
    print("Initialization.")
    mod = RadarModule()
    mod.mem.reg(key = "name", value = "0")
    print("RadarModule: %s" % mod.info())
    mod.set_radar_dist(dist = 1)
    resp = Response()
    mod.act(resp)
    for msg in resp.get_msgs(dest = "") :
        print("Message to '': %s" % msg.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[RadarModule Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
