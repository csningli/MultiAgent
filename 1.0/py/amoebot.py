import sys, os, time, datetime, json, math, inspect
import pygame
from pygame.locals import * 
from pygame.color import *

from numpy import array, dot 
from numpy.linalg import norm

from utils import distance_to_line

from multiagent import Timer, Space, Aggregator, Context, Object, Module, ProcessModule, SensorModule, Logger, check_attrs

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
    x = -2 * amoebot_paras["radius"] * p -2 * amoebot_paras["radius"] *  math.cos(math.pi / 3.0) * q 
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
        self.head_color = THECOLORS["red"]
        self.tail_color = THECOLORS["blue"]

    def is_expanded(self) :
        return not norm(self.head_pos - self.tail_pos) < 0.1
    
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

    def draw(self, screen) :
        (width, height) = screen.get_size()

        head_adjusted = [0, 0]
        head_xy = pq_to_xy(self.head_pos)
        head_adjusted[0] = int(round(width / 2.0 + head_xy[0]))
        head_adjusted[1] = int(round(height / 2.0 - head_xy[1]))
        
        if not self.is_expanded() :
            pygame.draw.circle(screen, self.stroke_color, head_adjusted, int(self.radius), 2)
            pygame.draw.circle(screen, self.head_color, head_adjusted, int(self.radius / 2.0), 4)
        else : 
            tail_adjusted = [0, 0]
            tail_xy = pq_to_xy(self.tail_pos)
            tail_adjusted[0] = int(round(width / 2.0 + tail_xy[0]))
            tail_adjusted[1] = int(round(height / 2.0 - tail_xy[1]))

            diff = array(head_xy) - array(tail_xy)
            angle = math.acos(diff[0] / norm(array(diff)))
            pygame.draw.circle(screen, self.stroke_color, head_adjusted, int(self.radius), 2)
            pygame.draw.circle(screen, self.stroke_color, tail_adjusted, int(self.radius), 2)
            pygame.draw.circle(screen, self.head_color, head_adjusted, int(self.radius / 2.0), 4)
            pygame.draw.circle(screen, self.tail_color, tail_adjusted, int(self.radius / 2.0), 4)
            pygame.draw.line(screen, self.stroke_color, head_adjusted, tail_adjusted, 4)
            
            #pygame.draw.arc(screen, self.stroke_color, 
                #pygame.Rect(head_adjusted[0] - int(self.radius), head_adjusted[1] - int(self.radius),
                #int(self.radius * 2), int(self.radius * 2)), angle - math.pi / 2.0, angle + math.pi / 2.0, 2)
            #pygame.draw.arc(screen, self.stroke_color, 
                #pygame.Rect(tail_adjusted[0] - int(self.radius), tail_adjusted[1] - int(self.radius),
                #int(self.radius * 2), int(self.radius * 2)), angle + math.pi / 2.0, angle - math.pi / 2.0, 2)
            #start = [0, 0]
            #end = [0, 0]
            #start[0] = int(round(head_adjusted[0] + self.radius * math.cos(angle - math.pi / 2.0)))
            #start[1] = int(round(head_adjusted[1] + self.radius * math.sin(angle - math.pi / 2.0)))
            #end[0] = int(round(tail_adjusted[0] + self.radius * math.cos(angle - math.pi / 2.0)))
            #end[1] = int(round(tail_adjusted[1] + self.radius * math.sin(angle - math.pi / 2.0)))
            #pygame.draw.line(screen, self.stroke_color, start, end, 2)
            #start[0] = int(round(head_adjusted[0] + self.radius * math.cos(angle + math.pi / 2.0)))
            #start[1] = int(round(head_adjusted[1] + self.radius * math.sin(angle + math.pi / 2.0)))
            #end[0] = int(round(tail_adjusted[0] + self.radius * math.cos(angle + math.pi / 2.0)))
            #end[1] = int(round(tail_adjusted[1] + self.radius * math.sin(angle + math.pi / 2.0)))
            #pygame.draw.line(screen, self.stroke_color, start, end, 2)
            #pygame.draw.line(screen, self.stroke_color, head_adjusted, tail_adjusted, 2)
            
            
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

    def expand_to(self, move) :
        p_move = int(move[0])
        q_move = int(move[1])
        if not self.is_expanded() and abs(p_move) <= 1.1 and abs(q_move) < 1.1 :
            if (not (p_move == 0 and q_move == 0) or abs(p_move + q_move) < 1.5) :
                pos = self.get_head_pos()
                self.set_head_pos((pos[0] + p_move, pos[1] + q_move))

    def contract_to(self, part) :
        if self.is_expanded() and part in ["head", "tail"] :
            if part == "head" :
                self.set_tail_pos(self.get_head_pos())
            else :
                self.set_head_pos(self.get_tail_pos())

    
