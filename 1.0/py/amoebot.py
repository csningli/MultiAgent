import sys, os, time, datetime, json, math, inspect
import pygame
from pygame.locals import * 
from pygame.color import *

from numpy import array, dot 
from numpy.linalg import norm

from utils import distance_to_line

from multiagent import Timer, Space, Logger, check_attrs

amoebot_paras = {
    "radius" : 10.0,
}

def pq_to_xy(a) :
    b = array([0.0, 0.0])
    p = a[0]
    q = a[1]
    x = 2 * amoebot_paras["radius"] * p + 2 * amoebot_paras["radius"] *  math.cos(math.pi / 3.0) * q 
    y = 2 * amoebot_paras["radius"] *  math.cos(math.pi / 6.0) * q
    b[0] = x
    b[1] = y
    return b

def wq_to_xy(a) :
    b = array([0.0, 0.0])
    p = a[0]
    q = a[1]
    x = -2 * amoebot_paras["radius"] * p + -2 * amoebot_paras["radius"] *  math.cos(math.pi / 3.0) * q 
    y = 2 * amoebot_paras["radius"] *  math.cos(math.pi / 6.0) * q
    b[0] = x
    b[1] = y
    return b
    
def xy_to_pq(b) :
    a = array([0.0, 0.0])
    x = b[0]
    y = b[1]
    q = int(float(y) / (2 * amoebot_paras["radius"] *  math.cos(math.pi / 6.0)))
    p = int((float(x) -  2 * amoebot_paras["radius"] *  math.cos(math.pi / 3.0) * q) / (2 * amoebot_paras["radius"])) - q
    a[0] = p
    a[1] = q
    return a


class BotShape(Logger) :
    def __init__(self) :
        self.radius = float(amoebot_paras["radius"])
        self.head_pos = array([0.0, 0.0])
        self.tail_pos = array([0.0, 0.0])
        self.stroke_color = THECOLORS["black"]
        self.fill_color = THECOLORS["black"]

    def is_expanded(self) :
        return norm(self.head_pos - self.tail_pos) < 0.1
    
    def get_head_pos(self) :
        return self.head_pos
        
    def set_head_pos(self, pos) :
        self.head_pos = pos

    def get_tail_pos(self) :
        return self.tail_pos

    def set_tail_pos(self, pos) :
        self.tail_pos = pos
        
    def get_stroke_color(self) :
        return self.stroke_color

    def set_stroke_color(self, color) :
        self.stroke_color = color

    def get_fill_color(self) :
        return self.fill_color

    def set_fill_color(self, color) :
        self.fill_color = color

    def draw(self, screen) :
        (width, height) = screen.get_size()

        # adjust the drawing coordinates to make sure (0, 0) stays in the center
        
        p = [0, 0]
        p[0] = int(width / 2.0 + self.head_pos[0]) 
        p[1] = int(height / 2.0 - self.head_pos[1]) 

        pygame.draw.circle(screen, self.stroke_color, p, int(self.radius), 2)
        pygame.draw.circle(screen, self.fill_color, p, int(self.radius / 2.0), 4)
        
        if self.is_expanded() :
            p[0] = int(width / 2.0 + self.tail_pos[0]) 
            p[1] = int(height / 2.0 - self.tail_pos[1]) 
            pygame.draw.circle(screen, self.stroke_color, p, int(self.radius), 2)
            pygame.draw.circle(screen, self.fill_color, p, int(self.radius / 2.0), 4)
            
            
