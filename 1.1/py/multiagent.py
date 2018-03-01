
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
        self.__label = self.__name 

    def info(self) :
        return "<<multiagent.%s name=%s>>" % (type(self).__name__, self.name)

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, name) :
        self.__name = name

    @property
    def label(self) :
        return self.__label

    @label.setter 
    def label(self, label) :
        self.__label = label
    
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

    def info(self) :
        return "<<multiagent.%s name=%s>>" % (type(self).__name__, self.name)

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
    
    def __init__(self, objs = [], obts = []) : 
        super(OracleSpace, self).__init__()
        
        self.__objs = {}
        self.__obts = {} 

        for obj in objs : 
            self.add_obj(obj)
            
        for obt in obts : 
            self.add_obt(obt)

    def info(self) :
        return "<<multiagent.%s objs_num=%d obts_num=%d>>" % (type(self).__name__, len(self.__objs), len(self.__obts))

    def clear(self) :
        self.__objs = {}
        self.__obts = {}

    @property
    def objs(self) :
        return copy.copy(self.__objs)

    @property
    def obts(self) :
        return copy.copy(self.__obts)

    def add_obj(self, obj) :
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

    def add_obt(self, obt) :
        if check_attrs(obt, {"body" : None, "ends" : None,}) :
            self.add(obt.body, obt)
            self.__obts[obt.name] = obt

    def get_obj_with(self, name) : 
        return self.__objs.get(str(name), None)

    def get_obt_with(self, name) : 
        return self.__obts.get(str(name), None)

    def get_objs_at(self, c, l, dist = ppdist_l2) : 
        objs = {}
        if check_attrs(c, {"pos" : None, "radius" : None}) : 
            for (name, obj) in self.objs.items() : 
                if dist(c.pos, obj) < l + c.radius + obj.radius:
                    objs[name] = obj
        return objs 

    def get_obts_at(self, c, l, dist = pldist_l2) : 
        obts = {}
        if check_attrs(c, {"pos" : None, "radius" : None}) : 
            for obt in self.obts : 
                (start, end) = obt.ends
                if dist(c.pos, start, end) < l + c.radius:
                    obts.append(obt)
        return obts

    def draw(self, screen) :
        for obj in self.objs.values() + self.obts.values() :
            obj.draw(screen)

    def step(self) :
        pass


class Message(object) :
    def __init__(self, src = "", dest = "", key = "", value = "") :
        self.__src = src    # src == "" means 'from the context'
        self.__dest = dest  # dest == "" means 'to the context'
        self.__key = key
        self.__value = value 

    def info(self) :
        return "<<multiagent.%s src=%s dest=%s key=%s value=%s>>" % (type(self).__name__, self.__src, self.__dest, self.__key, self.__value)
        
    @property
    def src(self) :
        return self.__src

    @src.setter
    def src(self, src) :
        self.__src = str(src)

    @property
    def dest(self) :
        return self.__dest

    @dest.setter 
    def dest(self, dest) :
        self.__dest = str(dest)

    @property
    def key(self) :
        return self.__key

    @key.setter 
    def key(self, key) :
        self.__key = str(key)

    @property
    def value(self) :
        return self.__value

    @value.setter 
    def value(self, value) :
        self.__value = str(value)


