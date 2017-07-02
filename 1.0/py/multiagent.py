
import sys, os, time, datetime, json
import pygame
from pygame.locals import * 
from pygame.color import *

import pymunkoptions
pymunkoptions.options["debug"] = False
from pymunk import Circle, Body, Space, Vec2d

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
# Modules
#

class Module(Logger) :
    def __init__(self) :
        self.result = {"local" : {}, "post" : {}, "ram" : {}}
    def perform(self, msg, ram) :
        for key in self.result.keys() :
            self.result[key] = {}
        for (key, value) in msg.items() :
            if self.result["post"].get(key, None) is None :
                self.result["post"][key] = "" 
            self.result["post"][key] += str(value)
        for (key, value) in ram.items() :
            if self.result["ram"].get(key, None) is None :
                self.result["ram"][key] = ""
            self.result["ram"][key] += str(value)
        return self.result


class MotionModule(Module) :        # simulate the motion interface 
    def perform(self, msg, ram) :
        self.result["post"] = {}
        forces = msg.get("forces", None)
        if forces is not None and len(forces) > 0 :
            x = 0.0
            y = 0.0
            for force in forces:
                x += force[0]
                y += force[1]
            self.result["post"]["force"] = (x, y) 
        
        spins = msg.get("spins", None)
        if spins is not None and len(spins) > 0 :
            s = 0.0
            for spin in spins:
                s += spin
            self.result["post"]["spin"] = s 
        return self.result


class CommunicateModule(Module) :   # simulate the communication interface 
    def perform(self, msg, ram) :
        self.result["post"] = {}
        packets = msg.get('packets', None)
        if packets is not None and len(packets) > 0 :
            transmit = ""
            for packet in packets:
                transmit = transmit + packet + ";"
            self.result['post']['transmit'] = transmit
        return self.result


class ProcessModule(Module) :       # simulate the process action interface
    pass


class SensorModule(Module) :        # simulate the sensing action interface
    pass


class TimeSensorModule(SensorModule) :    # query for the global time 
    def perform(self, msg, ram) :
        self.result["post"] = {}
        self.result['post']['time'] = ""
        return self.result
        

class PositionSensorModule(SensorModule) :    # query for the position  
    def perform(self, msg, ram) :
        self.result["post"] = {}
        self.result['post']['position'] = ""
        return self.result
        
        
class AngleSensorModule(SensorModule) :    # query for the angle (counter clock from east) 
    def perform(self, msg, ram) :
        self.result["post"] = {}
        self.result['post']['angle'] = ""
        return self.result

class VelocitySensorModule(SensorModule) :    # query for the velocity 
    def perform(self, msg, ram) :
        self.result["post"] = {}
        self.result['post']["velocity"] = ""
        return self.result

class AngularVelSensorModule(SensorModule) :    # query for the angular velocity
    def perform(self, msg, ram) :
        self.result["post"] = {}
        self.result['post']["angular_velocity"] = ""
        return self.result

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
        
    def step(self, obj_data = None) :
        self.info("%s steps." % self)
        
        #self.info("%s '%s' pre-status: %s" % (obj.__class__.__name__, obj.name, obj.status['pre']))
        
        for key in self.status['local'].keys() :
            self.status['pre'][key] = self.status['local'][key]
        self.status['local'] = {}
        
        for mod in self.mods : 
            result = mod.perform(msg = self.status['pre'], ram = self.status['mem'])
            for domain in ["local"] : 
                domain_result = result.get(domain, None) 
                if domain_result is not None :
                    for key in domain_result.keys() :
                        if self.status[domain].get(key, None) is None :
                            self.status[domain][key] = []
                        self.status[domain][key].append(domain_result[key])
            for domain in ["post"] : 
                domain_result = result.get(domain, None) 
                if domain_result is not None :
                    for key in domain_result.keys() :
                        self.status[domain][key] = domain_result[key]
        #self.info("%s '%s' post-status: %s" % (obj.__class__.__name__, obj.name, obj.status['post']))

    def mimic(self, obj_data) :
        pass


class Agent(Object) :
    pass
    

