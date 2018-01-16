
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


class LookMixin(object) : 
    '''
    This class has the 'look', and hence its instances can be drawn on the screen.
    '''

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
        

class OracleSpace(Space) : 
    
    def __init__(self, objects = [], obstacles = []) : 
        super(OracleSpace, self).__init__()
        
        self.__objs = {}
        self.__obts = {} 

        for obj in objs : 
            self.add_obj(obj)
            
        for obt in obts : 
            self.add_obt(obt)

    def clear(self) :
        self.__objs = {}
        self.__obts = {}

    @property
    def objs(self) :
        return copy(self.__objs)

    @property
    def obts(self) :
        return copy(self.__obts)

    def add_obj(obj) :
        if check_attrs(obj, 
                {   "body" : None,
                    "name" : None, 
                    "pos" : None, 
                    "angle" : None, 
                    "rot" : None, 
                    "vel" : None, 
                    "avel" : None, 
                    "force" : None,
                }) :

            self.add(obj.body, obj)
            self.__objs[obj.name] = obj

    def add_obt(obt) :
        if check_attrs(obt, {"body" : None, "ends" : None,}) :
            self.add(obj.body, obj)
            self.__obts[obt.name] = obt

    def get_obj_by_name(name) : 
        return self.__objs.get(str(name), None)

    def get_obt_by_name(name) : 
        return self.__obts.get(str(name), None)

    def get_objs_by_range(c, l, dist = ppdist_l2) : 
        objs = {}
        if check_attrs(c, {"pos" : None, "radius" : None}) : 
            for (name, obj) in self.objs.items() : 
                if dist(c.pos, obj) < l + c.radius + obj.radius:
                    objs[name] = obj
        return objs 

    def get_obts_by_range(c, l, dist = pldist_l2) : 
        obts = {}
        if check_attrs(c, {"pos" : None, "radius" : None}) : 
            for obt in self.obts : 
                (start, end) = obt.ends
                if dist(c.pos, start, end) < l + c.radius:
                    obts.append(obt)
        return obts



class Message(object) :
    def __init__(self, src = "", dest = "", key = "", value = "") :
        self.__src = src    # src == "" means 'from the context'
        self.__dest = dest  # dest == "" means 'to the context'
        self.__key = key
        self.__value = value 

    @property
    def src(self) :
        return self.__src

    @src.setter(self, src) :
    def src(self, src) :
        self.__src = str(src)

    @property
    def dest(self) :
        return self.__dest

    @dest.setter(self, dest) :
    def dest(self, dest) :
        self.__dest = str(dest)

    @property
    def key(self) :
        return self.__key

    @key.setter(self, key) :
    def key(self, key) :
        self.__key = str(key)

    @property
    def value(self) :
        return self.__value

    @value.setter(self, value) :
    def value(self, value) :
        self.__value = str(value)


class Request(object) :
    def __init__(self) :
        self.__content = {}

    @property
    def content(self) :
        return copy.copy(self.__content)

    def add_msg(self, msg) :
        if check_attrs(msg, {"src" : None, "dest" : None, "key" : None, "value" : None}) and msg.dest != "" : 
            if msg.dest not in self.__content.keys() :
                self.__content[str(msg.dest)] = [] 
            self.__content[str(msg.dest)].append(msg)

    def get_msgs(self, dest) :
        return self.__content.get(str(dest), [])
        

class Response(Request) :
    pass


class Context(object) : 
    def __init__(self, objs = [], obts = [], oracle = None) :  
        if oracle is not None : 
            if check_attrs(oracle, 
                    {   "objs" : None, 
                        "obts" : None, 
                        "add_obj" : None,
                        "add_obt" : None,
                        "get_obj_by_name" : None,
                        "get_obt_by_name" : None,
                        "get_objs_by_range" : None,
                        "get_obts_by_range" : None,
                    }) :

                self.__oracle = oracle
            else :
                print("Invalid oracle for the construction of context. Exit.")
                exit(1)
        else :
            self.__oracle = OracleSpace()
            
        for obj in objs : 
            self.__oracle.add_obj(obj)
            
        for obt in obts : 
            self.__oracle.add_obt(obt)

        self.__reqt = None 
        self.__resp = None

    def handle_reqt(reqt) :
        self.__reqt = reqt 
        self.__resp = Response() 
        
        return self.__resp


class Buffer(object) :
    def __init__(self) :
        self.__content = {}

    def reg(self, key, value) :
        self.__content[key] = value

    def read(self, key, default_value) :
        return self.__content.get(key, default_value) 
    
    