class Request(object) :
    def __init__(self) :
        self.__content = {}

    def info(self) :
        return "<<multiagent.%s content_len=%d>>" % (type(self).__name__, len(self.__content.keys()))

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
                        "get_obj_with" : None,
                        "get_obt_with" : None,
                        "get_objs_at" : None,
                        "get_obts_at" : None,
                    }) :

                self.__oracle = oracle
            else :
                print("Invalid oracle for the construction of context. Exit.")
                exit(1)
        else :
            self.__oracle = OracleSpace()
            
        for obj in objs : 
            self.add_obj(obj)
            
        for obt in obts : 
            self.add_obj(obj)

        self.__reqt = None 
        self.__resp = None

    def info(self) :
        return "<<multiagent.%s has_oracle=%d>>" % (type(self).__name__, self.__oracle is not None)

    def handle_reqt(reqt) :
        self.__reqt = reqt 
        self.__resp = Response() 
        return self.__resp

    def draw(self, screen) :
        self.__oracle.draw(screen)

    def add_obj(self, obj) : 
        return self.__oracle.add_obj(obj)

    def add_obt(self, obt) : 
        return self.__oracle.add_obt(obt)
        


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
        self.__group_num = 0 
        self.__mods = []
        for mod in mods :
            self.add_mod(mod)
        self.__reqt = None
        self.__resp = None
    
    def info(self) :
        return "<<multiagent.%s name=%s mods_num=%d>>" % (type(self).__name__, self.__name, len(self.__mods))

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, name) :
        self.__name = name

    @property
    def group_num(self) :
        return self.__group_num

    @group_num.setter
    def group_num(self, num) :
        self.__group_num = num

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

    def info(self) :
        return "<<multiagent.%s read=%.4f delta=%.4f>>" % (type(self).__name__, self.__read, self.__delta)

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
        self.__queue = {} 

    def info(self) :
        return "<<multiagent.%s queue_len=%d>>" % (type(self).__name__, len(self.__queue))
    
    def add_obj(self, obj, delay = 0) :
        self.queue_append(item = obj, category = "objects", delay = delay)

    def add_obt(self, obt, delay = 0) :
        self.queue_append(item = obt, category = "obstacles", delay = delay)

    def add_agent(self, agent, delay = 0) :
        self.queue_append(item = agent, category = "agents", delay = delay)

    def queue_append(self, item, category, delay = 0) :
        if int(delay) not in self.__queue.keys() :
            self.__queue[int(delay)] = {
                "objects" : [],
                "obstacles" : [],
                "agents" : [],
            }
        if category in ["objects", "obstacles", "agents"] :
            self.__queue[int(delay)][category].append(item)

    def queue_pop(self) : 
        item = self.__queue.get(0, {"objects" : [], "obstacles" : [], "agents" : [],})
        self.__queue[0] = {
            "objects" : [],
            "obstacles" : [],
            "agents" : [],
        }
        
        delays = list(self.__queue.keys())
        delays.sort()
        for delay in delays :
            if delay < 1 : 
                continue 
            else :
                self.__queue[delay - 1] = self.__queue[delay]
                self.__queue[delay] = self.__queue.get(delay + 1, {"objects" : [], "obstacles" : [], "agents" : [],})

        return item
        
        
class Driver(object) : 
    def __init__(self, context, schedule, delta = 0.01, data = None) : 
        if check_attrs(context, {"handle_reqt" : None}) :
            self.__context = context 
        else :
            print("Invalid context for the construction of driver. Exit.")
            exit(1)

        if check_attrs(schedule, {"queue_pop" : None}) :
            self.__schedule = schedule
            self.__agents = {}
        else :
            print("Invalid schedule for the construction of driver. Exit.")
            exit(1)

        if type(delta).__name__ in ["float", "int"] :
            self.__timer = Timer(float(delta))
        else :
            print("Invalid delta for the construction of driver. Exit.")
            exit(1)


        self.__steps = 0
        if data is not None :
            if check_attrs(data, {"add_shot" : None, "get_shot" : None}) :
                self.__data = data
                self.__steps = data.get_steps()
                self.restore() 
            else :
                print("Invalid data for the construction of driver. Exit.")
                exit(1)
        else : 
            self.__data = Data()
            
        self.__reqt = None
        self.__resp = None

    @property
    def steps(self) :
        return self.__steps

    @property
    def time(self) :
        return self.__timer.read
        
    def info(self) :
        return "<<multiagent.%s has_context=%d has_schedule=%d has_timer=%d agents_num=%d>>" % (type(self).__name__, self.__context is not None, self.__schedule is not None, self.__timer is not None, len(self.__agents))

    def draw(self, screen) :
        self.__context.draw(screen)

    def go(self) :
        result = True 
        self.__steps += 1
        #agents = self.__shedule.pop_agents()
        #for agent in agents :
            #if check_attrs(agent, {"name" : None, "handle_reqt" : None}) :
                #self.__agents[agent.name] = agent
            
        #self.__resp = self.__context.handle_reqt(self.__reqt)
        #self.__reqt = Response()
        #for name, agent in self.agents.items() :
            #reqt = Request()
            #msgs = self._resp.get_msgs(name)
            #for msg in msgs : 
                #msg.src = ""
                #reqt.add_msg(msg)
            #resp = agent.handle_reqt(reqt) 

            #msgs = resp.get_msgs("")
            #for msg in msgs : 
                #msg.src = name
        #        self.__reqt.add_msg(msg)

        return result


    def back(self) :    
        result = True 
        if self.__steps > 0 :
            self.__steps -= 1
        return result

    def restore(self) :
        pass