class CircleShape(Logger, Circle) : 

    def draw(self, screen, font) :
        r = self.radius
        p = self.body.position
        rot = self.body.rotation_vector
        (width, height) = screen.get_size()

        # adjust the drawing coordinates to make sure (0, 0) stays in the center
        
        p[0] = int(width / 2.0 + p[0]) 
        p[1] = int(height / 2.0 - p[1]) 

        head = Vec2d(rot.x, -rot.y) * r * 0.9
        pygame.draw.circle(screen, THECOLORS["blue"], p, int(r), 2)
        pygame.draw.line(screen, THECOLORS["red"], p, p + head)

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

    def get_angular_velocity(self) :
        return self.body.angular_velocity

    def apply_force(self, force) :
        self.body.force = force

    def apply_spin(self, spin) :
        self.body.angular_velocity = spin / self.body.mass

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

    def get_angle(self) :
        return self.shape.get_angle()
        
    def set_angle(self, angle) :
        self.shape.set_angle(angle)

    def get_velocity(self) :
        return self.shape.get_velocity() 

    def get_angular_velocity(self) :
        return self.shape.get_angular_velocity()


    def apply_force(self, force) :
        self.shape.apply_force(force)

    def apply_spin(self, spin) :
        self.shape.apply_spin(spin)

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


    def judge(self, intention, step_data = None) :
        self.intention = intention
        
        # collect and apply the physics information
        
        for (obj_name, obj_intention) in self.intention.items() :
            if obj_name in self.units.keys() :
                force = obj_intention.get('force', None)
                if force is not None :
                    self.units[obj_name].apply_force(force)
                spin = obj_intention.get('spin', None)
                if spin is not None :
                    self.units[obj_name].apply_spin(spin)

        # physics engine step 
        
        self.space.step(self.delta)
        self.timer.tick(self.delta)

        # response to the sensors 

        self.confirm = {}
        for (obj_name, obj_intention) in self.intention.items() :
                if self.confirm.get(obj_name, None) is None :
                    self.confirm[obj_name] = {}
                    
                time_query = obj_intention.get('time', None)
                pos_query = obj_intention.get('position', None)
                angle_query = obj_intention.get('angle', None)
                velocity_query = obj_intention.get('velocity', None)
                angular_velocity_query = obj_intention.get('angular_velocity', None)

                if time_query is not None :
                    self.confirm[obj_name]['timer_value'] = self.timer.value

                if self.units.get(obj_name, None) is not None : 
                    if pos_query is not None : 
                        pos = self.units[obj_name].get_position()
                        self.confirm[obj_name]['pos_x'] = pos[0]
                        self.confirm[obj_name]['pos_y'] = pos[1]
                    if angle_query is not None : 
                        self.confirm[obj_name]['angle'] = self.units[obj_name].get_angle() 
                    if velocity_query is not None : 
                        vel = self.units[obj_name].get_velocity()
                        self.confirm[obj_name]["vel_x"] = vel[0]
                        self.confirm[obj_name]["vel_y"] = vel[1]
                    if angular_velocity_query is not None : 
                        self.confirm[obj_name]['angular_vel'] = self.units[obj_name].get_angular_velocity() 

        self.post_judge()

        if step_data is not None and check_attrs(step_data, self.step_data_attrs) :
            for (name, unit) in self.units.items() :
                if step_data.get(name, None) is None :
                    step_data[name] = {}
                pos = unit.get_position()
                angle = unit.get_angle()
                step_data[name]['pos_x'] = pos[0]
                step_data[name]['pos_y'] = pos[1]
                step_data[name]['angle'] = angle
            step_data['timer_value'] = self.timer.value
        
        return self.confirm


    def post_judge(self) :
        transmits = {}
        for (obj_name, obj_intention) in self.intention.items() :
            if obj_name in self.units.keys() :
                transmit = obj_intention.get('transmit', None)
                if transmit is not None :
                    transmits[obj_name] = transmit 
        for (unit_name, unit) in self.units.items() :
            if self.confirm.get(unit_name, None) is None :
                self.confirm[unit_name] = {}
            self.confirm[unit_name]['receive'] = transmits


    def mimic(self, step_data) :
        if step_data is not None and check_attrs(step_data, self.step_data_attrs):
            timer_value = step_data.get('timer_value', None)
            if timer_value is not None :
                self.timer.value = float(timer_value)
            for (name, unit_data) in step_data.items() :
                if name == "timer_value" :
                    continue
                if name not in self.units.keys() :
                    self.units[name] = Unit(name = name)
                pos_x = unit_data.get('pos_x', None)
                pos_y = unit_data.get('pos_y', None)
                if pos_x is not None and pos_y is not None :
                    self.units[name].set_position((float(pos_x), float(pos_y)))
                angle = unit_data.get('angle', None)
                if angle is not None :
                    self.units[name].set_angle(float(angle))
    

    def draw(self, screen, font) :
        for unit in self.units.values() :
            if unit.shape is not None :
                unit.shape.draw(screen, font)
                
        
class Aggregator(Logger) :

    object_status_focus = ['force', 'spin', 'time', 'position', 'angle', 'transmit', "velocity", "angular_velocity"]

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
                obj.step(obj_data = obj_data)
                if obj_data is not None and len(obj_data) > 0 :
                    if step_data.get(obj.name, None) is None :
                        step_data[obj.name] = {}
                    for (key, value) in obj_data :
                        step_data[obj.name][key] = value  
                obj.status['pre'] = {}
            self.intention = self.aggr.post(objects = self.objects)
            self.confirm = self.context.judge(intention = self.intention, step_data = step_data)
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
        width = 600
        height = 600
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
                    
                    self.driver.context.draw(screen, font)
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
                obj.mimic(obj_data = step_data.get(obj.name, None))
        
         

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
        width = 600
        height = 600
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
                    
                    self.zipper.context.draw(screen, font)
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
    

if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v1.0")
    print("")
    print("(c) 2017-2018, NiL, csningli@gmail.com.")
    print("")
    print("Interactive Mode.")
    print("")