class Module(object) :
    def __init__(self) : 
        self.__buff = Buffer() 

    def sense(self, reqt, resp) :
        pass

    def process(self, reqt, resp) :
        pass

    def act(self, reqt, resp) :
        pass
        

class Agent(object) : 
    def __init__(self, name, mods = []) : 
        self.__name = name
        self.__mods = []
        for mod in mods :
            self.add_mod(mod)
        self.__reqt = None
        self.__resp = None

    @property
    def name(self) :
        return name

    @name.setter
    def name(self, name) :
        self.__name = name

    def add_mod(self, mod) :
        if check_attrs(mod, {"sense" : None, "process" : None, "act" : None}) :
            self.__mods.append(mod)

    def handle_reqt(self, reqt) :
        self.__reqt = reqt
        self.__resp = Response()

        for mod in mods :
            mod.sense(self.__reqt, self.__resp)

        for mod in mods :
            mod.process(self.__reqt, self.__resp)

        for mod in mods :
            mod.act(self.__reqt, self.__resp)

        return self.__resp
    

class Shot(object) :
    def __init__(self) :
        self.__shot = {
            "obj_props" : {
            },
            "obj_props" : {
            },
            "context_paras" : {
            },
            "agent_memos" : {
            },
        }

    @property
    def obj_props(self) :
        return copy.copy(self.__shot["obj_props"])

    @property
    def agent_memos(self) :
        return copy.copy(self.__shot["agent_memos"])

    @property
    def context_paras(self) :
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


class Timer(object) :
    def __init__(self, delta = 0.01) :
        self.__read = 0.0
        self.__delta = delta

    @property
    def read(self) :
        return self.__read

    @read.setter
    def read(self, read) :
        self.__read = read

    @property
    def delta(self) :
        return self.__delta 

    @delta.setter
    def delta(self, delta) :
        self.__delta = delta

    def tick(self, delta = None) :
        if delta is not None :
            self.__read += delta
        else :
            self.__read += self.__delta

    def tack(self, delta = None) :
        if delta is not None :
            self.__read -= delta
        else :
            self.__read -= self.__delta

        if self.__read < 0 : 
            self.__read = 0


class Schedule(object) :
    def __init__(self) : 
        self.__agents = {} 

    def add_agent(self, agent, delay = 0) :
        if check_attrs(agent, {"name" : None, "handle_reqt" : None}) :
            if int(delay) not in self.__agents.keys() :
                self.__agents[int(delay)] = []
            self.__agents[int(delay)].append(agent)

    def pop_agents(self) : 
        agents = self.__agents.get(0, [])
        
        delays = list(self.__agents.keys())
        delays.sort()
        for delay in delays :
            if delay < 1 : 
                continue 
            else :
                self.__agents[delay - 1] = self.__agents[delay]
                self.__agents[delay] = self.__agents.get(delay + 1, [])

        return agents 
        
        
class Driver(object) : 
    def __init__(self, context, schedule, delta = 0.01) : 
        if check_attrs(context, ) :
            self.__context = context 
        else :
            print("Invalid context for the construction of driver. Exit.")
            exit(1)

        if check_attrs(schedule, {"get_agents" : None}) :
            self.__schedule = schedule
            self.__agents = {}
        else :
            print("Invalid schedule for the construction of driver. Exit.")
            exit(1)

        if check_attrs(context, ) :
            self.__context = context 
        else :
            print("Invalid context for the construction of driver. Exit.")
            exit(1)
            
        if type(delta).__name__ in ["float", "int"] :
            self.__timer = Timer(float(delta))
        else :
            print("Invalid delta for the construction of driver. Exit.")
            exit(1)

        self.__data = Data()
        self.__reqt = None
        self.__resp = None

    @property
    def time(self) :
        return self.__timer.read()

    def go(self) :
        agents = self.__shedule.pop_agents()
        for agent in agents :
            if check_attrs(agent, {"name" : None, "handle_reqt" : None}) :
                self.__agents[agent.name] = agent
            
        self.__resp = self.__context.handle_reqt(self.__reqt)
        self.__reqt = Response()
        for name, agent in self.agents.items()
            reqt = Request()
            msgs = self._resp.get_msgs(name)
            for msg in msgs : 
                msg.src = ""
                reqt.add_msg(msg)
            resp = agent.handle_reqt(reqt) 

            msgs = resp.get_msgs("")
            for msg in msgs : 
                msg.src = name
                self.__reqt.add_msg(msg)


    def back(self) :    
        pass


class Simulator(object) : 
    pass


if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v1.1 (c) 2017-2018, NiL, csningli@gmail.com.")