class Unit(Logger) :
    
    def __init__(self, name) :
        self.name = str(name)
        self.shape = BotShape()

    def __str__(self) :
        return "<amoebot.%s name=%s shape=%s>" % (type(self).__name__, self.name)

    def is_expanded(self) :
        return self.shape.is_expanded()
    
    def get_head_pos(self) :
        return self.shape.get_head_pos()
        
    def set_head_pos(self, pos) :
        self.shape.set_head_pos(array([pos[0], pos[1]]))

    def get_tail_pos(self) :
        return self.shape.get_tail_pos() 

    def set_tail_pos(self, pos) :
        self.shape.set_tail_pos(array([pos[0], pos[1]]))
        
    def get_stroke_color(self) :
        return self.shape.get_stroke_color()

    def set_stroke_color(self, color) :
        self.shape.set_stroke_color(color)

    def get_fill_color(self) :
        return self.shape.get_fill_color()

    def set_fill_color(self, color) :
        self.shape.set_fill_color(color)

    def expand_to(self, p_move, q_move) :
        p_move = int(p_move)
        q_move = int(q_move)
        if not self.is_expanded() and abs(p_move) <= 1.1 and abs(q_move) < 1.1 :
            if (p_move + q_move != 0) :
                pos = self.get_head_pos()
                self.set_head_pos((pos[0] + p_move, pos[1] + q_move))

    def contract_to(self, part) :
        if self.is_expanded() and part in ["head", "tail"] :
            if part == "head" :
                self.set_tail_pos(self.get_head_pos())
            else :
                self.set_head_pos(self.get_tail_pos())

    
            
            
