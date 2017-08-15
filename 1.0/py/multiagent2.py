
import sys, os, time, datetime, json, math, inspect
import pygame
from pygame.locals import * 
from pygame.color import *

import pymunkoptions
pymunkoptions.options["debug"] = False
from pymunk import Circle, Segment, Body, Space, Vec2d

def append_to_sys_path(path = None) :
    if path is None :
        unit_tests_path = os.path.dirname(os.path.abspath(__file__))
        path = '/'.join(unit_tests_path.split('/')[:-1]) + '/py'
    sys.path.append(path)

def test_func(func) :
    def func_wrapper(*argv) :
        print('| Run test: %s' % func.__name__)
        start = time.time()
        func(*argv)
        for label in ['INFO', 'ERROR'] :
            Logger().print_logs(label = label)
        end = time.time()
        print('| Done. Time cost: %s (s)' % (end - start))
        print('-' * 60)
    return func_wrapper

def check_attrs(obj, attrs) :
    is_valid = True
    if attrs is not None and hasattr(attrs, '__iter__') and hasattr(attrs, '__getitem__'):
        for attr in attrs :
            if not hasattr(obj, attr) :
                is_valid = False
                break
            elif attrs[attr] is not None and type(getattr(obj, attr)).__name__ not in ['method', 'builtin_function_or_method'] :
                is_valid = check_attrs(getattr(obj, attr), attrs[attr])
                if is_valid == False :
                    break
    else :
        is_valid = False
    return is_valid                   


class Logger(object) :

    logs = {} 
    
    def log(self, line, label = None, show = False) :
        result = None 
        if label is None or type(label).__name__ != 'str' :
            label = "LOG"
        if label not in self.logs.keys() :
            self.logs[label] = []
        log_list = self.logs[label]
        
        line = "[%s\t%s]\t%s" % (label, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), line)
        if hasattr(log_list, "append") :
            log_list.append(line)
            result = line
        if show :
            print(line)
        return result

    def get_logs(self, label = None, begin = None, end = None) : 
        result = []
        if label is None or type(label).__name__ != 'str' :
            label = "LOG"
        log_list = self.logs.get(label, None)
        if log_list is not None :
            if end is None or end > len(log_list):
                end = len(log_list)
            if begin is None or begin < 0:
                begin = 0
            result = log_list[begin:end]
        return result

    def print_logs(self, label, begin = None, end = None) :
        result = False
        if label is None :
            label = "LOGS"
        print(label + ":")
        for line in self.get_logs(label = label, begin = begin, end = end) :
            print(line)
        result = True
        return result

    def save_logs(self, label = None, begin = None, end = None, filename = None) :
        if label is None :
            label = "LOGS"
        if filename is None :
            filename = "multiagent_%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S_%f")
        with open(filename + ".%s" % label, 'w') as f :
            for line in self.get_logs(label = label, begin = begin, end = end) :
                f.write(line + "\n")
                    
    def info(self, line, show = False) :
        self.log(line = line, label = "INFO", show = show)

    def error(self, line, show = False) :
        self.log(line = line, label = "ERROR", show = show)


#
# Objects
#


class Object(Logger) :

    mod_attrs = {'perform' : None} 

    obj_data_attrs = {
            '__getitem__' : None,
    } 
    
    def __init__(self, name, mods) :
        self.name = str(name)
        self.status = {'post' : {}, 'pre' : {}, 'local' : {}, 'mem' : {}}
        self.mods = []
        if hasattr(mods, '__iter__') :
            for mod in mods: 
                if mod is not None and check_attrs(mod, self.mod_attrs) :
                    self.mods.append(mod)
                else :
                    self.error("Found invalid module.")

    def __str__(self) :
        return '<multiagent.%s name=%s>' % (self.__class__.__name__, self.name)
        
    def step(self) :
        self.info("%s steps." % self)
        
        #self.info("%s '%s' pre-status: %s" % (obj.__class__.__name__, obj.name, obj.status['pre']))
        
        for key in self.status['local'].keys() :
            self.status['pre'][key] = self.status['local'][key]
        self.status['local'] = {}
        
        for mod in self.mods : 
            result = mod.perform(msg = self.status['pre'], ram = self.status['mem'])
            for domain in ["local"] : 
                domain_buffs = result.get(domain, None) 
                if domain_buffs is not None :
                    for symbol_buff in domain_buffs.keys() :
                        if self.status[domain].get(symbol_buff, None) is None :
                            self.status[domain][symbol_buff] = []
                        self.status[domain][symbol_buff].append(domain_buffs[symbol_buff])
            for domain in ["post"] : 
                domain_request = result.get(domain, None) 
                if domain_request is not None :
                    for symbol in domain_request.keys() :
                        self.status[domain][symbol] = domain_request[symbol]

    def snap(self, obj_data = None) :
        if obj_data is not None :
            for domain in ["pre", "post", "local", "mem"] : 
                obj_data[domain] = {}
                for (key, value) in self.status[domain].items() :
                    obj_data[domain][key] = value 

        
    def mimic(self, obj_data) :
        if obj_data is not None :
            for domain in ["pre", "post", "local", "mem"] : 
                if obj_data.get(domain, None) is not None :
                    for (key, value) in obj_data[domain].items() :
                        self.status[domain][key] = value

    def put_to_mem(self, symbol, value) :
        if type(symbol).__name__ == "str" : 
            self.status["mem"][symbol + "_value"] = value 
        return self.status["mem"] 
        
