
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_oracle_init() :
    '''
    >>> test_oracle_init()
    Oracle: <<multiagent.OracleSpace objs_num=1 obts_num=1>>
    Object: <<multiagent.Object name=0>>
    Obstacle: <<multiagent.Obstacle name=0>>
    '''
    oracle = OracleSpace(objs = [Object(name = "0"),], obts = [Obstacle(name = "0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0),])
    print("Oracle: %s" % oracle.info())
    for name, obj in oracle.objs.items() :
        print("Object: %s" % obj.info())
    for name, obt in oracle.obts.items() :
        print("Obstacle: %s" % obt.info())

def test_oracle_add() :
    '''
    >>> test_oracle_add()
    Oracle: <<multiagent.OracleSpace objs_num=0 obts_num=0>>
    Add Object: <<multiagent.Object name=0>>
    Oracle: <<multiagent.OracleSpace objs_num=1 obts_num=0>>
    Add Obstacle: <<multiagent.Obstacle name=0>>
    Oracle: <<multiagent.OracleSpace objs_num=1 obts_num=1>>
    Clear Objects
    Oracle: <<multiagent.OracleSpace objs_num=0 obts_num=1>>
    '''
    oracle = OracleSpace()
    print("Oracle: %s" % oracle.info())
    obj = Object(name = "0")
    print("Add Object: %s" % obj.info())
    oracle.add_obj(obj)
    print("Oracle: %s" % oracle.info())
    obt = Obstacle(name = "0", a = (0.0, -1.0), b = (1.0, 0.0), radius = 2.0)
    print("Add Obstacle: %s" % obt.info())
    oracle.add_obt(obt)
    print("Oracle: %s" % oracle.info())
    print("Clear Objects")
    oracle.clear(dist = -1)
    print("Oracle: %s" % oracle.info())

def test_oracle_get() :
    '''
    >>> test_oracle_get()
    Oracle: <<multiagent.OracleSpace objs_num=1 obts_num=1>>
    Object: <<multiagent.Object name=0>>
    Object: None
    Obstacle: <<multiagent.Obstacle name=0>>
    Obstacle: None
    Objects within distance 10 from center (0, 0).
    Object: <<multiagent.Object name=0>>
    Obstacles within distance 10 from center (0, 0).
    Obstacle: <<multiagent.Obstacle name=0>>
    '''
    oracle = OracleSpace(objs = [Object(name = "0"),], obts = [Obstacle(name = "0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0),])
    print("Oracle: %s" % oracle.info())
    obj = oracle.get_obj_with(name = "0")
    print("Object: %s" % obj.info())
    obj = oracle.get_obj_with(name = "1")
    print("Object: %s" % obj)
    obt = oracle.get_obt_with(name = "0")
    print("Obstacle: %s" % obt.info())
    obt = oracle.get_obt_with(name = "1")
    print("Obstacle: %s" % obt)
    print("Objects within distance 10 from center (0, 0).")
    for obj in oracle.get_objs_at(c = (0, 0), d = 10, dist = ppdist_l2) :
        print("Object: %s" % obj.info())
    print("Obstacles within distance 10 from center (0, 0).")
    for obt in oracle.get_obts_at(c = (0, 0), d = 10, dist = pldist_l2) :
        print("Obstacle: %s" % obt.info())

def test_oracle_touch() :
    '''
    >>> test_oracle_touch()
    Oracle: <<multiagent.OracleSpace objs_num=1 obts_num=1>>
    Touching points within distance 10 from center (0, 0).
    Block: (0.0, 0.0)
    Block: (0.0, 1.0)
    '''
    oracle = OracleSpace(objs = [Object(name = "0"),], obts = [Obstacle(name = "0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0),])
    print("Oracle: %s" % oracle.info())
    print("Touching points within distance 10 from center (0, 0).")
    for block in oracle.touch(c = (0, 0), d = 10) :
        print("Block: (%.1f, %.1f)" % (block[2], block[3]))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Oracle Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
