
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_mem_basic() :
    '''
    >>> test_mem_basic()
    Initialization.
    Memory: <<multiagent.Memory content_size=0>>
    '''
    print("Initialization.")
    mem = Memory()
    print("Memory: %s" % mem.info())
    for key, value in mem.content.items() :
        print("Key: %s - Value: %s" % (key, value))


def test_mem_reg_read() :
    '''
    >>> test_mem_reg_read()
    Initialization.
    Memory: <<multiagent.Memory content_size=0>>
    Key: key - Value: value
    Read value of key: 'key'
    Value of key 'key': value
    Read value of key: 'miss'
    Value of key 'miss': not found
    '''
    print("Initialization.")
    mem = Memory()
    print("Memory: %s" % mem.info())
    mem.reg(key = "key", value = "value")
    for key, value in mem.content.items() :
        print("Key: %s - Value: %s" % (key, value))
    print("Read value of key: 'key'")
    value = mem.read(key = "key")
    print("Value of key 'key': %s" % value)
    print("Read value of key: 'miss'")
    value = mem.read(key = "miss", default_value = "not found")
    print("Value of key 'miss': %s" % value)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Request Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