class BasicShape(Logger) :
    stroke_color = THECOLORS["blue"]
    fill_color = THECOLORS["blue"]
    pointer_color = THECOLORS["red"]
    
    def set_stroke_color(self, color) :
        self.stroke_color = color 

    def get_stroke_color(self) :
        return self.stroke_color

    def set_fill_color(self, color) :
        self.fill_color = color 

    def get_fill_color(self) :
        return self.fill_color

    def set_pointer_color(self, color) :
        self.pointer_color = color 

    def get_pointer_color(self) :
        return self.pointer_color
     
    def draw(self, screen) :
        pass

    def get_range(self) :
        return (1.0, 1.0)

    def get_position(self) :
        return (0.0, 0.0)
        
    def set_position(self, position) :
        pass

    def get_mass(self) :
        return 0
        
    def get_angle(self) :
        return 0
        
    def set_angle(self, angle) :
        pass

    def get_velocity(self) :
        return (0.0, 0.0) 

    def get_angular_velocity(self) :
        return 0.0 

    def apply_force(self, force) :
        pass

    def apply_spin(self, spin) :
        pass
        
class SegmentShape(BasicShape, Segment) : 
    def __init__(self, a, b) :
        super(SegmentShape, self).__init__(Body(body_type=Body.STATIC), a, b, 0.0)
        self.friction = 1.0
        self.collision_type = 0  

    def draw(self, screen) :
        (width, height) = screen.get_size()
        (pv1, pv2) = self.get_ends()
        pv1[0] = int(width / 2.0 + pv1[0]) 
        pv1[1] = int(height / 2.0 - pv1[1]) 
        pv2[0] = int(width / 2.0 + pv2[0]) 
        pv2[1] = int(height / 2.0 - pv2[1])
        pygame.draw.lines(screen, self.stroke_color, False, [pv1, pv2])
    
    def get_position(self) :
        return self.body.position 

    def get_ends(self) :
        body = self.body
        pv1 = body.position + self.a.cpvrotate(body.rotation_vector)
        pv2 = body.position + self.b.cpvrotate(body.rotation_vector)
        return (tuple(pv1), tuple(pv2)) 

class CircleShape(BasicShape, Circle) : 
    def draw(self, screen) :
        r = self.radius
        p = self.body.position
        rot = self.body.rotation_vector
        (width, height) = screen.get_size()

        # adjust the drawing coordinates to make sure (0, 0) stays in the center
        
        p[0] = int(width / 2.0 + p[0]) 
        p[1] = int(height / 2.0 - p[1]) 

        head = Vec2d(rot.x, -rot.y) * r * 0.9
        pygame.draw.circle(screen, self.stroke_color, p, int(r), 2)
        pygame.draw.circle(screen, self.fill_color, p, int(r/2.0), 4)
        pygame.draw.line(screen, self.pointer_color, p, p + head)

    def get_mass(self) :
        return self.body.mass
        
    def get_position(self) :
        return self.body.position 
        
    def set_position(self, position) :
        result = False
        if hasattr(position, '__getitem__') and hasattr(position, '__len__') and len(position) == 2 : 
            self.body.position = position
            result = True
        return result 

    def get_angle(self) :
        return self.body.angle

    def set_angle(self, angle) :
        result = False
        self.body.angle = angle
        result = True
        return result 
        
    def get_range(self) :
        return (self.radius, self.radius) 
        
    def get_velocity(self) :
        velocity = self.body.velocity
        return (velocity.x, velocity.y) 
        
    def set_velocity(self, vel) :
        self.body.velocity = vel

    def get_angular_velocity(self) :
        return self.body.angular_velocity

    def set_angular_velocity(self, avel) :
        self.body.angular_velocity = avel 

    def apply_force(self, force) :
        self.body.force = force

# Unit (- Context (- Simulator

