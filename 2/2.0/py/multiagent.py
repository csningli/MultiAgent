
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

# import sys modules
import sys, os, os.path, copy, time, datetime, json, math, inspect, pickle, sqlite3
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

    __visible = True
    __stroke_color = THECOLORS["black"]
    __fill_color = THECOLORS["black"]
    __pointer_color = THECOLORS["red"]

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

    @property
    def visible(self) :
        return self.__visible

    @visible.setter
    def visible(self, value) :
        self.__visible = value


class Object(Circle, LookMixin) :
    def __init__(self, name, mass = 1.0, radius = 10.0) :
        body = Body(mass = mass, moment = moment_for_circle(mass, 0, radius, (0,0)))
        super(Object, self).__init__(body, radius, (0, 0))
        self.__name = name
        self.mass = mass

    def info(self) :
        return "<<multiagent.%s name=%s>>" % (type(self).__name__, self.name)

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, name) :
        self.__name = name

    # uncomment the property mass, then you can get or set the mass of the body directly.

    #@property
    #def mass(self) :
        #return self.body.mass

    #@mass.setter
    #def mass(self, m) :
    #    self.body.mass = m

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
        return tuple(self.body.velocity)

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
        return tuple(self.body.force)

    @force.setter
    def force(self, force) :
        self.body.force = force

    @property
    def prop(self) : # props is in key-value dict.
        p = {
            "mass" : str(self.mass),
            "radius" : str(self.radius),
            "pos" : str(self.pos),
            "angle" : str(self.angle),
            "rot" : str(self.rot),
            "vel" : str(self.vel),
            "avel" : str(self.avel),
            "force" : str(self.force),
            "pcolor" : str(self.pointer_color),
            "fcolor" : str(self.fill_color),
            "scolor" : str(self.stroke_color),
            "visible" : str(self.visible),
        }
        # print("prop:", self.fill_color, p["fcolor"], p["pcolor"])
        return p

    @prop.setter
    def prop(self, p) :
        if "mass" in p.keys() :
            self.mass = float(p["mass"])
        if "angle" in p.keys() :
            self.angle = float(p["angle"])
        if "avel" in p.keys() :
            self.avel = float(p["avel"])
        if "visible" in p.keys() :
            self.visible = bool(p["visible"])
        if "pos" in p.keys() :
            self.pos = tuple([float(i) for i in p["pos"].strip("(").strip(")").split(",")])
        if "rot" in p.keys() :
            self.rot = tuple([float(i) for i in p["rot"].strip("(").strip(")").split(",")])
        if "vel" in p.keys() :
            self.vel = tuple([float(i) for i in p["vel"].strip("(").strip(")").split(",")])
        if "force" in p.keys() :
            self.force = tuple([float(i) for i in p["force"].strip("(").strip(")").split(",")])
        if "pcolor" in p.keys() :
            self.pointer_color = tuple([int(i) for i in p["pcolor"].strip("(").strip(")").split(",")])
        if "fcolor" in p.keys() :
            self.fill_color = tuple([int(i) for i in p["fcolor"].strip("(").strip(")").split(",")])
        if "scolor" in p.keys() :
            self.stroke_color = tuple([int(i) for i in p["scolor"].strip("(").strip(")").split(",")])

    def draw(self, screen) :
        if self.visible == True :
            p = Vec2d(self.pos)
            rot = Vec2d(self.rot)
            r = self.radius
            (width, height) = screen.get_size()

            # adjust the drawing coordinates to make sure (0, 0) stays in the center

            p.x = int(width / 2.0 + p.x)
            p.y = int(height / 2.0 - p.y)

            head = Vec2d(rot.x, -rot.y) * self.radius * 0.9
            pygame.draw.circle(screen, self.stroke_color, p, int(r), 2)
            pygame.draw.circle(screen, self.fill_color, p, int(r/2.0), 4)
            pygame.draw.line(screen, self.pointer_color, p, p + head)