class AmoebotSpace(Logger) :
    limit = 100
    def __init__(self, units, rg = None) :
        if rg is None :
            rg = [2 * self.limit, 2 * self.limit]
        self.cord = array([None for i in range(rg[0] * rg[1])])
        self.cord = self.cord.reshape(rg)
        self.units = {} 
        for unit in units :
            self.units[unit.name] = unit
        self.step(delta = 0)
        
    def add(self, body, shape) :
        pass
        
    def step(self, delta) :
        for unit in self.units.values() :
            head_pos = unit.get_head_pos()
            p_index = int(head_pos[0] + self.limit)
            q_index = int(head_pos[1] + self.limit)
            if q_index >= 0 and q_index >= 0 :
                self.cord[p_index, q_index] = unit
            tail_pos = unit.get_tail_pos()
            p_index = int(tail_pos[0] + self.limit)
            q_index = int(tail_pos[1] + self.limit)
            if q_index >= 0 and q_index >= 0 :
                self.cord[p_index, q_index] = unit

    def query(self, pos) :
        result = None
        p_index = int(pos[0] + self.limit)
        q_index = int(pos[1] + self.limit)
        if q_index >= 0 and q_index >= 0 :
            unit = self.cord[p_index, q_index]
            if unit is not None :
                if int(unit.get_head_pos()[0]) == int(pos[0]) and int(unit.get_head_pos()[1]) == int(pos[1]) :
                    result = (unit, "head") 
                if int(unit.get_tail_pos()[0]) == int(pos[0]) and int(unit.get_tail_pos()[1]) == int(pos[1]) :
                    result = (unit, "tail") 
                else :
                    self.cord[p_index, q_index] = None
        return result
            