class Unit(Logger) :
    
    object_attrs = {
            'name' : None, 
    }

    shape_attrs = {
            'body' : None,
    }

    def __init__(self, name, shape = None) :
        self.name = str(name)
        self.shape = None
        if shape is not None : 
            if check_attrs(shape, self.shape_attrs) :
                self.shape = shape 
            else :
                self.error("Invalid 'shape'.")
        else :
            self.shape = CircleShape(Body(1.0, 10.0), 10.0, (0.0, 0.0))
        self.shape.collision_type = 2 # collision type: ball
        self.shape.friction = 0.5

    def __str__(self) :
        return "<multiagent.%s name=%s shape=%s>" % (type(self).__name__, self.name, self.shape)
        
    def get_position(self) :
        return self.shape.get_position()
        
    def set_position(self, position) :
        self.shape.set_position(position)

    def get_mass(self) :
        return self.shape.get_mass()
        
    def get_angle(self) :
        return self.shape.get_angle()
        
    def set_angle(self, angle) :
        self.shape.set_angle(angle)

    def get_velocity(self) :
        return self.shape.get_velocity() 
        
    def set_velocity(self, vel) :
        return self.shape.set_velocity(vel) 

    def get_angular_velocity(self) :
        return self.shape.get_angular_velocity()

    def apply_force(self, force) :
        self.shape.apply_force(force)

    def set_angular_velocity(self, avel) :
        self.shape.set_angular_velocity(avel)
        
    def get_stroke_color(self) :
        return self.shape.get_stroke_color()

    def set_stroke_color(self, color) :
        self.shape.set_stroke_color(color)

    def get_fill_color(self) :
        return self.shape.get_fill_color()

    def set_fill_color(self, color) :
        self.shape.set_fill_color(color)

    def get_pointer_color(self) :
        return self.shape.get_pointer_color()
        
    def set_pointer_color(self, color) :
        self.shape.set_pointer_color(color)
        
#
# Oracle
#

class Oracle(Logger) :
    
    def __init__(self) :
        pass


class NetworkOracle(Oracle) :

    def __init__(self, name) :
        super(NetworkSpace, self).__init__()
        self.name = name
        self.agents = [] 
        self.relations = []

    def __str__(self) :
        return '[Network name = %s, agents = %s, relations = %s]' % (self.name, self.agents, self.relations)

    def add_agent(self, agent) :
        attr = self.name + '_name'
        a = getattr(agent,  attr, None) 
        if a is None :
            r = setattr(agent, attr, len(self.agents))
        self.agents.append(agent)
        self.relations.append([])
        return self.agents[-1]

    def update_agent(self, index, new_agent) :
        if index < 0 or index > len(self.agents) - 1 :
            return None
        self.agents[index] = new_agent
        return self.agents[index]
        
    def index_of_agent(self, agent) :
        if type(agent).__name__ != 'int' :
            if agent not in self.agents :
                return -1
            else :
                return self.agents.index(from_index)
        return agent
        
    def add_relation(self, relation) :
        from_index = self.index_of_agent(relation[0])
        if from_index < 0 or from_index > len(self.agents) - 1 :
            return None
            
        to_index = self.index_of_agent(relation[1])
        if to_index < 0 or to_index > len(self.agents) - 1 :
            return None
        
        if to_index not in self.relations[from_index] :
            self.relations[from_index].append(to_index)
            self.relations[from_index].sort()

        return (from_index, to_index)

    def delete_relation(self, relation) :
        from_index = self.index_of_agent(relation[0])
        if from_index < 0 or from_index > len(self.agents) - 1 :
            return None
            
        to_index = self.index_of_agent(relation[1])
        if to_index < 0 or to_index > len(self.agents) - 1 :
            return None
        
        if to_index in self.relations[from_index] :
            self.relations[from_index].remove(to_index)
            
        return (from_index, to_index)


class Timer(Logger) :
    def __init__(self) :
        self.value = 0.0

    def tick(self, delta) :
        if (type(delta).__name__ == 'float') :
            self.value += delta
        else :
            self.error("Invalid 'delta' for Timer.tick().")
    
        
