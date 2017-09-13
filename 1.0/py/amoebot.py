import sys, os, time, datetime, json, math, inspect
import pygame
from pygame.locals import * 
from pygame.color import *

from numpy import array, dot 
from numpy.linalg import norm

from utils import distance_to_line

from multiagent import Timer, Space, Context, Object, Logger, check_attrs

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


class AmoebotObject(Object) :
    pass

class BotShape(Logger) :
    def __init__(self) :
        self.radius = float(amoebot_paras["radius"])
        self.body = None
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
            
            
class AmoebotUnit(Logger) :
    
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

    
class Space(Logger) :
    def add(self, body, shape) :
        pass
    def step(self, delta) :
        pass
            
class AmoebotContext(Context) :
    def __init__(self, delta, timer = None, units = None) :
        super(AmoebotContext, self).__init__(delta = delta, space = Space(), timer = timer, units = units)
        
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
