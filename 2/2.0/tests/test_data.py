
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_data_basic() :
    '''
    >>> test_data_basic()
    Initialization.
    Data: <<multiagent.Data size=0 filename=multiagent.data>>
    Size: 0
    Filename: multiagent.data
    '''
    print("Initialization.")
    data = Data(filename = "multiagent.data")
    print("Data: %s" % data.info())
    print("Size: %d" % data.size)
    print("Filename: %s" % data.filename)


def test_data_add_get() :
    '''
    >>> test_data_add_get()
    Initialization.
    Data: <<multiagent.Data size=0 filename=multiagent.data>>
    Add shot: <<multiagent.Shot obj_props_len=0 obt_props_len=0 context_paras_len=0 agent_memos_len=0>>
    Get shot: <<multiagent.Shot obj_props_len=0 obt_props_len=0 context_paras_len=0 agent_memos_len=0>>
    '''
    print("Initialization.")
    data = Data(filename = "multiagent.data")
    print("Data: %s" % data.info())
    shot = Shot()
    print("Add shot: %s" % shot.info())
    data.add_shot(shot = shot)
    shot = data.get_shot(index = 0)
    print("Get shot: %s" % shot.info())


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Data Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