class Context(Logger) :

    unit_attrs = {
            'name' : None,
            'shape' : {
                    'body' : None,  
            },
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
                    self.space.add(unit.shape.body, unit.shape)
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
                vel = self.get_from_intention(obj_name = obj_name, symbol = "set_vel")
                if vel is not None and type(vel).__name__ == "tuple" and len(vel) == 2 :
                    self.units[obj_name].set_velocity(vel)
                angle = self.get_from_intention(obj_name = obj_name, symbol = "set_angle")
                if angle is not None and type(angle).__name__ == "float" :
                    self.units[obj_name].set_angle(angle)
                force = self.get_from_intention(obj_name = obj_name, symbol = "force")
                if force is not None :
                    self.units[obj_name].apply_force(force)
                avel = self.get_from_intention(obj_name = obj_name, symbol = "set_avel")
                if avel is not None :
                    self.units[obj_name].set_angular_velocity(avel)
                stroke = self.get_from_intention(obj_name = obj_name, symbol = "stroke")
                if stroke is not None :
                    self.units[obj_name].set_stroke_color(stroke)
                fill = self.get_from_intention(obj_name = obj_name, symbol = "fill")
                if fill is not None :
                    self.units[obj_name].set_fill_color(fill)
                pointer = self.get_from_intention(obj_name = obj_name, symbol = "pointer")
                if pointer is not None :
                    self.units[obj_name].set_pointer_color(pointer)

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
            pos_query = self.get_from_intention(obj_name = obj_name, symbol = "pos")
            angle_query = self.get_from_intention(obj_name = obj_name, symbol = "angle")
            vel_query = self.get_from_intention(obj_name = obj_name, symbol = "vel")
            avel_query = self.get_from_intention(obj_name = obj_name, symbol = "avel")

            if time_query is not None :
                self.feed_confirm(obj_name = obj_name, results = {"time" : self.timer.value})
            results = {}
            if mass_query is not None : 
                results["mass"] = self.units[obj_name].get_mass()
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
                    detects.append((obj_name, unit.get_position(), unit.get_velocity(), unit.get_radius()))
            for obj_name in radar_rcvs :
                self.feed_confirm(obj_name = obj_name, results = {"radar" : detects})
        
        if len(obstacle_rcvs) > 0 : 
            obtables = []
            for (name, unit) in self.units.items() :
                if isinstance(unit.shape, SegmentShape) :
                    ends = unit.shape.get_ends()
                    obstacle.append((name, ends[0], ends[1], unit.get_velocity()))
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
                pos = unit.get_position()
                step_data[name]["pos"] = "%f %f" % (pos[0], pos[1])
                angle = unit.get_angle()
                step_data[name]['angle'] = "%f" % angle
                stroke = unit.get_stroke_color()  
                step_data[name]["stroke"] = "%f %f %f" % (stroke[0], stroke[1], stroke[2])
                fill = unit.get_fill_color()  
                step_data[name]["fill"] = "%f %f %f" % (fill[0], fill[1], fill[2])
                pointer = unit.get_pointer_color()  
                step_data[name]["pointer"] = "%f %f %f" % (pointer[0], pointer[1], pointer[2])

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

                    pos= unit_data.get("pos", None)
                    if pos is not None :
                        self.units[name].set_position((float(pos.split(' ')[0]), float(pos.split(' ')[1])))

                    angle = unit_data.get('angle', None)
                    if angle is not None :
                        self.units[name].set_angle(float(angle))

                    stroke = unit_data.get("stroke", None)
                    if stroke is not None :
                        self.units[name].set_stroke_color((float(stroke.split(' ')[0]), float(stroke.split(' ')[1]), float(stroke.split(' ')[2])))
                        
                    fill = unit_data.get("fill", None)
                    if fill is not None :
                        self.units[name].set_fill_color((float(fill.split(' ')[0]), float(fill.split(' ')[1]), float(fill.split(' ')[2])))
                    pointer = unit_data.get("pointer", None)
                    if pointer is not None :
                        self.units[name].set_pointer_color((float(pointer.split(' ')[0]), float(pointer.split(' ')[1]), float(pointer.split(' ')[2])))


    def draw(self, screen) :
        for unit in self.units.values() :
            if unit.shape is not None :
                unit.shape.draw(screen)
                
        
class Aggregator(Logger) :

    object_status_focus = [
            "time", "force", "spin", "transmit", "listen", 
            "mass", "pos", "angle", "vel", "avel",
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


class Driver(Logger) : 

    object_attrs = {
            'step' : None,
    } 

    aggregator_attrs = {
            'pre' : None, 
            'post' : None,
    } 

    context_attrs = {
            'judge' : None,
    } 
    
    data_attrs = {
            'data' : None,
    }
    
    def __init__(self, aggr = None, context = None, objects = None, data = None) :
       
        self.context = None
        if context is not None :
            if check_attrs(context, self.context_attrs) :
                self.context = context
            else :
                self.error("Invalid 'context'")
        else :
            self.context = Context(delta = None)
    
        self.objects = []
        if objects is not None and hasattr(objects, '__iter__') :
            for obj in objects :
                if check_attrs(obj, self.object_attrs) :
                    self.objects.append(obj)
                else :
                    self.error("Invalid 'object'.")

        self.context.bind_objects(self.objects)
                    
        self.aggr = None
        if aggr is not None : 
            if check_attrs(aggr, self.aggregator_attrs) :
                self.aggr = aggr 
            else :
                self.error("Invalid 'aggr'.")
        else :  
            self.aggr = Aggregator()

        self.data = None
        if data is not None and check_attrs(data, self.data_attrs) :
                self.data = data 
        else :
            self.error("Invalid 'data'.")
        
        self.intention = {}
        self.confirm = {}
        self.step_count = 0
        
    def step(self) :
        step_data = None
        if self.data is not None :
            step_data = {}
            
        if self.aggr is not None and self.context is not None :
            self.aggr.pre(objects = self.objects, confirm = self.confirm)
            self.confirm = {}
            for obj in self.objects : 
                obj_data = None 
                if step_data is not None :
                    obj_data = {}
                obj.status['post'] = {}
                obj.step()
                obj.snap(obj_data = obj_data)
                if obj_data is not None and len(obj_data) > 0 :
                    if step_data.get(obj.name, None) is None :
                        step_data[obj.name] = {}
                    if step_data[obj.name].get("status", None) is None :
                        step_data[obj.name]["status"] = {}
                    for (key, value) in obj_data.items() :
                        step_data[obj.name]["status"][key] = value  
                obj.status['pre'] = {}
            self.intention = self.aggr.post(objects = self.objects)
            self.confirm = self.context.judge(intention = self.intention)
            if step_data is not None :
                self.context.snap(step_data = step_data)
            self.intention = {}
        else :
            self.error("None 'context' or none 'aggr'. Step omitted.")
       
        if step_data is not None and len(step_data) > 0:
            data_value = {str(self.step_count) : step_data}
            self.data.update(data_value = data_value)
        
        self.step_count += 1
            

class Simulator(Logger) :
    
    driver_attrs = {
        'step' : None,
    }
    
    inspector_attrs = {
        'check' : None,
    }
    
    def __init__(self, driver) :
        self.driver = None
        if driver is not None and check_attrs(driver, self.driver_attrs) :
            self.driver = driver 
        else :
            self.error("Invalid 'driver'.")

    def simulate(self, steps = None, inspector = None, graphics = False) :
        if self.driver is None :
            self.error("No valid 'driver' given.")
            return False 
        if steps is not None and type(steps).__name__ != 'int' :
            self.error("Invalid 'steps'.")
            return False 
        if inspector is not None and not check_attrs(inspector, self.inspector_attrs) :
            self.error("Invalid 'inspector'.")
            return False 
        
        pygame.init()

        screen = None
        width = 800
        height = 800
        if graphics :
             screen = pygame.display.set_mode((width, height))
        
        clock = pygame.time.Clock()
      
        steps_to_run = 0
        if steps is not None :   
            steps_to_run = steps
        
        
        font = pygame.font.Font(None, 16)
        help_info = [
                "ESC: quit; Space: pause/run; Key '->': next step;",
        ]
        
        pause = False
        running = True
        key_press_delay = 0
        
        while running :
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN :
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pause = not pause
                        if not pause and steps is not None :
                            steps_to_run = steps - step_count

            keys = pygame.key.get_pressed() 
            
            if key_press_delay > 0 : 
                key_press_delay -= 1
            elif keys[K_RIGHT] :
                steps_to_run = 1
                key_press_delay = 10000


            if (pause and steps_to_run > 0) or (not pause and (steps is None or self.driver.step_count < steps)) :

                self.driver.step()
                
                if steps_to_run > 0 : 
                    steps_to_run -= 1
                
                if inspector is not None and not inspector.check(context = self.driver.context, objects = self.driver.objects) : 
                    pause = True
                    steps_to_run = 0 
                    
                if screen is not None :
                    screen.fill(THECOLORS["white"])
                    
                    self.driver.context.draw(screen)
                    pygame.display.flip()

                    sim_info = [ 
                        "{:<10}".format("Steps:") + "%d" % self.driver.step_count, 
                        "{:<10}".format("Time:") + "%2.6f" % self.driver.context.timer.value, 
                    ]
                    
                    y = 5
                    for line in sim_info:
                        screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                        y += 10

                    y = height - 20
                    for line in help_info:
                        screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                        y -= 10
                        
                    pygame.display.set_caption("MultiAgent Simulator v1.0 (c) 2017-2018, NiL, csningli@gmail.com")
                    pygame.display.flip()
                    
                clock.tick(50)
 

class Inspector(Logger) :
    def __init__(self) :
        pass
        
    def check(self, context = None, objects = None) :
        return True


class LatestDataInspector(Inspector) :
    def __init__(self) :
        self.begin = 0
        self.end = None
        

class Data(Logger) :

    value_attrs = {
            'keys' : None, 
            'items' : None, 
            'get' : None, 
            '__iter__' : None, 
            '__getitem__' : None,
    }
    
    def __init__(self) :
        self.data = {}

    def to_file(self, filename = None) :
        if filename is None :
            filename = "multiagent_%s.data" % datetime.datetime.now().strftime("%Y%m%d%H%M%S_%f")
        with open(filename, 'w') as f : 
            json.dump(self.data, f)
        return filename

    def from_file(self, filename) :
        self.data = {}
        with open(filename, 'r') as f : 
            self.data = json.load(f)

    def update(self, data_value) :
        result = {}
        if not check_attrs(data_value, self.value_attrs) :
            self.error("Invalid 'data_value'.")
            return result 
        for (step_label, step_data) in data_value.items() :
            if hasattr(step_label, 'isdigit') and step_label.isdigit() and check_attrs(step_data, self.value_attrs) :
                result[step_label] = {}
                if (self.data.get(step_label, None) is None) : 
                    self.data[step_label] = step_data
                    result[step_label] = step_data
                else : 
                    for (name_label, obj_data) in step_data.items() :
                        if type(name_label).__name__ == 'str' :
                            result[step_label][name_label] = {}
                            if (self.data[step_label].get(name_label, None) is None) and check_attrs(obj_data, self.value_attrs):
                                self.data[step_label][name_label] = obj_data
                                result[step_label][name_label] = obj_data
                            else :
                                for (key, value) in obj_data.items() :
                                    if type(name_label).__name__ == 'str' and type(value).__name__ == 'str' :
                                        self.data[step_label][name_label][key] = value 
                                        result[step_label][name_label][key] = value
        return result 
        
    def get(self, none_value) :
        result = {}
        if not check_attrs(none_value, self.value_attrs) :
            self.error("Invalid 'none_value'.")
            return result 
        if len(none_value.items()) < 1 :
            result = self.data
        else :
            for (step_label, step_data) in none_value.items() :
                if hasattr(step_label, 'isdigit') and step_label.isdigit() :
                    result[step_label] = {}
                    if self.data.get(step_label, None) is None : 
                        result[step_label] = None 
                    elif step_data is None :
                        result[step_label] = self.data[step_label]
                    elif check_attrs(step_data, self.value_attrs) : 
                        for (name_label, obj_data) in step_data.items() :
                            if type(name_label).__name__ == 'str' :
                                result[step_label][name_label] = {}
                                if self.data[step_label].get(name_label, None) is None :
                                    result[step_label][name_label] = None 
                                elif obj_data is None :
                                    result[step_label][name_label] = self.data[step_label][name_label]
                                elif check_attrs(obj_data, self.value_attrs) :
                                    for (key, value) in obj_data.items() :
                                        if type(key).__name__ == 'str' :
                                            result[step_label][name_label][key] = self.data[step_label][name_label].get(key, None) 

        return result
        
        
class Zipper(Logger) :

    data_attrs = {
        'data' : None,
    }

    context_attrs = {
    }
    
    object_attrs = {
    }

    def __init__(self, data, context = None, objects = None) :
        self.data = None
        if check_attrs(data, self.data_attrs) :
                self.data = data 
        else :
            self.error("Invalid 'data'.")
        self.step_count = 0
            
        self.context = None
        if context is not None : 
            if check_attrs(context, self.context_attrs) :
                self.context = context
        else :
            self.context = Context(delta = None) 

        self.objects = []
        if objects is not None and hasattr(objects, '__iter__') :
            for obj in objects :
                if check_attrs(obj, self.object_attrs) :
                    self.objects.append(obj)
                else :
                    self.error("Invalid 'object'.")

        self.context.bind_objects(self.objects)


    def forward(self) :
        step_data = None
        if self.data is not None :
            max_count = max([int(key) for key in self.data.data.keys()])
            while step_data is None and self.step_count < max_count :
                self.step_count += 1
                step_data = self.data.get(none_value = {str(self.step_count) : None})[str(self.step_count)]
            self.mimic_to_data(step_data = step_data)
        else :
            self.error("No valid 'data' given.")
        return step_data


    def backward(self) :
        step_data = None
        if self.data is not None :
            while step_data is None and self.step_count > 0 :
                self.step_count -= 1
                step_data = self.data.get(none_value = {str(self.step_count) : None})[str(self.step_count)] 
            self.mimic_to_data(step_data = step_data)
        else :
            self.error("No valid 'data' given.")
        return step_data


    def mimic_to_data(self, step_data) :
        if step_data is not None :
            self.context.mimic(step_data = step_data)
            for obj in self.objects :
                if step_data.get(obj.name, None) is not None :
                    obj.mimic(obj_data = step_data[obj.name].get("status", None))
         

class Player(Logger) :

    zipper_attrs = {
        'forward' : None,
        'backward' : None,
        'context' : None,
    }
    
    def __init__(self, zipper) :
        self.zipper = None
        if zipper is not None and check_attrs(zipper, self.zipper_attrs) :
            self.zipper = zipper
        else :
            self.error("Invalid 'zipper'.")
        
    def play(self, steps = None, inspector = None, graphics = False) :
        if self.zipper is None :
            self.error("No valid 'zipper' given.")
            return False 
        if steps is not None and type(steps).__name__ != 'int' :
            self.error("Invalid 'steps'.")
            return False 
        if inspector is not None and not check_attrs(inspector, self.inspector_attrs) :
            self.error("Invalid 'inspector'.")
            return False 
        
        pygame.init()

        screen = None
        width = 800
        height = 800
        if graphics :
             screen = pygame.display.set_mode((width, height))
        
        clock = pygame.time.Clock()
    
        steps_to_run = 0
        if steps is not None :   
            steps_to_run = steps
        
        font = pygame.font.Font(None, 16)
        help_info = [
                "ESC: quit; Space: pause/run; Key '<-': previous step; Key '->': next step;",
        ]
        
        pause = False
        running = True
        key_press_delay = 0
        
        while running :
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN :
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pause = not pause
                        if not pause and steps is not None :
                            steps_to_run = steps - step_count

            keys = pygame.key.get_pressed() 
            
            if key_press_delay > 0 : 
                key_press_delay -= 1
            elif keys[K_RIGHT] :
                steps_to_run = 1
                key_press_delay = 10000
            elif keys[K_LEFT] :
                steps_to_run = -1
                key_press_delay = 10000

            if (pause and (steps_to_run > 0 or steps_to_run < 0)) or (not pause and (steps is None or self.driver.step_count < steps)) :
                
                step_data = None

                if pause :
                    if steps_to_run > 0 : 
                        step_data = self.zipper.forward()
                        steps_to_run -= 1
                    else : 
                        step_data = self.zipper.backward()
                        steps_to_run += 1
                else :
                    step_data = self.zipper.forward()


                if inspector is not None and not inspector.check(status = None) : 
                    pause = True
                    steps_to_run = 0 
                    
                if step_data is None :
                    pause = True
                    steps_to_run = 0 
                elif screen is not None :
                    screen.fill(THECOLORS["white"])
                    
                    self.zipper.context.draw(screen)
                    pygame.display.flip()

                    sim_info = [ 
                        "{:<10}".format("Steps:") + "%d" % self.zipper.step_count, 
                        "{:<10}".format("Time:") + "%2.6f" % self.zipper.context.timer.value, 
                    ]
                    
                    y = 5
                    for line in sim_info:
                        screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                        y += 10

                    y = height - 20
                    for line in help_info:
                        screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                        y -= 10
                        
                    pygame.display.set_caption("MultiAgent Player v1.0 (c) 2017-2018, NiL, csningli@gmail.com")
                    pygame.display.flip()
                    
                clock.tick(50)
    

#
# Modules
#

class Module(Logger) :

    msg_attrs = {
        "get" : None,
    }
    
    ram_attrs = {
        "get" : None,
    }
    
    symbol = None
    
    def __init__(self) :
        self.result = {"local" : {}, "post" : {}, "ram" : {}}
        self.buffs = None
        
    def perform(self, msg, ram) :
        self.result["post"] = {}
        self.result["local"] = {}
        self.update_information(msg = msg)
        return self.result

    def output(self, value) :
        self.result["post"][self.symbol] = value
        
    def inform_module(self, symbol, value) :
        if type(symbol).__name__ == "str" and len(symbol) > 0 :
            self.result["local"][symbol + "_buff"] = value
            
    def activate_sensors(self, symbols) :
        if type(symbols).__name__ == "list" and len(symbols) > 0 :
            for symbol in symbols :
                self.inform_module(symbol, "")

    def update_information(self, msg) :
        self.buffs = None
        if self.symbol is not None and check_attrs(msg, self.msg_attrs) :
            self.buffs = msg.get(self.symbol + "_buff", None)
            if self.buffs is not None :
                if type(self.buffs).__name__ != "list" or len(self.buffs) < 1 :
                    self.buffs = None

    def get_from_msg(self, msg, symbol) :
        value = None
        if check_attrs(msg, self.msg_attrs) and type(symbol).__name__ == "str" : 
            value = msg.get(symbol + "_result", None)
        return value

    def get_from_ram(self, ram, symbol) :
        value = None
        if check_attrs(ram, self.ram_attrs) and type(symbol).__name__ == "str" : 
            value = ram.get(symbol + "_value", None)
        return value

    def put_to_ram(self, ram, symbol, value) :
        if check_attrs(ram, self.ram_attrs) and type(symbol).__name__ == "str" : 
            ram[symbol + "_value"] = value 
        return ram 


class ColorModule(Module) :        # change object's color 
    symbol = "fill"
        
    def perform(self, msg, ram) :
        super(ColorModule, self).perform(msg = msg, ram = ram)
        if self.buffs is not None :
            r = 0.0
            g = 0.0
            b = 0.0
            for fill in self.buffs:
                r += fill[0] / len(fills)
                g += fill[1] / len(fills)
                b += fill[2] / len(fills)
            self.output(value = (r, g, b))
            
        return self.result


class ForceModule(Module) :        # simulate the force interface 
    symbol = "force"
        
    def perform(self, msg, ram) :
        super(ForceModule, self).perform(msg = msg, ram = ram)
        if self.buffs is not None :
            x = 0.0
            y = 0.0
            for force in self.buffs :
                x += force[0]
                y += force[1]
            self.output(value = (x, y))
            
        return self.result


class SetAVelModule(Module) :        # simulate the spin interface 
    symbol = "set_avel"
        
    def perform(self, msg, ram) :
        super(SetAVelModule, self).perform(msg = msg, ram = ram)
        if self.buffs is not None :
            avel = 0.0
            for a in self.buffs :
                avel += float(a) / len(self.buffs) 
            self.output(value = avel) 
            
        return self.result

class SetVelocityModule(Module) :        
    symbol = "set_vel"
        
    def perform(self, msg, ram) :
        super(SetVelocityModule, self).perform(msg = msg, ram = ram)
        if self.buffs is not None :
            vx = 0.0
            vy = 0.0
            for vel in self.buffs :
                vx += vel[0] 
                vy += vel[1] 
            self.output(value = (vx, vy)) 
            
        return self.result


class SetAngleModule(Module) :        
    symbol = "set_angle"
        
    def perform(self, msg, ram) :
        super(SetAngleModule, self).perform(msg = msg, ram = ram)
        if self.buffs is not None :
            a = 0.0
            for angle in self.buffs :
                a += angle / len(self.buffs)
            self.output(value = float(a)) 
            
        return self.result

class MoveModule(Module) :        # simulate the driver interface which drives the motion 
    symbol = "move"
        
    def perform(self, msg, ram) :
        super(MoveModule, self).perform(msg = msg, ram = ram)
        sensor_symbols = ["pos", "vel", "angle"]
        if self.buffs is not None :
            x = 0.0
            y = 0.0
            v = 0.0
            s = 0.0
            for move in self.buffs :
                if len(move) > 2 :
                    x += move[0]
                    y += move[1]
                    if v > 0.0 :
                        v = min(v, abs(move[2]))
                    else :
                        v = abs(move[2])
                    if s > 0.0 :
                        s = min(a, abs(move[3]))
                    else :
                        s = abs(move[3])

            mass = self.get_from_ram(ram = ram, symbol = "mass")
            if mass is None :
                mass_result = self.get_from_msg(msg = msg, symbol = "mass")
                if mass_result is None or type(mass_result).__name__ != "float" :
                    sensor_symbols.append("mass")
                else :
                    self.put_to_ram(ram = ram, symbol = "mass", value = mass_result)
            else :
                # calculate the force according to the move
                angle = self.get_from_msg(msg = msg, symbol = "angle")
                pos = self.get_from_msg(msg = msg, symbol = "pos")
                vel = self.get_from_msg(msg = msg, symbol = "vel")
                if None not in [pos, vel, angle] :
                    vec = (x - float(pos[0]), y - float(pos[1]))
                    norm = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
                    if norm > 0.001 :
                        vec = (vec[0] / norm, vec[1] / norm)
                    else :
                        vec = (0.0, 0.0)
                    if norm > 0.1 :
                        if angle > math.pi :
                            angle = angle  - 2 * math.pi
                            
                        spin = math.acos(vec[0])
                        
                        if vec[1] > 0.0 :
                            spin = spin - angle
                        else :
                            spin = - spin - angle
                        
                        if spin > math.pi : 
                            spin = spin - 2 * math.pi
                        elif spin < - math.pi : 
                            spin = spin + 2 * math.pi 

                        if abs(spin) / 2.0 < s :
                            s = abs(spin)

                        if abs(spin) > 0.001 :
                            self.inform_module(symbol = "set_avel", value = s * spin / (abs(spin) * mass))
                        
                        if abs(spin) > 0.5 :
                            vec = (0.0, 0.0)
                    v = min(norm, v)
                    self.inform_module(symbol = "force", value = (mass * (vec[0] * v - vel[0]), mass * (vec[1] * v - vel[1])))
        else :
            vel = self.get_from_msg(msg = msg, symbol = "vel")
            if vel is not None and math.sqrt(vel[0] * vel[0] + vel[1] * vel[1]) > 0.001 :
                self.inform_module(symbol = "force", value = (-vel[0], -vel[1]))
                
        self.activate_sensors(symbols = sensor_symbols)
            
        return self.result
        

class TransmitModule(Module) :   # simulate the transmit interface 
    symbol = "transmit"
        
    def perform(self, msg, ram) :
        super(TransmitModule, self).perform(msg = msg, ram = ram)

        if self.buffs is not None :
            transmit_union = ""
            for transmit in self.buffs :
                transmit_union = transmit_union + transmit + ";"
            self.output(value = transmit_union)
            
        return self.result


class ProcessModule(Module) :       # simulate the process action interface
    pass
    

class SensorModule(Module) :        # simulate the sensing action interface
    def perform(self, msg, ram) :
        super(SensorModule, self).perform(msg = msg, ram = ram)
        if self.buffs is not None :
            self.output(value = "")
        return self.result



class ListenModule(SensorModule) :   # simulate the listen interface 
    symbol = "listen"

class TimeSensorModule(SensorModule) :    # query for the global time 
    symbol = "time"

class ObstacleSensorModule(SensorModule) :  # query for obstacles 
    symbol = "obstacle"

class RadarSensorModule(SensorModule) :
    symbol = "radar"
    
class PositionSensorModule(SensorModule) :    # query for the position  
    symbol = "pos"


class AngleSensorModule(SensorModule) :    # query for the angle (counter clock from east) 
    symbol = "angle"


class VelocitySensorModule(SensorModule) :    # query for the velocity 
    symbol = "vel"


class AngularVelSensorModule(SensorModule) :    # query for the angular velocity
    symbol = "avel"
        
        
class MassSensorModule(SensorModule) :    # query for the angular velocity
    symbol = "mass"


if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v1.0")
    print("")
    print("(c) 2017-2018, NiL, csningli@gmail.com.")
    print("")
    #print("Interactive Mode.")
    print("")
