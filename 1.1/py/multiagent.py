
import sys, os, time, datetime, json, math, inspect

import pygame
from pygame.locals import * 
from pygame.color import *

import pymunkoptions
pymunkoptions.options["debug"] = False
from pymunk import Circle, Segment, Body, Space, Vec2d

from utils import *


class Shape(object) : 
    
    def __init__(self) :
        self.__stroke_color = THECOLORS["blue"]
        self.__pointer_color = THECOLORS["red"]
        self.__fill_color = THECOLORS["blue"]
        self.__size = (0.0, 0.0)
        self.__pos = (0.0, 0.0)
        self.__angle = 0.0
        self.__mass = 0.0
   
    @property
    def stroke_color(self) :
        return self.__stroke_color 

    @stroke_color.setter
    def set_stroke_color(self, color) :
        self.__stroke_color = color
    
    @property
    def pointer_color(self) :
        return self.__pointer_color 

    @pointer_color.setter
    def set_pointer_color(self, color) :
        self.__pointer_color = color

    @property
    def fill_color(self) :
        return self.__fill_color 

    @fill_color.setter
    def set_fill_color(self, color) :
        self.__fill_color = color
    
    @property
    def size(self) :
        return self.__size

    @size.setter
    def set_size(self, size) :
        self.__size = size

    @property
    def pos(self) :
        return self.__pos

    @pos.setter
    def set_pos(self, pos) :
        self.__pos = pos 

    @property
    def angle(self) :
        return self.__angle

    @mass.setter
    def set_mass(self, angle) :
        self.__angle = angle

    @property
    def mass(self) :
        return self.__mass

    @mass.setter
    def set_mass(self, mass) :
        self.__mass = mass

    def draw(self, screen) :
        pass

class Object(Shape, Circle) :
    pass

class Obstacle(Shape, Segment) :
    pass

class Agent(object) : 

if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v1.1")
    print("")
    print("(c) 2017-2018, NiL, csningli@gmail.com.")
    print("")
    #print("Interactive Mode.")
    print("")
