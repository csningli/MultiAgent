
# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, copy, time, datetime, json, math, inspect

from numpy import array, dot
from numpy.linalg import norm

import pygame
from pygame.locals import * 
from pygame.color import *

import pymunkoptions
pymunkoptions.options["debug"] = False
from pymunk import Circle, Segment, Body, Space, Vec2d, moment_for_circle


from utils import *
from geometry import *


class Shot(object) :
    def __init__(self) :
        self.__shot = {
            "obj_props" : {
            },
            "context_paras" : {
            },
            "agent_memos" : {
            },
        }

    def get_obj_props(self) :
        return copy.copy(self.__shot["obj_props"])

    def get_agent_memos(self) :
        return copy.copy(self.__shot["agent_memos"])

    def get_context_paras(self) :
        return copy.copy(self.__shot["context_paras"])

    def set_obj_prop(self, name, key, value = None) :
        if name not in self.__shot["obj_props"].keys() :
            self.__shot["obj_props"][name] = {}
        self.__shot["obj_props"][name][key] = value

    def set_anget_memo(self, name, key, value = None) :
        if name not in self.__shot["agent_memos"].keys() :
            self.__shot["agent_memos"][name] = {}
        self.__shot["agent_memos"][name][key] = value  

    def set_context_para(self, key, value = None) :
        self.__shot["context_paras"][key] = value  
        
        
    
class Data(object) : 
    def __init__(self) :
        self.__data = []

    def add_shot(self, shot) :
        if check_attrs(shot, {}) :
            self.data.append(shot)

    def get_shot(self, index) :
        if type(index).__name__ == "int" and index >= 0 and index < self.__data.size() :
            return self.__data[index]
            


class Inspector(object) : 
    pass


class LookMixin : 

    __stroke_color = THECOLORS["black"]
    __pointer_color = THECOLORS["black"]
    __fill_color = THECOLORS["black"]
    
    @property
    def stroke_color(self) :
        return self.__stroke_color 

    @stroke_color.setter
    def stroke_color(self, color) :
        self.__stroke_color = color
    
    @property
    def pointer_color(self) :
        return self.__pointer_color 

    @pointer_color.setter
    def pointer_color(self, color) :
        self.__pointer_color = color

    @property
    def fill_color(self) :
        return self.__fill_color 

    @fill_color.setter
    def fill_color(self, color) :
        self.__fill_color = color
    

class Object(Circle, LookMixin) :
    def __init__(self, name, mass = 1.0, radius = 10.0) :
        body = Body(mass = mass, moment = moment_for_circle(mass, 0, radius, (0,0)))
        super(Object, self).__init__(body, radius, (0, 0))
        self.__name = name

    def __str__(self) :
        return "<multiagent.%s name=%s>" % (type(self).__name__, self.name)

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, name) :
        self.__name = name
    
    @property
    def pos(self) :
        return tuple(self.body.position)
        
    @pos.setter
    def pos(self, pos) :
        self.body.position = pos

    @property
    def angle(self) :
        return self.body.angle
    
    @angle.setter
    def angle(self, angle) :
        self.body.angle = angle
        
    @property
    def rot(self) :
        return tuple(self.body.rotation_vector)
    
    @rot.setter
    def rot(self, rot) :
        self.body.rot = tuple(rot) 
        
    @property
    def vel(self) :
        return self.body.velocity 
        
    @vel.setter
    def vel(self, vel) :
        self.body.velocity = vel

    @property
    def avel(self) :
        return self.body.angular_velocity

    @avel.setter
    def avel(self, avel) :
        self.body.angular_velocity = avel 

    @property
    def force(self) :
        return self.body.force

    @force.setter
    def force(self, force) :
        self.body.force = force

    def draw(self, screen) :
        p = self.pos
        rot = self.rot
        (width, height) = screen.get_size()

        # adjust the drawing coordinates to make sure (0, 0) stays in the center
        
        p[0] = int(width / 2.0 + p[0]) 
        p[1] = int(height / 2.0 - p[1]) 

        head = Vec2d(rot.x, -rot.y) * self.radius * 0.9
        pygame.draw.circle(screen, self.stroke_color, p, int(r), 2)
        pygame.draw.circle(screen, self.fill_color, p, int(r/2.0), 4)
        pygame.draw.line(screen, self.pointer_color, p, p + head)
    

class Obstacle(Segment, LookMixin) :
    def __init__(self, name, a = (0.0, 0.0), b = (0.0, 0.0), radius = 0.0) :
        super(Obstacle, self).__init__(Body(body_type = Body.STATIC), a, b, radius)    
        self.__name = name

    def __str__(self) :
        return "<multiagent.%s name=%s>" % (type(self).__name__, self.name)

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, name) :
        self.__name = name

    @property
    def ends(self) :
        body = self.body
        start = body.position + self.a.cpvrotate(body.rotation_vector)
        end = body.position + self.b.cpvrotate(body.rotation_vector)
        return (tuple(start), tuple(end))

    def draw(self, screen) :
        (width, height) = screen.get_size()
        (start, end) = self.get_ends()
        start_t = (int(width / 2.0 + start[0]), int(height / 2.0 - start[1])) 
        end_t = (int(width / 2.0 + end[0]), int(height / 2.0 - end[1]))
        pygame.draw.lines(screen, self.stroke_color, False, [start_t, end_t])
        

class Oracle(object) : 
    
    def __init__(self, objects = [], obstacles = []) : 
        self.__objs = {}
        self.__obstacles = {} 

        for obj in objects : 
            self.add_obj(obj)
            
        for obt in obstacles : 
            self.add_obt(obt)

    @property
    def objects(self) :
        return copy(self.__objects)

    @property
    def obstacles(self) :
        return copy(self.__obstacles)

    def add_obj(obj) :
        if check_attrs(obj, {"name" : None, "pos" : None, "angle" : None, "rot" : None, 
                "vel" : None, "avel" : None, "force" : None}) :
            self.__objects[obj.name] = obj

    def add_obt(obt) :
        if check_attrs(obt, {"ends" : None,}) :
            self.__obstacles[obt.name] = obt

    def get_obj_by_name(name) : 
        return self.__objects.get(str(name), None)

    def get_objs_by_range(c, l, dist = ppdist_l2) : 
        objs = {}
        if check_attrs(c, {"pos" : None, "radius" : None}) : 
            for (name, obj) in self.objects.items() : 
                if dist(c.pos, obj) < l + c.radius + obj.radius:
                    objs[name] = obj
        return objs 

    def get_obts_by_range(c, l, dist = pldist_l2) : 
        obts = {}
        if check_attrs(c, {"pos" : None, "radius" : None}) : 
            for obt in self.obstacles : 
                (start, end) = obt.ends
                if dist(c.pos, start, end) < l + c.radius:
                    obts.append(obt)
        return obts
    
class Context(object) : 
    pass
    

class Agent(object) : 
    pass



    

class Driver(object) : 
    pass


class Simulator(object) : 
    pass


if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v1.1 (c) 2017-2018, NiL, csningli@gmail.com.")