class Context(Logger) :

    unit_attrs = {
            'name' : None,
            'shape' : None,
    }
    
    space_attrs = {
            'add' : None, 
            'step' : None,
    } 

    timer_attrs = {
            'tick' : None, 
    } 

    intention_attrs = {
        "get" : None,
        "items" : {
            "__iter__" : None,
        },
        "__getitem__" : {
            "items" : {
                "__iter__" : None,
            },
        },
    }

    step_data_attrs = {
            'get' : None, 
            'keys' : None, 
            'items' : None, 
            '__getitem__' : None, 
    } 
    
    def __init__(self, delta, space = None, timer = None, units = None) :  
        self.delta = 1.0 / 50.0
        if type(delta).__name__ == 'float' :
            self.delta = delta
        else :
            self.error('Invalid delta. Use default value: %f' % self.delta)
        
        self.space = None
        if space is not None :
            if check_attrs(space, self.space_attrs) :
                self.space = space
            else :
                self.error("Invalid 'space'.")
        else : 
            self.space = Space()
            
        self.timer = None
        if timer is not None :
            if check_attrs(timer, self.timer_attrs) :
                self.timer = timer
            else :
                self.error("Invalid 'timer'.")
        else : 
            self.timer = Timer()
       
        self.units = {}
        self.names = []
        if units is not None and hasattr(units, '__iter__') :
            for unit in units :
                if check_attrs(unit, self.unit_attrs) :
                    self.units[unit.name] = unit
                    #self.space.add(unit.shape.body, unit.shape)
                    if unit.name.isdigit() and unit.name not in self.names :
                        self.names.append(int(unit.name))
                else :
                    self.error("Invalid 'unit'.")
        self.names.sort()
        self.intention = {} 
        self.confirm = {}
    
    
    def next_name(self) :
        name = len(self.names)
        if len(self.names) > 0 and self.names[-1] > len(self.names) - 1 :
            for i in range(len(self.names)) :
                if i < self.names[i] :
                    name = i
                    break
        self.names.insert(name, name)
        return str(name) 


    def bind_objects(self, objects) :
        if objects is not None and hasattr(objects, '__iter__') :
            for obj in objects :
                if hasattr(obj, 'name') and type(obj.name).__name__ == 'str' :
                    if obj.name not in self.units.keys() :
                        self.error("No shape has name: %s" % obj.name)
                else :
                    self.error("Invalid 'object'.")


    def judge(self, intention) :
        self.intention = {}
        if check_attrs(intention, self.intention_attrs) :
            self.intention = intention

        # collect and apply the physics information
        
        for (obj_name, obj_intention) in self.intention.items() :
            if obj_name in self.units.keys() :
                #vel = self.get_from_intention(obj_name = obj_name, symbol = "set_vel")
                #if vel is not None and type(vel).__name__ == "tuple" and len(vel) == 2 :
                    #self.units[obj_name].set_velocity(vel)
                stroke = self.get_from_intention(obj_name = obj_name, symbol = "stroke")
                if stroke is not None :
                    self.units[obj_name].set_stroke_color(stroke)
                fill = self.get_from_intention(obj_name = obj_name, symbol = "fill")
                if fill is not None :
                    self.units[obj_name].set_fill_color(fill)

        # physics engine step 
        
        self.space.step(self.delta)
        self.timer.tick(self.delta)
        
        # response to the sensors 

        self.confirm = {}
        listen_rcvs = []
        radar_rcvs = [] 
        obstacle_rcvs = [] 
        
        for (obj_name, obj_intention) in self.intention.items() :
            obstacle_query = self.get_from_intention(obj_name = obj_name, symbol = "obstacle")
            if obstacle_query is not None :
                obstacle_rcvs.append(obj_name)
            radar_query = self.get_from_intention(obj_name = obj_name, symbol = "radar")
            if radar_query is not None :
                radar_rcvs.append(obj_name)
            listen_query = self.get_from_intention(obj_name = obj_name, symbol = "listen")
            if listen_query is not None :
                listen_rcvs.append(obj_name) 
                
            time_query = self.get_from_intention(obj_name = obj_name, symbol = "time")
            mass_query = self.get_from_intention(obj_name = obj_name, symbol = "mass")
            radius_query = self.get_from_intention(obj_name = obj_name, symbol = "radius")
            pos_query = self.get_from_intention(obj_name = obj_name, symbol = "pos")
            angle_query = self.get_from_intention(obj_name = obj_name, symbol = "angle")
            vel_query = self.get_from_intention(obj_name = obj_name, symbol = "vel")
            avel_query = self.get_from_intention(obj_name = obj_name, symbol = "avel")

            if time_query is not None :
                self.feed_confirm(obj_name = obj_name, results = {"time" : self.timer.value})
            results = {}
            if mass_query is not None : 
                results["mass"] = self.units[obj_name].get_mass()
            if radius_query is not None : 
                results["radius"] = self.units[obj_name].get_radius()
            if pos_query is not None : 
                pos = self.units[obj_name].get_position()
                results["pos"] = (pos[0], pos[1]) 
            if angle_query is not None : 
                results["angle"] = self.units[obj_name].get_angle() 
            if vel_query is not None : 
                vel = self.units[obj_name].get_velocity()
                results["vel"] = (vel[0], vel[1]) 
            if avel_query is not None : 
                results["avel"] = self.units[obj_name].get_angular_velocity() 
            self.feed_confirm(obj_name = obj_name, results = results, check_unit = True)
        
        if len(listen_rcvs) > 0 :
            transmits = [] 
            for (obj_name, obj_intention) in self.intention.items() :
                transmit = self.get_from_intention(obj_name = obj_name, symbol = "transmit")
                if transmit is not None :
                    transmits.append(transmit) 
            for obj_name in listen_rcvs :
                self.feed_confirm(obj_name = obj_name, results = {"listen" : transmits})

        if len(radar_rcvs) > 0 : 
            detects = [] 
            for (obj_name, obj_intention) in self.intention.items() :
                unit = self.units.get(obj_name, None)
                if unit is not None : 
                    detects.append((obj_name, unit.get_position(), unit.get_velocity(), unit.get_radius(), unit.get_angle()))
            for obj_name in radar_rcvs :
                self.feed_confirm(obj_name = obj_name, results = {"radar" : detects})
        
        if len(obstacle_rcvs) > 0 : 
            obstacles = []
            for (name, unit) in self.units.items() :
                if isinstance(unit.shape, SegmentShape) :
                    ends = unit.shape.get_ends()
                    obstacles.append((name, ends[0], ends[1], unit.get_velocity()))
            for obj_name in obstacle_rcvs :
                self.feed_confirm(obj_name = obj_name, results = {"obstacle" : obstacles})
                
        return self.confirm

    def get_from_intention(self, obj_name, symbol) :
        value = None
        if self.intention is not None and self.intention.get(obj_name, None) is not None :
            value = self.intention[obj_name].get(symbol, None)
        return value

    def feed_confirm(self, obj_name, results, check_unit = False) :
        if type(obj_name).__name__ == "str" and (not check_unit or self.units.get(obj_name, None) is not None) and type(results).__name__ == "dict" :
            for (symbol, value) in results.items() :
                if self.confirm.get(obj_name, None) is None :
                    self.confirm[obj_name] = {}
                self.confirm[obj_name][symbol + "_result"] = value
                
    def snap(self, step_data) :
        if step_data is not None and check_attrs(step_data, self.step_data_attrs) :
            for (name, unit) in self.units.items() :
                if step_data.get(name, None) is None :
                    step_data[name] = {}
                head_pos = unit.get_head_pos()
                step_data[name]["head_pos"] = "%f %f" % (head_pos[0], head_pos[1])
                tail_pos = unit.get_tail_pos()
                step_data[name]["tail_pos"] = "%f %f" % (tail_pos[0], tail_pos[1])
                stroke = unit.get_stroke_color()  
                step_data[name]["stroke"] = "%f %f %f" % (stroke[0], stroke[1], stroke[2])
                fill = unit.get_fill_color()  
                step_data[name]["fill"] = "%f %f %f" % (fill[0], fill[1], fill[2])

            step_data["_global_"] = {}
            step_data["_global_"]["timer"] = self.timer.value

    def mimic(self, step_data) :
        if step_data is not None and check_attrs(step_data, self.step_data_attrs):
            for (name, unit_data) in step_data.items() :
                if name == "_global_" :
                    timer_value = unit_data.get('timer', None)
                    if timer_value is not None :
                        self.timer.value = float(timer_value)
                else :
                    if name not in self.units.keys() :
                        self.units[name] = Unit(name = name)

                    head_pos = unit_data.get("head_pos", None)
                    if head_pos is not None :
                        self.units[name].set_head_pos((float(head_pos.split(' ')[0]), float(head_pos.split(' ')[1])))

                    tail_pos = unit_data.get("tail_pos", None)
                    if tail_pos is not None :
                        self.units[name].set_tail_pos((float(tail_pos.split(' ')[0]), float(tail_pos.split(' ')[1])))

                    stroke = unit_data.get("stroke", None)
                    if stroke is not None :
                        self.units[name].set_stroke_color((float(stroke.split(' ')[0]), float(stroke.split(' ')[1]), float(stroke.split(' ')[2])))
                        
                    fill = unit_data.get("fill", None)
                    if fill is not None :
                        self.units[name].set_fill_color((float(fill.split(' ')[0]), float(fill.split(' ')[1]), float(fill.split(' ')[2])))


    def draw(self, screen) :
        (width, height) = screen.get_size()
        
        # draw the grids

        grid_line_color = THECOLORS["lightgray"]

        unit = 2 * amoebot_paras["radius"] *  math.cos(math.pi / 6.0)

        start = [0, height / 2]
        end = [width, height / 2]
        pygame.draw.line(screen, THECOLORS["gray"], start, end, 1)


        q_ceil = int(math.ceil((height / unit) / 2))
        for i in range(1, q_ceil) :
            start = [0, height / 2 + unit * i]
            end = [width, height / 2 + unit * i]
            pygame.draw.line(screen, THECOLORS["gray"], start, end, 1)
            start = [0, height / 2 - unit * i]
            end = [width, height / 2 - unit * i]
            pygame.draw.line(screen, THECOLORS["gray"], start, end, 1)
            

        distance = distance_to_line((-width / 2.0, height / 2.0), (0, 0), pq_to_xy((0, 1))) 
        start = pq_to_xy((0, q_ceil))
        start[0] = int(width / 2.0 + start[0]) 
        start[1] = int(height / 2.0 - start[1]) 
        end = pq_to_xy((0, -q_ceil))
        end[0] = int(width / 2.0 + end[0]) 
        end[1] = int(height / 2.0 - end[1]) 
        pygame.draw.line(screen, grid_line_color, start, end, 1)
        start = wq_to_xy((0, q_ceil))
        start[0] = int(width / 2.0 + start[0]) 
        start[1] = int(height / 2.0 - start[1]) 
        end = wq_to_xy((0, -q_ceil))
        end[0] = int(width / 2.0 + end[0]) 
        end[1] = int(height / 2.0 - end[1]) 
        pygame.draw.line(screen, grid_line_color, start, end, 1)
        
        for i in range(1, int(1.5 * math.ceil(distance / unit))) :
            start = pq_to_xy((i, q_ceil))
            start[0] = int(width / 2.0 + start[0]) 
            start[1] = int(height / 2.0 - start[1]) 
            end = pq_to_xy((i, -q_ceil))
            end[0] = int(width / 2.0 + end[0]) 
            end[1] = int(height / 2.0 - end[1]) 
            pygame.draw.line(screen, grid_line_color, start, end, 1)
            start = pq_to_xy((-i, q_ceil))
            start[0] = int(width / 2.0 + start[0]) 
            start[1] = int(height / 2.0 - start[1]) 
            end = pq_to_xy((-i, -q_ceil))
            end[0] = int(width / 2.0 + end[0]) 
            end[1] = int(height / 2.0 - end[1]) 
            pygame.draw.line(screen, grid_line_color, start, end, 1)
            start = wq_to_xy((i, q_ceil))
            start[0] = int(width / 2.0 + start[0]) 
            start[1] = int(height / 2.0 - start[1]) 
            end = wq_to_xy((i, -q_ceil))
            end[0] = int(width / 2.0 + end[0]) 
            end[1] = int(height / 2.0 - end[1]) 
            pygame.draw.line(screen, grid_line_color, start, end, 1)
            start = wq_to_xy((-i, q_ceil))
            start[0] = int(width / 2.0 + start[0]) 
            start[1] = int(height / 2.0 - start[1]) 
            end = wq_to_xy((-i, -q_ceil))
            end[0] = int(width / 2.0 + end[0]) 
            end[1] = int(height / 2.0 - end[1]) 
            pygame.draw.line(screen, grid_line_color, start, end, 1)
        
        for unit in self.units.values() :
            if unit.shape is not None :
                unit.shape.draw(screen)
                
