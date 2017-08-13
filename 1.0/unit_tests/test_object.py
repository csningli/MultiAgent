
import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 


def test_object() :
    '''
    >>> test_object()
    Object: <multiagent.Object name=test_obj>
    pre: {'pre_key': 'pre_value'}
    local: {'local_key': 'local_value'}
    Object status: {'pre': {'local_key': 'local_value', 'pre_key': 'pre_value'}, 'mem': {'mem_key': 'mem_value'}, 'post': {}, 'local': {}}
    '''
    obj = Object(name = "test_obj", mods = [Module()])
    print("Object: %s" % obj)
    pre = {"pre_key" : "pre_value"}
    local = {"local_key" : "local_value"}
    mem = {"mem_key" : "mem_value"}
    print("pre: %s" % pre)
    print("local: %s" % local)
    obj.status["pre"] = pre
    obj.status["local"] = local 
    obj.status["mem"] = mem
    obj.step(obj_data = None)
    print("Object status: %s" % obj.status)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Object Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 