class Obstacle(Segment, LookMixin) :
    def __init__(self, name, a = (0.0, 0.0), b = (0.0, 0.0), radius = 1.0) :
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
    def start(self) :
        return tuple(self.a)

    @property
    def end(self) :
        return tuple(self.b)

    @property
    def prop(self) : # props is in key-value dict.
        p = {
            "start" : str(self.start),
            "end" : str(self.end),
            "radius" : str(self.radius),
            "pcolor" : str(self.pointer_color),
            "fcolor" : str(self.fill_color),
            "scolor" : str(self.stroke_color),
            "visible" : str(self.visible),
        }
        return p

    @prop.setter
    def prop(self, p) :
        if "pcolor" in p.keys() :
            self.pointer_color = tuple([int(i) for i in p["pcolor"].strip("(").strip(")").split(",")])
        if "fcolor" in p.keys() :
            self.fill_color = tuple([int(i) for i in p["fcolor"].strip("(").strip(")").split(",")])
        if "scolor" in p.keys() :
            self.stroke_color = tuple([int(i) for i in p["scolor"].strip("(").strip(")").split(",")])
        if "visible" in p.keys() :
            self.visible = bool(p["visible"])

    def draw(self, screen) :
        if self.visible == True :
            (width, height) = screen.get_size()
            start = (int(width / 2.0 + self.start[0]), int(height / 2.0 - self.start[1]))
            end = (int(width / 2.0 + self.end[0]), int(height / 2.0 - self.end[1]))
            pygame.draw.line(screen, self.stroke_color, start, end, int(self.radius))


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

    @property
    def objs(self) :
        return self.__objs

    @property
    def obts(self) :
        return self.__obts

    def add_obj(self, obj) :
        if check_attrs(obj, {
                "body" : None,
                "name" : None,
                "pos" : None,
                "angle" : None,
                "rot" : None,
                "vel" : None,
                "avel" : None,
                "force" : None,
            }) and obj.name not in self.objs.keys() :
            self.add(obj.body, obj)
            self.objs[obj.name] = obj

    def add_obt(self, obt) :
        if check_attrs(obt, {
                "body" : None,
                "a" : None,
                "b" : None,
                "radius" : None,
            }) and obt.name not in self.obts.keys() :
            self.add(obt.body, obt)
            self.obts[obt.name] = obt

    def get_obj_with(self, name) :
        return self.objs.get(str(name), None)

    def get_obt_with(self, name) :
        return self.obts.get(str(name), None)

    def get_objs_at(self, c, d = 0, dist = ppdist_l2) :
        objs = []
        if hasattr(c, "__len__") and len(c) > 1 :
            for name, obj in self.objs.items() :
                if dist(c, obj.pos) < d + obj.radius:
                    objs.append(obj)
        return objs

    def get_obts_at(self, c, d = 0, dist = pldist_l2) :
        obts = []
        if hasattr(c, "__len__") and len(c) > 1 :
            for name, obt in self.obts.items() :
                if dist(c, obt.start, obt.end) < d:
                    obts.append(obt)
        return obts

    def touch(self, c, d = 0) :
        blocks = []
        for obj in self.get_objs_at(c, d) :
            l = ppdist_l2(obj.pos, c)
            x = obj.pos[0] - c[0]
            y = obj.pos[1] - c[1]
            if (abs(l) > 0.001) :
                x *= max(0, l - obj.radius) / float(l)
                y *= max(0, l - obj.radius) / float(l)
            blocks.append((x, y))
        for obt in self.get_obts_at(c, d) :
            diff = pldiff(c, obt.start, obt.end)
            blocks.append((- diff[0], - diff[1]))
        return blocks

    def draw(self, screen) :
        for obj in self.objs.values() + self.obts.values() :
            obj.draw(screen)

    def clear(self, dist) :
        names_of_dead = []
        for name, obj in self.objs.items() :
            if ppdist_l2(obj.pos, (0, 0)) > dist :
                self.remove(obj.body)
                names_of_dead.append(name)
        for name in names_of_dead :
            del(self.objs[name])
        return names_of_dead


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
        return self.__content

    @property
    def dests(self) :
        return self.__content.keys()

    def add_msg(self, msg) :
        if check_attrs(msg, {"src" : None, "dest" : None, "key" : None, "value" : None}) :
            if msg.dest not in self.content.keys() :
                self.content[str(msg.dest)] = [] # msgs are organized according to the dest.
            self.content[str(msg.dest)].append(msg)

    def get_msgs(self, dest) :
        return self.content.get(str(dest), [])


class Response(Request) :
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
            self.read += delta
        else :
            self.read += self.delta


