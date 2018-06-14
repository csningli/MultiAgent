
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *


def test_objmod_basic() :
    '''
    >>> test_objmod_basic()
    Initialization.
    ObjectModule: <<multiagent.ObjectModule memory_size=0>>
    '''
    print("Initialization.")
    mod = ObjectModule()
    print("ObjectModule: %s" % mod.info())


def test_objmod_sense() :
    '''
    >>> test_objmod_sense()
    Initialization.
    ObjectModule: <<multiagent.ObjectModule memory_size=1>>
    Prepare the request.
    Request: <<multiagent.Request content_len=1>>
    Message to '0': <<multiagent.Message src= dest=0 key=pos value=(10, 10)>>
    Message to '0': <<multiagent.Message src= dest=0 key=angle value=10>>
    Message to '0': <<multiagent.Message src= dest=0 key=vel value=(1, 1)>>
    Message to '0': <<multiagent.Message src= dest=0 key=avel value=1>>
    Message to '0': <<multiagent.Message src= dest=0 key=force value=(1, 1)>>
    Message to '0': <<multiagent.Message src= dest=0 key=color value=(1, 1, 1, 255)>>
    Memory after sense.
    Position in memory: (10.0, 10.0)
    Position in buffer: (10.0, 10.0)
    Angle in memory: 10.0
    Angle in buffer: 10.0
    Velocity in memory: (1.0, 1.0)
    Velocity in buffer: (1.0, 1.0)
    Angular velocity in memory: 1.0
    Angular velocity in buffer: 1.0
    Force in memory: (1.0, 1.0)
    Force in buffer: (1.0, 1.0)
    Color in memory: (1, 1, 1, 255)
    Color in buffer: (1, 1, 1, 255)
    '''
    print("Initialization.")
    mod = ObjectModule()
    mod.mem.reg(key = "name", value = "0")
    print("ObjectModule: %s" % mod.info())
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
    mod.sense(reqt)
    print("Memory after sense.")
    pos = mod.get_pos()
    print("Position in memory: (%.1f, %.1f)" % (pos[0], pos[1]))
    print("Position in buffer: (%.1f, %.1f)" % (mod.buff["pos"][0], mod.buff["pos"][1]))
    angle = mod.get_angle()
    print("Angle in memory: %.1f" % angle)
    print("Angle in buffer: %.1f" % mod.buff["angle"])
    vel = mod.get_vel()
    print("Velocity in memory: (%.1f, %.1f)" % (vel[0], vel[1]))
    print("Velocity in buffer: (%.1f, %.1f)" % (mod.buff["vel"][0], mod.buff["vel"][1]))
    avel = mod.get_avel()
    print("Angular velocity in memory: %.1f" % avel)
    print("Angular velocity in buffer: %.1f" % mod.buff["avel"])
    force = mod.get_force()
    print("Force in memory: (%.1f, %.1f)" % (force[0], force[1]))
    print("Force in buffer: (%.1f, %.1f)" % (mod.buff["force"][0], mod.buff["force"][1]))
    color = mod.get_color()
    print("Color in memory: (%d, %d, %d, %d)" % (color[0], color[1], color[2], color[3]))
    print("Color in buffer: (%d, %d, %d, %d)" % (mod.buff["color"][0], mod.buff["color"][1], mod.buff["color"][2], mod.buff["color"][3]))


def test_objmod_act() :
    '''
    >>> test_objmod_act()
    Initialization.
    ObjectModule: <<multiagent.ObjectModule memory_size=1>>
    Message to '': <<multiagent.Message src= dest= key=vel value=(10, 10)>>
    Message to '': <<multiagent.Message src= dest= key=avel value=1>>
    Message to '': <<multiagent.Message src= dest= key=force value=(1, 1)>>
    Message to '': <<multiagent.Message src= dest= key=color value=(1, 1, 1, 255)>>
    '''
    print("Initialization.")
    mod = ObjectModule()
    mod.mem.reg(key = "name", value = "0")
    print("ObjectModule: %s" % mod.info())
    mod.apply_vel(vel = (10, 10))
    mod.apply_avel(avel = 1)
    mod.apply_force(force = (1, 1))
    mod.apply_color(color = (1, 1, 1, 255))
    resp = Response()
    mod.act(resp)
    for msg in resp.get_msgs(dest = "") :
        print("Message to '': %s" % msg.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[ObjectModule Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
