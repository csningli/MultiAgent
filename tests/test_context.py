
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_context_basic() :
    '''
    >>> test_context_basic()
    Initialization.
    Context: <<multiagent.Context has_oracle=1>>
    Time: 0.0000
    Object: <<multiagent.Object name=0>>
    Obstacle: <<multiagent.Obstacle name=0>>
    '''
    print("Initialization.")
    oracle = OracleSpace()
    context = Context(oracle = oracle, delta = 0.02, objs = [Object(name = "0"), ], obts = [Obstacle(name ="0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0), ])
    print("Context: %s" % context.info())
    print("Time: %.4f" % context.time)
    for name, obj in context.oracle.objs.items() :
        print("Object: %s" % obj.info())
    for name, obt in context.oracle.obts.items() :
        print("Obstacle: %s" % obt.info())

def test_context_add() :
    '''
    >>> test_context_add()
    Initialization.
    Context: <<multiagent.Context has_oracle=1>>
    Add object: <<multiagent.Object name=0>>
    Add object: <<multiagent.Object name=1>>
    Object: <<multiagent.Object name=1>>
    Object: <<multiagent.Object name=0>>
    Add obstacle: <<multiagent.Obstacle name=0>>
    Obstacle: <<multiagent.Obstacle name=0>>
    '''
    print("Initialization.")
    context = Context()
    print("Context: %s" % context.info())
    obj = Object(name = "0")
    print("Add object: %s" % obj.info())
    context.add_obj(obj)
    obj = Object(name = "1")
    print("Add object: %s" % obj.info())
    context.add_obj(obj)
    for name, obj in context.oracle.objs.items() :
        print("Object: %s" % obj.info())
    obt = Obstacle(name ="0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0)
    print("Add obstacle: %s" % obt.info())
    context.add_obt(obt)
    for name, obt in context.oracle.obts.items() :
        print("Obstacle: %s" % obt.info())


def test_context_get() :
    '''
    >>> test_context_get()
    Initialization.
    Context: <<multiagent.Context has_oracle=1>>
    Get time by 10 steps.
    Time: 0.1
    Objects within distance 10 from center (0, 0).
    Object: <<multiagent.Object name=0>>
    Obstacles within distance 10 from center (0, 0).
    Obstacle: <<multiagent.Obstacle name=0>>
    '''
    print("Initialization.")
    context = Context(objs = [Object(name = "0"), ], obts = [Obstacle(name ="0", a = (0.0, 1.0), b = (1.0, 0.0), radius = 2.0), ])
    print("Context: %s" % context.info())
    print("Get time by 10 steps.")
    print("Time: %s" % context.get_time_by_steps(steps = 10))
    print("Objects within distance 10 from center (0, 0).")
    for obj in context.get_objs_at(pos = (0, 0), d = 10) :
        print("Object: %s" % obj.info())
    print("Obstacles within distance 10 from center (0, 0).")
    for obt in context.get_obts_at(pos = (0, 0), d = 10) :
        print("Obstacle: %s" % obt.info())

def test_context_para() :
    '''
    >>> test_context_para()
    Initialization.
    Context: <<multiagent.Context has_oracle=1>>
    Time: 0.0000
    Change parameters by directly apply 'context.paras = paras', where 'paras' is a map storing the new values.
    Time: 0.5000
    '''
    print("Initialization.")
    context = Context()
    print("Context: %s" % context.info())
    print("Time: %.4f" % context.time)
    print("Change parameters by directly apply 'context.paras = paras', where 'paras' is a map storing the new values.")
    paras = {"time" : "0.5"}
    context.paras = paras
    print("Time: %.4f" % context.time)

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Context Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