class Simulator(object) : 
    driver_attrs = {
        "go" : None,
        "back" : None,
    }
    
    inspector_attrs = {
    }
    
    def __init__(self, driver, inspector = None) :
        self.__driver = None
        if driver is not None and check_attrs(driver, self.driver_attrs) :
            self.__driver = driver 
        else :
            print("Invalid driver. Exit")
            exit(1)
            
        if inspector is None or check_attrs(inspector, self.inspector_attrs) :
            self.__inspector = inspector 
        else :
            
            print("Invalid inspector. Exit")
            exit(1)

    def info(self) :
        return "<<multiagent.%s has_driver=%d>>" % (type(self).__name__, self.__driver is not None)

        
    def simulate(self, inspector = None, graphics = False, width = 800, height = 800, limit = None) :
        if self.__driver is None :
            print("No valid driver given. Return.")
            return False 

        if inspector is None : 
            inspector = self.__inspector
        
        pygame.init()
        screen = None
        if graphics == True :
             screen = pygame.display.set_mode((width, height))
        
        clock = pygame.time.Clock()
        
        font = pygame.font.Font(None, 16)
        help_info = [
                "ESC: quit; Space: pause/run;",
                "Key 'left': prev step; Key 'right': next step;",
                "Key 'up': speed up; Key 'down': speed down;",
        ]
        
        delay = 0       # delay between handling key presses
        speed = 1         # number of rounds in one step
        phases = None     # number of steps to run; None for ever 

        running = True
        pause = False 
        
        while (limit is None or self.__driver.steps < limit) and running :
            updated = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN :
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pause = not pause
                        if pause == False :
                            if limit is None :
                                phases = None
                            else :
                                phases = int(math.ceil((limit - self.__driver.steps) / float(speed)))

            keys = pygame.key.get_pressed() 
            
            if delay > 0 : 
               delay -= 1
            elif keys[K_UP] :
                speed = min(100, speed + 1)
                delay = 10
                updated = True
            elif keys[K_DOWN] :
                speed = max(1, speed - 1)
                delay = 10
                updated = True
            elif keys[K_RIGHT] :
                if pause == True :
                    phases = 1
                    pause = False
                delay = 10
            elif keys[K_LEFT] :
                if pause == True :
                    phases = -1
                    pause = False
                delay = 10

            clock.tick(50)
            
            if (phases is None or phases != 0) and (pause == False) : 
               
                if phases is None or phases > 0 : 
                    for i in range(speed) :
                        self.__driver.go()
                    if phases is not None and phases > 0 :
                        phases -= 1
                    #if inspector is not None and not inspector.check(driver = self.__driver) : 
                        #pause = True
                elif phases < 0 :
                    for i in range(speed) :
                        self.__driver.back() 
                    phases += 1

                if phases == 0 :
                    pause = True

                updated = True

            if updated == True and screen is not None :
            
                screen.fill(THECOLORS["white"])
                
                self.__driver.draw(screen)
                pygame.display.flip()

                sim_info = [ 
                    "{:<10}".format("Speed:") + "%d" % speed, 
                    "{:<10}".format("Steps:") + "%d" % self.__driver.steps, 
                    "{:<10}".format("Time:") + "%2.6f" % self.__driver.time, 
                ]
                
                y = 5
                for line in sim_info:
                    screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                    y += 10

                y = height - 20
                for line in help_info:
                    screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                    y -= 10
                    
                pygame.display.set_caption("MultiAgent Simulator v1.1 (c) 2017-2018, NiL, csningli@gmail.com")
                pygame.display.flip()


if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v1.1 (c) 2017-2018, NiL, csningli@gmail.com.")
    
