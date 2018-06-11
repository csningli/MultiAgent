
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def test_msg_basic() :
    '''
    >>> test_msg_basic()
    Initialization.
    Message: <<multiagent.Message src=0 dest=1 key=key value=value>>
    Change values of the properties.
    Source: 1
    Destination: 0
    Key: new_key
    Value: new_value
    '''
    print("Initialization.")
    msg = Message(src = "0", dest = "1", key = "key", value = "value")
    print("Message: %s" % msg.info())
    print("Change values of the properties.")
    msg.src = "1"
    print("Source: %s" % msg.src)
    msg.dest = "0"
    print("Destination: %s" % msg.dest)
    msg.key = "new_key"
    print("Key: %s" % msg.key)
    msg.value = "new_value"
    print("Value: %s" % msg.value)

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[Message Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
