#! /Users/nil/anaconda3/bin/python

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def test_data() :
    '''
    >>> test_data() 
    step_label = 0, name_label = node, key = test_key : {'0': {'node': {'test_key': '10'}}}
    step_label = 0, name_label = node, key = test_key2 : {'0': {'node': {'test_key2': '10'}}}
    step_label = 0, name_label = node : {'0': {'node': {'test_key': '10', 'test_key2': '10'}}}
    step_label = 0, name_label = node2 : {'0': {'node2': {'test_key2': '10'}}}
    step_label = 0 : {'0': {'node': {'test_key': '10', 'test_key2': '10'}, 'node2': {'test_key2': '10'}}}
    step_label = 1 : {'1': {'node2': {'test_key2': '10'}}}
    result: {'1': {'node2': {'test_key2': '10'}}, '0': {'node': {'test_key': '10', 'test_key2': '10'}, 'node2': {'test_key2': '10'}}}
    '''
    step_label = str(0)
    name_label = 'node'
    key = 'test_key'
    value = '10'
    data = Data()
    data.update(data_value = {step_label : {name_label : {key : value}}})
    none_value = {step_label : {name_label : {key : None}}}
    result = data.get(none_value = none_value)
    print("step_label = %s, name_label = %s, key = %s : %s" % (step_label, name_label, key, result))
    key = 'test_key2'
    value = '10'
    data.update(data_value = {step_label : {name_label : {key : value}}})
    none_value = {step_label : {name_label : {key : None}}}
    result = data.get(none_value = none_value)
    print("step_label = %s, name_label = %s, key = %s : %s" % (step_label, name_label, key, result))
    none_value = {step_label : {name_label : None}}
    result = data.get(none_value = none_value)
    print("step_label = %s, name_label = %s : %s" % (step_label, name_label, result))
    name_label = 'node2'
    data.update(data_value = {step_label : {name_label : {key : value}}})
    none_value = {step_label : {name_label : None}}
    result = data.get(none_value = none_value)
    print("step_label = %s, name_label = %s : %s" % (step_label, name_label, result))
    none_value = {step_label :  None}
    result = data.get(none_value = none_value)
    print("step_label = %s : %s" % (step_label, result))
    step_label = str(1)
    data.update(data_value = {step_label : {name_label : {key : value}}})
    none_value = {step_label :  None}
    result = data.get(none_value = none_value)
    print("step_label = %s : %s" % (step_label, result))
    none_value = {}
    result = data.get(none_value = none_value)
    print("result: %s" % result)

    
def test_zipper() :
    '''
    >>> test_zipper() 
    Step data: {'0': {'key': 'value2'}}
    Step data: None
    Step data: {'0': {'key': 'value1'}}
    '''
    data = Data()
    data.update(data_value = {"0" : {"0" : {"key" : "value1"}}, "1" : {"0" : {"key" : "value2"}}})
    zipper = Zipper(data = data, context = None, objects = [])
    step_data = zipper.forward()
    print("Step data: %s"  % step_data)
    step_data = zipper.forward()
    print("Step data: %s"  % step_data)
    step_data = zipper.backward()
    print("Step data: %s"  % step_data)


if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Zipper Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 




