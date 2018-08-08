
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
from mas.multiagent import *

def test_shot_basic() :
    '''
    >>> test_shot_basic()
    Initialization.
    Shot: <<multiagent.Shot obj_props_len=0 obt_props_len=0 context_paras_len=0 agent_memos_len=0>>
    '''
    print("Initialization.")
    shot = Shot()
    print("Shot: %s" % shot.info())

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Shot Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