class Aggregator(Logger) :

    object_status_focus = [
            "time", "force", "spin", "transmit", "listen", 
            "mass", "radius", "pos", "angle", "vel", "avel",
            "fill", "stroke", "pointer",
            "radar", "obstacle",
            "set_angle", "set_vel", "set_avel", 
    ]

    data_attrs = {}
    
    def pre(self, objects, confirm = None) :
        if confirm is not None and len(confirm) > 0 :
            for obj in objects :
                obj_confirm = confirm.get(obj.name, None)
                if obj_confirm is not None :
                    for key in obj_confirm.keys() :
                        obj.status['pre'][key] = obj_confirm[key]


    def post(self, objects) :
        intention = {} 
        for obj in objects :
            obj_intention = {}
            for key in self.object_status_focus :
                focus_content = obj.status['post'].get(key, None)
                if focus_content is not None :
                    obj_intention[key] = focus_content 
            if len(obj_intention) > 0 :
                if intention.get(obj.name, None) is None :
                    intention[obj.name] = obj_intention
                else :
                    self.error("Found duplicate object: [%s]" % obj.name)
        return intention




if __name__ == '__main__' :
    print("")
    print("Amoebot Simulator v1.0")
    print("")
    print("(c) 2017-2018, NiL, csningli@gmail.com.")
    print("")
    #print("Interactive Mode.")
    print("")
