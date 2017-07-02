
import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 
from pymunk import Circle, Body, Vec2d


def test_shape() :
    '''
    >>> test_shape()
    Shape type: CircleShape
    position: Vec2d(0.0, 0.0)
    angle: 0.0
    range: (10.0, 10.0)
    '''
    shape = CircleShape(Body(10.0, 10.0), 10.0, (0.0, 0.0))
    print("Shape type: %s" % type(shape).__name__)
    print("position: %s" % shape.get_position())
    print("angle: %s" % shape.get_angle())
    print("range: (%s, %s)" % shape.get_range())

def test_unit() :
    '''
    >>> test_unit()
    Unit name: test_unit
    position: Vec2d(0.0, 0.0)
    angle: 0.0
    '''
    unit = Unit(name = "test_unit")
    print("Unit name: %s" % unit.name)
    print("position: %s" % unit.get_position())
    print("angle: %s" % unit.get_angle())
    

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50) 
    print("[Unit Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed)) 