class Context(object) :
    def __init__(self, oracle = None, delta = 0.01, objs = [], obts = []) :
        if oracle is not None :
            if check_attrs(oracle, {
                        "objs" : None,
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

        if type(delta).__name__ in ["float", "int"] :
            self.__timer = Timer(float(delta))
        else :
            print("Invalid delta for the construction of context. Exit.")
            exit(1)

        for obj in objs :
            self.add_obj(obj)

        for obt in obts :
            self.add_obt(obt)

        self.__reqt = None
        self.__resp = None

    def info(self) :
        return "<<multiagent.%s has_oracle=%d>>" % (type(self).__name__, self.__oracle is not None)

    @property
    def oracle(self) :
        return self.__oracle

    @property
    def timer(self) :
        return self.__timer

    @property
    def reqt(self) :
        return self.__reqt

    @reqt.setter
    def reqt(self, value) :
        self.__reqt = value

    @property
    def resp(self) :
        return self.__resp

    @resp.setter
    def resp(self, value) :
        self.__resp = value

    @property
    def time(self) :
        return self.timer.read

    @property
    def timer_delta(self) :
        return self.timer.delta

    @property
    def obj_props(self) : # obj_props is in name-dict dict.
        props = {}
        for name, obj in self.__oracle.objs.items() :
            props[name] = obj.prop
        return props

    @obj_props.setter
    def obj_props(self, props) :
        for name, prop in props.items() :
            obj = self.__oracle.objs.get(name, None)
            if obj is not None :
                obj.prop = prop

    @property
    def obt_props(self) : # obt_props is in name-dict dict.
        props = {}
        for name, obt in self.__oracle.obts.items() :
            props[name] = obt.prop
        return props

    @obt_props.setter
    def obt_props(self, props) :
        for name, prop in props.items() :
            obt = self.__oracle.obts.get(name, None)
            if obt is not None :
                obt.prop = prop

    @property
    def paras(self) : # paras is in key-value dict.
        p = {
            "time" : str(self.__timer.read),
        }
        return p

    @paras.setter
    def paras(self, p) :
        if "time" in p.keys() :
            self.__timer.read = float(p["time"])

    def handle_reqt(self, reqt) :
        self.reqt = reqt
        self.resp = Response()

        # interaction between the context and the agents

        msgs = {}
        for msg in self.reqt.get_msgs(dest = "") :
            if msg.src not in msgs.keys() :
                msgs[msg.src] = []
            msgs[msg.src].append(msg)

        for name, obj in self.oracle.objs.items() :
            for msg in msgs.get(name, []) :
                if msg.key == "vel" :
                    obj.vel = msg.value
                elif msg.key == "avel" :
                    obj.avel = msg.value
                elif msg.key == "pos" :
                    obj.pos = msg.value
                elif msg.key == "angle" :
                    obj.angle = msg.value
                elif msg.key == "force" :
                    obj.force = msg.value
                elif msg.key == "color" :
                    obj.fill_color = tuple(msg.value)
            for key, value in {"pos" : obj.pos, "angle" : obj.angle, "vel" : obj.vel, "avel" : obj.avel,
                    "force" : obj.force, "color" : obj.fill_color}.items() :
                self.resp.add_msg(Message(dest = name, key = key, value = value))

        # handle the communication signals and the radar signals.

        radio_msgs = []
        radar_src_dist = {}
        for name, ms in msgs.items() :
            for msg in ms :
                if msg.key == "radio" :
                    radio_msgs.append(msg.value)
                elif msg.key == "radar" :
                    radar_src_dist[name] = msg.value

        for name in self.oracle.objs.keys() :
            self.resp.add_msg(Message(dest = name, key = "radio", value = copy.copy(radio_msgs)))

        for src, dist in radar_src_dist.items() :
            obj = self.oracle.objs.get(src, None)
            if obj is not None :
                self.resp.add_msg(Message(dest = src, key = "radar", value = self.__oracle.touch(obj.pos, dist)))
            else :
                self.resp.add_msg(Message(dest = src, key = "radar", value = self.__oracle.touch((0, 0), dist)))

        # run the physical engine and update the time recorded in the context

        self.oracle.step(self.timer.delta)
        self.timer.tick()

        return self.resp

    def handle_cmds(self, cmds) :
        pass

    def draw(self, screen) :
        self.oracle.draw(screen)

    def add_obj(self, obj) :
        return self.oracle.add_obj(obj)

    def remove_obj(self, name) :
        pass

    def add_obt(self, obt) :
        return self.oracle.add_obt(obt)

    def remove_obt(self, name) :
        pass

    def get_time_by_steps(self, steps) :
        return self.timer.delta * steps

    def get_objs_at(self, pos, d = 0) :
        return self.oracle.get_objs_at(tuple(pos), d)

    def get_obts_at(self, pos, d = 0) :
        return self.oracle.get_obts_at(tuple(pos), d)

    def clear(self, dist) :
        return self.oracle.clear(dist)


class Memory(object) :
    def __init__(self) :
        self.__content = {}

    def info(self) :
        return "<<multiagent.%s content_size=%d>>" % (type(self).__name__, len(self.content))

    @property
    def content(self) :
        return self.__content

    @content.setter
    def content(self, c) :
        if check_attrs(c, {"items" : {"__iter__" : None}}) :
            for key, value in c.items() :
                self.reg(key, value)

    def reg(self, key, value) :
        self.__content[key] = value

    def read(self, key, default_value = None) :
        return self.__content.get(key, default_value)


class Module(object) :
    def __init__(self) :
        self.__mem = Memory()

    def info(self) :
        return "<<multiagent.%s memory_size=%d>>" % (type(self).__name__, len(self.mem.content))

    @property
    def mem(self) : # module's memory will be set with the memory of the host agent.
        return self.__mem

    @mem.setter
    def mem(self, mem) :
        if check_attrs(mem, {"content" : None, "reg" : None, "read" : None}) :
            self.__mem = mem

    def sense(self, reqt) : # can directly access or modify "mem" - the request received by the host agent
        pass

    def process(self) : # can directly access or modify "mem" - the memory of the host agent
        pass

    def act(self, resp) : # can directly access or modify "resp" - the response will be sent by the host agent
        pass

    def get_pos(self) :
        return self.mem.read("pos", None)

    def get_angle(self) :
        return self.mem.read("angle", None)

    def get_vel(self) :
        return self.mem.read("vel", None)

    def apply_vel(self, vel) :
        self.mem.reg(key = "vel", value = vel)

    def get_avel(self) :
        return self.mem.read("avel", None)

    def apply_avel(self, avel) :
        self.mem.reg(key = "avel", value = avel)

    def get_force(self) :
        return self.mem.read("force", None)

    def apply_force(self, force) :
        self.mem.reg(key = "force", value = force)

    def get_color(self) :
        return self.mem.read("color", None)

    def apply_color(self, color) :
        self.mem.reg(key = "color", value = color)

    def get_radio_in_msgs(self) :
        return self.mem.read("radio_in", [])

    def get_radio_out_msg(self) :
        return self.mem.read("radio_out", None)

    def set_radio_out_msg(self, msg) :
        self.mem.reg("radio_out", msg)

    def get_radar_detect(self) :
        return self.mem.read("radar_detect", [])

    def get_radar_dist(self) :
        return self.mem.read("radar_dist", None)

    def set_radar_dist(self, dist) :
        self.mem.reg("radar_dist", dist)


class ObjectModule(Module) :
    def __init__(self) :
        super(ObjectModule, self).__init__()
        self.__buff = {}

    @property
    def buff(self) :
        return self.__buff

    def sense(self, reqt) :
        for msg in reqt.get_msgs(self.mem.read("name", None)) :
            for prop in ["pos", "angle", "vel", "avel", "force", "color"] :
                if msg.key == prop :
                    self.mem.reg(key = prop, value = msg.value)
                    self.buff[prop] = msg.value
                    break

    def act(self, resp) :
        for prop in ["vel", "avel", "force", "color", "angle", "pos"] :
            value = self.mem.read(prop, None)
            if value is not None and value != self.buff.get(prop, None) :
                resp.add_msg(Message(key = prop, value = value))
                self.mem.reg(key = prop, value = None)


class RadioModule(Module) :
    def sense(self, reqt) :
        agent_name = self.mem.read("name", None)
        for msg in reqt.get_msgs(agent_name) :
            if msg.key == "radio" :
                self.mem.reg(key = "radio_in", value = msg.value)
                break

    def act(self, resp) :
        radio_msg = self.mem.read("radio_out", None)
        if radio_msg is not None :
            resp.add_msg(Message(key = "radio", value = radio_msg))
            self.mem.reg(key = "radio_out", value = None)


class RadarModule(Module) :
    def sense(self, reqt) :
        agent_name = self.mem.read("name", None)
        for msg in reqt.get_msgs(agent_name) :
            if msg.key == "radar" :
                self.mem.reg(key = "radar_detect", value = msg.value)
                break

    def act(self, resp) :
        radar_dist = self.mem.read("radar_dist", None)
        if radar_dist is not None :
            resp.add_msg(Message(key = "radar", value = radar_dist))
            self.mem.reg(key = "radar", value = None)

class Agent(object) :
    def __init__(self, name) :
        self.__name = ""
        self.__mem = Memory()
        self.__mods = []
        self.__reqt = None
        self.__resp = None
        self.__active = True
        self.name = name
        self.config()

    def config(self, mods = None) :
        if mods is None :
            mods = [ObjectModule(),] # by default, only ObjectModule() is added.
            #mods = [ObjectModule(), RadioModule(), RadarModule()]
        self.__mods = []

        # configure the modules for the agent

        if check_attrs(mods, {"__iter__" : None, }) :
            for mod in mods :
                if check_attrs(mod, {"sense" : None, "process" : None, "act" : None, }) :
                    self.__mods.append(mod)
                    mod.mem = self.__mem

    def info(self) :
        return "<<multiagent.%s name=%s mods_num=%d>>" % (type(self).__name__, self.__name, len(self.__mods))

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, name) :
        self.__name = name
        self.__mem.reg("name", self.__name)

    @property
    def mods(self) :
        return self.__mods

    @property
    def active(self) :
        return self.__active

    @active.setter
    def active(self, value) :
        self.__active = value

    @property
    def focus(self) :
        focus_info = {
            "cmd" : str(self.__mem.read("cmd")),
            "angle" : str(self.__mem.read("angle")),
            "avel" : str(self.__mem.read("avel")),
        }

        pos = self.__mem.read("pos")
        if pos is not None :
            focus_info["pos"] =  "(%4.2f, %4.2f)" % (pos[0], pos[1])

        vel = self.__mem.read("vel")
        if vel is not None :
            focus_info["vel"] =  "(%4.2f, %4.2f)" % (vel[0], vel[1])

        force = self.__mem.read("force")
        if force is not None :
            focus_info["force"] =  "(%4.2f, %4.2f)" % (force[0], force[1])

        return focus_info

    @property
    def mem(self) :
        return self.__mem

    @property
    def mods(self) :
        return self.__mods

    def add_mod(self, mod) :
        if check_attrs(mod, {"sense" : None, "process" : None, "act" : None}) :
            self.__mods.append(mod)

    @property
    def reqt(self) :
        return self.__reqt

    #@reqt.setter
    #def reqt(self, r) :
        #if check_attrs(r, {"add_msg" : None, "get_msgs" : None}) :
            #self.__reqt = r

    @property
    def resp(self) :
        return self.__resp

    #@resp.setter
    #def resp(self, r) :
        #if check_attrs(r, {"add_msg" : None, "get_msgs" : None}) :
            #self.__resp = r

    def handle_reqt(self, reqt) :
        self.__reqt = reqt
        self.__resp = Response()

        #print("handle", self.__name, self.__mods)
        for mod in self.__mods :
            mod.sense(self.__reqt)
        for mod in self.__mods :
            mod.process()
        for mod in self.__mods :
            resp = mod.act(self.__resp)
        return self.__resp

    def handle_cmds(self, cmds) :
        self.__mem.reg(key = "cmd", value = cmds)

    @property
    def memo(self) : # memo is in key-value dict.
        m = {
            "active" : str(self.active),
            "__mem" : self.__mem.content, # the memo will be show in the focus information if the key is not prefixed with __
        }
        return m

    @memo.setter
    def memo(self, m) :
        self.active = bool(m["active"])
        self.__mem.content = m["__mem"]



class Shot(object) :
    def __init__(self) :
        self.__shot = {
            "obj_props" : {},
            "obt_props" : {},
            "context_paras" : {},
            "agent_memos" : {},
        }

    @property
    def obj_props(self) : # obj_props is in name-dict dict.
        return copy.copy(self.__shot["obj_props"])

    @obj_props.setter
    def obj_props(self, props) :
        self.__shot["obj_props"] = copy.copy(props)

    @property
    def obt_props(self) : # obt_props is in name-dict dict.
        return copy.copy(self.__shot["obt_props"])

    @obt_props.setter
    def obt_props(self, props) :
        self.__shot["obt_props"] = copy.copy(props)

    @property
    def agent_memos(self) : # agent_memos is in name-dict dict.
        return copy.copy(self.__shot["agent_memos"])

    @agent_memos.setter
    def agent_memos(self, memos) :
        self.__shot["agent_memos"] = copy.copy(memos)

    @property
    def context_paras(self) : # context_paras is in name-value dict.
        return copy.copy(self.__shot["context_paras"])

    @context_paras.setter
    def context_paras(self, paras) :
        self.__shot["context_paras"] = copy.copy(paras)

    #def set_obj_prop(self, name, key, value = None) :
        #if name not in self.__shot["obj_props"].keys() :
            #self.__shot["obj_props"][name] = {}
        #self.__shot["obj_props"][name][key] = value

    #def set_obt_prop(self, name, key, value = None) :
        #if name not in self.__shot["obt_props"].keys() :
            #self.__shot["obt_props"][name] = {}
        #self.__shot["obt_props"][name][key] = value

    #def set_anget_memo(self, name, key, value = None) :
        #if name not in self.__shot["agent_memos"].keys() :
            #self.__shot["agent_memos"][name] = {}
        #self.__shot["agent_memos"][name][key] = value

    #def set_context_para(self, key, value = None) :
    #    self.__shot["context_paras"][key] = value


class Data(object) :
    def __init__(self) :
        self.__data = []
        self.__filename =  "multiagent_%s.data" % datetime.datetime.now().strftime("%Y%m%d%H%M%S_%f")

    @property
    def size(self) :
        return len(self.__data)

    @property
    def filename(self) :
        return self.__filename

    @filename.setter
    def filename(self, fn) :
        if len(self.__data) > 0 :
            self.to_file()
        self.__filename = fn
        if self.__filename != "" :
            self.from_file()

    def add_shot(self, shot) :
        if check_attrs(shot, {
                "obj_props" : None,
                "obt_props" : None,
                "context_paras" : None,
                "agent_memos" : None,
            }) :
            self.__data.append(shot)

    def get_shot(self, index) :
        if type(index).__name__ == "int" and index >= 0 and index < len(self.__data) :
            return self.__data[index]

    def to_file(self) :
        result = False

        if self.__filename != None and self.__filename != "" :
            with open(self.__filename, 'w') as f :
                data = []
                for shot in self.__data :
                    data.append({
                        "obj_props" : shot.obj_props,
                        "obt_props" : shot.obt_props,
                        "context_paras" : shot.context_paras,
                        "agent_memos" : shot.agent_memos,
                    })
                json.dump(data, f)
                result = True

        return result

    def from_file(self) :
        self.__data = []

        if self.__filename != None and os.path.isfile(self.__filename) :
            data = []
            with open(self.__filename, 'r') as f :
                data = json.load(f)

            for d in data :
                shot = Shot()
                shot.obj_props = d["obj_props"]
                shot.obt_props = d["obt_props"]
                shot.agent_memos = d["agent_memos"]
                shot.context_paras = d["context_paras"]
                self.add_shot(shot)


class Schedule(object) :
    def __init__(self) :
        self.__queue = {}
        self.__last = -1

    def info(self) :
        return "<<multiagent.%s queue_len=%d last=%d>>" % (type(self).__name__, len(self.__queue), self.__last)

    def get_gen(self, category, name) :
        gen = None
        found = False
        while found == False :
            for item in self.__queue.values() :
                for temp in item[category] :
                    if temp.name == name :
                        gen = type(temp)
                        found = True

        return gen

    def get_agent_gen(self, name) :
        return self.get_gen("agent", name)

    def get_obj_gen(self, name) :
        return self.get_gen("obj", name)

    def get_obt_gen(self, name) :
        return self.get_gen("obt", name)

    def add_obj(self, obj, delay = 0) :
        self.queue_append(item = obj, category = "obj", delay = delay)

    def add_obt(self, obt, delay = 0) :
        self.queue_append(item = obt, category = "obt", delay = delay)

    def add_agent(self, agent, delay = 0) :
        self.queue_append(item = agent, category = "agent", delay = delay)

    def queue_append(self, item, category, delay = 0) :
        if int(delay) not in self.__queue.keys() :
            self.__queue[int(delay)] = {
                "obj" : [],
                "obt" : [],
                "agent" : [],
            }
            if int(delay) > self.__last :
                self.__last = int(delay)
        if category in ["obj", "obt", "agent"] :
            self.__queue[int(delay)][category].append(item)

    def queue_pop(self) : # the poped item is key-list dict.
        item = self.__queue.get(0, {"obj" : [], "obt" : [], "agent" : [],})
        self.__queue[0] = {
            "obj" : [],
            "obt" : [],
            "agent" : [],
        }

        delays = list(self.__queue.keys())
        delays.sort()
        for delay in delays :
            if delay < 1 :
                continue
            else :
                self.__queue[delay - 1] = self.__queue[delay]
                self.__queue[delay] = self.__queue.get(delay + 1, {"obj" : [], "obt" : [], "agent" : [],})

            if delay == self.__last :
                self.__last = delay - 1

        return item

class Driver(object) :
    def __init__(self, context, schedule) :
        if check_attrs(context, {"handle_reqt" : None, "handle_cmds" : None}) :
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

        self.__steps = 0
        self.__data = Data()

        self.__reqt = None
        self.__resp = None

    @property
    def filename(self) :
        return self.__data.filename

    @filename.setter
    def filename(self, fn = None) :
        self.__data.filename = fn
        if self.__data.size > 0 :
            self.__steps = self.__data.size - 1
            self.apply_shot(self.__data.get_shot(self.__steps))


    @property
    def agent_memos(self) :
        memos = {}
        for name, agent in self.__agents.items() :
            memos[name] = agent.memo
        return memos

    @agent_memos.setter
    def agent_memos(self, memos) :
        for name, memo in memos.items() :
            agent = self.__agents.get(name, None)
            if agent is not None :
                agent.memo = memo

    @property
    def steps(self) :
        return self.__steps

    @property
    def context_time(self) :
        return self.__context.time

    @property
    def context_timer_delta(self) :
        return self.__context.timer_delta

    def info(self) :
        return "<<multiagent.%s has_context=%d has_schedule=%d has_timer=%d agents_num=%d>>" % (
                type(self).__name__, self.__context is not None,
                self.__schedule is not None,
                self.__timer is not None,
                len(self.__agents))

    def draw(self, screen) :
        self.__context.draw(screen)

    def go(self) :
        result = True

        self.__steps += 1

        while self.__data.size < self.__steps :
            self.__data.add_shot(self.take_shot())

        if self.__steps < self.__data.size :
            self.apply_shot(self.__data.get_shot(self.__steps))
        else :
            item = self.__schedule.queue_pop()
            for obt in item["obt"] :
                self.__context.add_obt(obt)
            for obj in item["obj"] :
                self.__context.add_obj(obj)
            for agent in item["agent"] :
                if check_attrs(agent, {"name" : None, "handle_reqt" : None, "handle_cmds" : None}) and agent.name not in self.__agents.keys() :
                    self.__agents[agent.name] = agent

            # get request from agents' handling results

            self.__reqt = Response()

            reqts = {}
            for name, agent in self.__agents.items() :
                reqt = Request()
                if self.__resp is not None :
                    msgs = self.__resp.get_msgs(name)
                    for msg in msgs :
                        msg.src = ""
                        reqt.add_msg(msg)
                reqts[name] = reqt

            for name, reqt in reqts.items() :
                resp = self.__agents[name].handle_reqt(reqt)
                msgs = resp.get_msgs("")
                for msg in msgs :
                    msg.src = name
                    self.__reqt.add_msg(msg)

            # get response from context's handling result

            self.__resp = self.__context.handle_reqt(self.__reqt)
            self.__data.add_shot(self.take_shot())

        return result

    def back(self) :
        result = True
        if self.__steps > 0 :
            self.__steps -= 1
            self.apply_shot(self.__data.get_shot(self.__steps))
        return result

    def clear(self, dist) :
        agents_to_die = self.__context.clear(dist)
        for name in agents_to_die :
            if name in self.__agents.keys() :
                self.__agents[name].active = False
                del(self.__agents[name])

    def handle_cmds(self, cmd_msgs) :
        for agent in self.__agents.values() :
            agent.handle_cmds(cmd_msgs)
        self.__context.handle_cmds(cmd_msgs)

    def take_shot(self) :
        shot = self.__data.get_shot(self.__steps)
        if shot is None :
            shot = Shot()
            shot.agent_memos = self.agent_memos
            shot.context_paras = self.__context.paras
            shot.obj_props = self.__context.obj_props
            shot.obt_props = self.__context.obt_props
        return shot

    def apply_shot(self, shot) :
        result = False
        if check_attrs(shot, {"agent_memos" : None, "context_paras" : None, "obj_props" : None, "obt_props" : None}) :
            for agent in self.__agents.values() :
                agent.active = False
            for name, memo in shot.agent_memos.items() :
                if name not in self.__agents.keys() :
                    agent_gen = self.__schedule.get_agent_gen(name)
                    if agent_gen is None :
                        agent_gen = Agent
                    agent = agent_gen(name = name)
                    agent.memo = memo
                    self.__agents[name] = agent
                self.__agents[name].active = True

            for obj in self.__context.oracle.objs.values() :
                obj.visible = False
            for name, prop in shot.obj_props.items() :
                if name not in self.__context.oracle.objs.keys() :
                    obj_gen = self.__schedule.get_obj_gen(name)
                    if obj_gen is None :
                        obj_gen = Object
                    obj = obj_gen(name = name, mass = float(prop["mass"]), radius = float(prop["radius"]))
                    self.__context.oracle.add_obj(obj)

                self.__context.oracle.objs[name].visible = True

            for obt in self.__context.oracle.obts.values() :
                obt.visible = False
            for name, prop in shot.obt_props.items() :
                if name not in self.__context.oracle.obts.keys() :
                    obt_gen = self.__schedule.get_obt_gen(name)
                    if obt_gen is None :
                        obt_gen = Obstacle
                    obt = obt_gen(name = name,
                        a = tuple([int(i) for i in prop["start"].strip("(").strip(")").split(",")]),
                        b = tuple([int(i) for i in prop["end"].strip("(").strip(")").split(",")]),
                        radius = float(prop["radius"]))
                    self.__context.oracle.add_obt(obt)
                self.__context.oracle.obts[name].visible = True

            self.agent_memos = shot.agent_memos
            self.__context.paras = shot.context_paras
            self.__context.obj_props = shot.obj_props
            self.__context.obt_props = shot.obt_props
            result = True
        return result

    def export(self) :
        self.__data.to_file()

    def get_focus_objs(self, pos) :
        return self.__context.get_objs_at(pos)

    def get_focus_agents(self, pos) :
        agents = []
        objs = self.__context.get_objs_at(pos)
        for obj in objs :
            if obj is not None and obj.name in self.__agents.keys() :
                agents.append(self.__agents[obj.name])
        return agents


class Inspector(object) :
    def __init__(self, delay = 0) :
        self.__delay = 0
        self.__count = 0

        self.delay = delay
        self.reset()

    @property
    def delay(self) :
        return self.__delay

    @delay.setter
    def delay(self, value) :
        self.__delay = value

    def reset(self) :
        self.__count = self.__delay

    def check(self, shot) :
        result = "pass"
        if self.__count > 0 :
            self.__count -= 1
        else :
            if shot is not None and check_attrs(shot, {"obj_props" : None, "obt_props" : None, "agent_memos" : None, "context_paras" : None}) :
                pass
            self.reset()
        return result


class Commander(object) :
    __database = "./multiagent_commands.db"

    def __init__(self) :
        self.__con = None
        self.__timelabel = timelabel()

        if os.path.exists(self.__database) :
            self.__con = sqlite3.connect(self.__database)

    def check(self):
        msgs = []
        if self.__con is None and os.path.exists(self.__database) :
            self.__con = sqlite3.connect(self.__database)

        if self.__con is not None :
            cur = self.__con.cursor()
            cur.execute("SELECT * from Commands WHERE timelabel > \"%s\" ORDER BY timelabel DESC" % self.__timelabel)
            for record in cur.fetchall() :
                msgs.append(record[1])
                if record[0] > self.__timelabel :
                    self.__timelabel = record[0]
        return msgs


class Simulator(object) :
    def __init__(self, driver, cmdr = None, inspector = None) :
        self.__driver = None
        if driver is not None and check_attrs(driver, {"go" : None, "back" : None, "handle_cmds" : None}) :
            self.__driver = driver
        else :
            print("Invalid driver for the initialization of the simulator. Exit")
            exit(1)

        self.__cmdr = None
        if cmdr is None :
            self.__cmdr = Commander()
        else :
            if check_attrs(cmdr, {"check" : None,}) :
                self.__cmdr = cmdr
            else :
                print("Invalid commander for the initialization of the simulator. Create a new one.")
                exit(1)

        self.__inspector = None
        if inspector is None or check_attrs(inspector, {"check" : None}) :
            self.__inspector = inspector
        else :
            print("Invalid inspector for the initialization of the simulator. Exit")
            exit(1)

    def info(self) :
        return "<<multiagent.%s has_driver=%d>>" % (type(self).__name__, self.__driver is not None)

    def simulate(self, inspector = None, width = 800, height = 800, limit = None, graphics = False, filename = None) :
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
        sim_info = []

        delay = 0       # delay between handling key presses
        speed = 1         # number of rounds in one step
        phases = None     # number of steps to run; None for ever

        running = True
        pause = False
        updated = False

        focus_info = []
        focus_agents = []

        cmd_msgs = []

        if filename is not None :
            self.__driver.filename = filename
            if filename != "" :
                pause = True
                updated = True

        while (limit is None or self.__driver.steps < limit) and running :
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
            elif screen is not None and pause == True and pygame.mouse.get_pressed()[0] == True :
                p = pygame.mouse.get_pos()
                focus_agents = self.__driver.get_focus_agents((int(p[0] - screen.get_width()/2.0), int(screen.get_height()/2.0 - p[1])))
                updated = True

            clock.tick(1 / self.__driver.context_timer_delta)

            if (phases is None or phases != 0) and (pause == False) :
                if len(cmd_msgs) > 0 :
                    self.__driver.handle_cmds(cmd_msgs)
                    cmd_msgs = []
                if phases is None or phases > 0 :
                    for i in range(speed) :
                        self.__driver.go()
                    if phases is not None and phases > 0 :
                        phases -= 1
                    if inspector is not None :
                        check_result = inspector.check(self.__driver.take_shot())
                        if check_result == "pause" :
                            pause = True
                        elif check_result == "exit" :
                            running = False
                    self.__driver.clear(2.0 * ppdist_l2((width, height), (0, 0)))
                elif phases < 0 :
                    for i in range(speed) :
                        self.__driver.back()
                    phases += 1

                if phases == 0 :
                    pause = True

                updated = True
            else :
                msgs = self.__cmdr.check()
                if len(msgs) > 0 :
                    cmd_msgs = msgs + cmd_msgs
                updated = True


            if updated == True and screen is not None :

                screen.fill(THECOLORS["white"])

                self.__driver.draw(screen)
                pygame.display.flip()

                sim_info = [
                    rfix_str_len("Speed:", 12, ':') + "%d" % speed,
                    rfix_str_len("Steps:", 12, ':') + "%d" % self.__driver.steps,
                    rfix_str_len("Time:", 12, ':') + "%.3f" % self.__driver.context_time,
                ]

                y = 5
                for line in sim_info:
                    screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                    y += 10

                y = 5
                for focus_agent in focus_agents :
                    if focus_agent.active == True :
                        focus_info = [
                            rfix_str_len("name:", 16, ':') + " " * 4 + rfix_str_len(str(focus_agent.name), 20),
                        ]
                        focus_info_width = len(focus_info[0])
                        for key, value in focus_agent.focus.items() :
                            if len(key) > 1 :
                                focus_info.append(rfix_str_len("%s" % key + ":", 16, ':') + " " * 4 + rfix_str_len("%s" % value, 20))
                                focus_info_width = len(focus_info[-1])
                        focus_info.append("")

                        for line in focus_info:
                            screen.blit(font.render(line, 1, THECOLORS["black"]), (screen.get_width() - 5.5 * focus_info_width - 10, y))
                            y += 10

                if len(cmd_msgs) > 0 :
                    y = height - 20
                    for msg in cmd_msgs :
                        if len(msg) > 50 :
                            line = lfix_str_len(msg, 50)
                        else :
                            line = msg
                        screen.blit(font.render(line, 1, THECOLORS["red"]), (screen.get_width() - 5.5 * len(line) - 10, y))
                        y -= 10

                y = height - 20
                for line in help_info:
                    screen.blit(font.render(line, 1, THECOLORS["black"]), (5, y))
                    y -= 10


                pygame.display.set_caption("MultiAgent Simulator v2.0 (c) 2017-2018, NiL, csningli@gmail.com")
                pygame.display.flip()
                pygame.event.pump()

            updated = False

        # end of the simulation

        self.__driver.export()


if __name__ == '__main__' :
    print("")
    print("MultiAgent Simulator v2.0 (c) 2017-2018, NiL, csningli@gmail.com.")