class AmoebotContext(Context) :
    def __init__(self, delta, timer = None, units = None) :
        super(AmoebotContext, self).__init__(delta = delta, space = AmoebotSpace(units = units), timer = timer, units = units)
    
    def judge(self, intention) :
        self.intention = {}
        if check_attrs(intention, self.intention_attrs) :
            self.intention = intention

        # collect and apply the physics information
        
        for (obj_name, obj_intention) in self.intention.items() :
            if obj_name in self.units.keys() :
                contract = self.get_from_intention(obj_name = obj_name, symbol = "contract")
                if contract is not None and type(contract).__name__ == "str":
                    self.units[obj_name].contract_to(contract)
                expand = self.get_from_intention(obj_name = obj_name, symbol = "expand")
                if expand is not None and type(expand).__name__ == "tuple" and len(expand) == 2 :
                    pos = self.units[obj_name].get_head_pos()
                    coll = self.space.query((pos[0] + expand[0], pos[1] + expand[1]))
                    if coll is None :
                        self.units[obj_name].expand_to(expand)
                    else :
                        if coll[0].is_expanded() :
                            coll[0].contract_to(coll[1])
                            self.units[obj_name].expand_to(expand)
                        
                stroke = self.get_from_intention(obj_name = obj_name, symbol = "stroke")
                if stroke is not None :
                    self.units[obj_name].set_stroke_color(stroke)

        self.space.step(self.delta)
        self.timer.tick(self.delta)
        
        # response to the sensors 

        self.confirm = {}
        
        for (obj_name, obj_intention) in self.intention.items() :
            
            time_query = self.get_from_intention(obj_name = obj_name, symbol = "time")
            head_pos_query = self.get_from_intention(obj_name = obj_name, symbol = "head_pos")
            tail_pos_query = self.get_from_intention(obj_name = obj_name, symbol = "tail_pos")
            neighbor_query = self.get_from_intention(obj_name = obj_name, symbol = "neighbor")

            if time_query is not None :
                self.feed_confirm(obj_name = obj_name, results = {"time" : self.timer.value})
            results = {}
            head_pos = self.units[obj_name].get_head_pos()
            tail_pos = self.units[obj_name].get_tail_pos()
            if head_pos_query is not None : 
                results["head_pos"] = (head_pos[0], head_pos[1]) 
            if tail_pos_query is not None : 
                results["tail_pos"] = (tail_pos[0], tail_pos[1]) 
            if neighbor_query is not None :
                results["neighbor"] = [] 
                for shift in [(1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0)] : 
                    neighbor = self.space.query((head_pos[0] + shift[0], head_pos[1] + shift[1]))
                    if neighbor is not None and neighbor[0].name != obj_name :
                        results["neighbor"].append((neighbor, shift, "head")) 
                    if self.units[obj_name].is_expanded() :
                        neighbor = self.space.query((tail_pos[0] + shift[0], tail_pos[1] + shift[1]))
                        if neighbor is not None and neighbor[0].name != obj_name :
                            results["neighbor"].append((neighbor, shift, "tail")) 
            self.feed_confirm(obj_name = obj_name, results = results, check_unit = True)
        
        transmits = {}
        for (obj_name, obj_intention) in self.intention.items() :
            transmit = self.get_from_intention(obj_name = obj_name, symbol = "share")
            # print(obj_name, obj_intention, transmit)
            if transmit is not None and transmit[0] != None :
                if transmits.get(transmit[0].name, None) is None : 
                    transmits[transmit[0].name] = []
                transmits[transmit[0].name].append((transmit[1], self.units[obj_name])) 
        # print("trans:", transmits)
        for obj_name in transmits.keys() :
            self.feed_confirm(obj_name = obj_name, results = {"shared" : transmits[obj_name]})
        # print("confirm:", self.confirm)

        return self.confirm
        
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
                
                
class AmoebotAggregator(Aggregator) :

    object_status_focus = [
            "time", "neighbor", "share", "shared", "head_pos", "tail_pos", 
            "stroke", "expand", "contract",
    ]

class ExpandModule(Module) :        
    symbol = "expand"
        
    def perform(self, msg, ram) :
        super(ExpandModule, self).perform(msg = msg, ram = ram)
        sensor_symbols = []
        if self.buffs is not None and len(self.buffs) > 0 :
            self.output(value = self.buffs[0]) 
            
        self.activate_sensors(symbols = sensor_symbols)
        
        return self.result

class ContractModule(Module) :  
    symbol = "contract"
        
    def perform(self, msg, ram) :
        super(ContractModule, self).perform(msg = msg, ram = ram)
        sensor_symbols = []
        if self.buffs is not None and len(self.buffs) > 0 :
            self.output(value = self.buffs[0]) 
            
        self.activate_sensors(symbols = sensor_symbols)
        
        return self.result
        
class ShareModule(Module) :
    symbol = "share"
        
    def perform(self, msg, ram) :
        super(ShareModule, self).perform(msg = msg, ram = ram)

        if self.buffs is not None and len(self.buffs) > 0 :
            self.output(value = self.buffs[0]) 
            
        return self.result


class NeighborModule(SensorModule) :   # simulate the listen interface 
    symbol = "neighbor"

if __name__ == '__main__' :
    print("")
    print("Amoebot Simulator v1.0")
    print("")
    print("(c) 2017-2018, NiL, csningli@gmail.com.")
    print("")
    #print("Interactive Mode.")
    print("")
