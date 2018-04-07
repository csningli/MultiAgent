
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, random, datetime, math
random.seed(datetime.datetime.now())

sys.path.append("../../2.0/py")

from multiagent import *
from utils import *

amoebot_radius = 10.0

def pq_to_xy(a) :
    b = array([0.0, 0.0])
    p = a[0]
    q = a[1]
    x = 2 * amoebot_radius * p + 2 * amoebot_radius *  math.cos(math.pi / 3.0) * q
    y = 2 * amoebot_radius *  math.cos(math.pi / 6.0) * q
    b[0] = x
    b[1] = y
    return b

def wq_to_xy(a) :
    b = array([0.0, 0.0])
    p = a[0]
    q = a[1]
    x = -2 * amoebot_radius * p -2 * amoebot_radius *  math.cos(math.pi / 3.0) * q
    y = 2 * amoebot_radius *  math.cos(math.pi / 6.0) * q
    b[0] = x
    b[1] = y
    return b

def xy_to_pq(b) :
    a = array([0.0, 0.0])
    x = b[0]
    y = b[1]
    q = int(float(y) / (2 * amoebot_radius *  math.cos(math.pi / 6.0)))
    p = int((float(x) -  2 * amoebot_radius *  math.cos(math.pi / 3.0) * q) / (2 * amoebot_radius))
    a[0] = p
    a[1] = q
    return a

# share the memory among all the agents
shared_memory = {}

class AmoeObject(Object) :
    @property
    def amoe_pos(self) :
        return tuple(xy_to_pq(self.pos))

    @amoe_pos.setter
    def amoe_pos(self, pos) :
        self.pos = pq_to_xy(pos)

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


class AmoeOracleSpace(OracleSpace) :
    def __init__(self, objs = [], obts = []) :
        super(AmoeOracleSpace, self).__init__(objs, obts)
        self.__objs_indexing = {}

    def add_obj(self, obj) :
        if check_attrs(obj, {
                "body" : None,
                "name" : None,
                "pos" : None,
                #"angle" : None,
                #"rot" : None,
                #"vel" : None,
                #"avel" : None,
                #"force" : None,
            }) and obj.name not in self.objs.keys() :
            self.objs[obj.name] = obj
            if str(obj.amoe_pos) not in self.__objs_indexing.keys() :
                self.__objs_indexing[str(obj.amoe_pos)] = []
            self.__objs_indexing[str(obj.amoe_pos)].append(obj.name)

    def add_obt(self, obt) :
        if check_attrs(obt, {
                "body" : None,
                "a" : None,
                "b" : None,
                "radius" : None,
            }) and obt.name not in self.obts.keys() :
            self.obts[obt.name] = obt

    def move_amoe_obj(self, name, amoe_pos) :
        amoe_pos = tuple(amoe_pos)
        if name in self.objs.keys() :
            obj = self.objs[name]
            if str(obj.amoe_pos) in self.__objs_indexing.keys() :
                if name in self.__objs_indexing[str(obj.amoe_pos)] :
                    index = self.__objs_indexing[str(obj.amoe_pos)].index(name)
                    del(self.__objs_indexing[str(obj.amoe_pos)][index])
            obj.amoe_pos = amoe_pos
            if str(amoe_pos) not in self.__objs_indexing.keys() :
                self.__objs_indexing[str(amoe_pos)] = []
            self.__objs_indexing[str(amoe_pos)].append(name)

    def objs_at_amoe_pos(self, amoe_pos) :
        amoe_pos = tuple(amoe_pos)
        return self.__objs_indexing.get(str(amoe_pos), [])

    def draw(self, screen) :
        # draw objs

        for obj in self.objs.values() :
            obj.draw(screen)

        # draw connection between the coupled objects

        (width, height) = screen.get_size()
        for i in range(int(math.floor(len(self.objs) / 2.0))) :
            head = self.objs[str(2 * i)]
            tail = self.objs[str(2 * i + 1)]
            if head.amoe_pos != tail.amoe_pos :
                head_draw = [int(round(width / 2.0 + head.pos[0])), int(round(height / 2.0 - head.pos[1]))]
                tail_draw = [int(round(width / 2.0 + tail.pos[0])), int(round(height / 2.0 - tail.pos[1]))]
                pygame.draw.line(screen, head.stroke_color, head_draw, tail_draw, 4)


class AmoeContext(Context) :
    def handle_reqt(self, reqt) :
        resp = super(AmoeContext, self).handle_reqt(reqt)

        msgs = {}
        for msg in self.reqt.get_msgs(dest = "") :
            if msg.src not in msgs.keys() :
                msgs[msg.src] = []
            msgs[msg.src].append(msg)

        for i in range(int(math.floor(len(self.oracle.objs)/2.0))) :
            head = self.oracle.objs[str(2 * i)]
            tail = self.oracle.objs[str(2 * i + 1)]
            for msg in msgs.get(head.name, []) :
                # print(msg.key, msg.value, head.amoe_pos, tail.amoe_pos)
                if msg.key == "expand" :
                    target_amoe_pos = array(head.amoe_pos) + array(msg.value)
                    if head.amoe_pos == tail.amoe_pos and len(self.oracle.objs_at_amoe_pos(target_amoe_pos)) < 1:
                        self.oracle.move_amoe_obj(head.name, target_amoe_pos)
                elif msg.key == "contract" :
                    if msg.value == "head" :
                        self.oracle.move_amoe_obj(tail.name, head.amoe_pos)
                    elif msg.value == "tail" :
                        self.oracle.move_amoe_obj(head.name, tail.amoe_pos)
                # print(head.amoe_pos, tail.amoe_pos)

            self.resp.add_msg(Message(dest = head.name, key = "head_amoe_pos", value = tuple(head.amoe_pos)))
            self.resp.add_msg(Message(dest = head.name, key = "tail_amoe_pos", value = tuple(tail.amoe_pos)))
            head_detect = []
            tail_detect = []
            for port in [(1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0)] :
                if len(self.oracle.objs_at_amoe_pos(array(head.amoe_pos) + array(port))) > 0 :
                    head_detect.append(port)
                if len(self.oracle.objs_at_amoe_pos(array(tail.amoe_pos) + array(port))) > 0 :
                    tail_detect.append(port)
            self.resp.add_msg(Message(dest = head.name, key = "head_detect", value = head_detect))
            self.resp.add_msg(Message(dest = head.name, key = "tail_detect", value = tail_detect))

        return self.resp

    def draw(self, screen) :
        (width, height) = screen.get_size()

        # draw the grids

        grid_line_color = THECOLORS["lightgray"]

        unit = 2 * amoebot_radius *  math.cos(math.pi / 6.0)

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


        distance = pldist_l2((-width / 2.0, height / 2.0), (0, 0), pq_to_xy((0, 1)))
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

        super(AmoeContext, self).draw(screen)


class AmoeDetectModule(Module) :
    def sense(self, reqt) :
        agent_name = self.mem.read("name", None)
        for msg in reqt.get_msgs(agent_name) :
            if msg.key == "head_amoe_pos" :
                self.mem.reg(key = "head_amoe_pos", value = msg.value)
            elif msg.key == "tail_amoe_pos" :
                self.mem.reg(key = "tail_amoe_pos", value = msg.value)
            elif msg.key == "head_detect" :
                self.mem.reg(key = "head_detect", value = msg.value)
            elif msg.key == "tail_detect" :
                self.mem.reg(key = "tail_detect", value = msg.value)
        # print("head_detect", self.mem.read("head_detect"))
        # print("tail_detect", self.mem.read("tail_detect"))


class AmoeMoveModule(Module) :
    def act(self, resp) :
        contract_value = self.mem.read("contract", None)
        if contract_value is not None and contract_value in ["head", "tail"]:
            resp.add_msg(Message(key = "contract", value = contract_value))
        else :
            expand_value = self.mem.read("expand", None)
            if expand_value is not None and check_attrs(expand_value, {"__getitem__" : None, "__len__" : None}) and len(expand_value) >= 2 :
                resp.add_msg(Message(key = "expand", value = expand_value))
        self.mem.reg(key = "contract", value = None)
        self.mem.reg(key = "expand", value = None)


class AmoeProcessModule(Module) :
    def process(self) :
        agent_name = self.mem.read("name", None)
        head_amoe_pos = self.mem.read("head_amoe_pos", None)
        tail_amoe_pos = self.mem.read("tail_amoe_pos", None)
        head_detect = self.mem.read("head_detect", [])
        tail_detect = self.mem.read("tail_detect", [])
        # print("head_detect:", head_detect)
        # print("tail_detect:", tail_detect)
        if head_amoe_pos is not None and tail_amoe_pos is not None :
            head_ports = [(1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0)]
            for port in head_detect :
                if port in head_ports :
                    del(head_ports[head_ports.index(port)])
            if head_amoe_pos == tail_amoe_pos :
                if len(head_ports) > 0 :
                    if random.random() < 0.5 :
                        self.mem.reg(key = "expand", value = random.choice(head_ports))
                        # print("port:", self.mem.read("expand"))
            else :
                if random.random() < 0.5 :
                    self.mem.reg(key = "contract", value = "head")
                else :
                    self.mem.reg(key = "contract", value = "tail")


class AmoeFocusAgent(Agent) :
    @property
    def focus(self) :
        focus_info = {
        }

        head_amoe_pos = self.mem.read("head_amoe_pos", None)
        if head_amoe_pos is not None :
            focus_info["head_amoe_pos"] =  "(%4.2f, %4.2f)" % (head_amoe_pos[0], head_amoe_pos[1]),

        tail_amoe_pos = self.mem.read("tail_amoe_pos", None)
        if tail_amoe_pos is not None :
            focus_info["tail_amoe_pos"] =  "(%4.2f, %4.2f)" % (tail_amoe_pos[0], tail_amoe_pos[1]),

        return focus_info


class AmoeStaticAgent(AmoeFocusAgent) :
    def __init__(self, name) :
        super(AmoeStaticAgent, self).__init__(name)
        self.config(mods = [])


class AmoeDynamicAgent(AmoeFocusAgent) :
    def __init__(self, name) :
        super(AmoeDynamicAgent, self).__init__(name)
        self.config(mods = [AmoeDetectModule(), AmoeMoveModule(), AmoeProcessModule()])


def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the oracle space

    oracle = AmoeOracleSpace()

    # create the context

    context = AmoeContext(oracle = oracle)

    # create the schedule for adding agents in the running

    schedule = Schedule()

    # add objects and agents to the context

    row = 5
    col = 5
    for i in range(col) :
        for j in range(row) :
            k = i * row + j
            # the (2 * k)-th object is coupled with the (2 * k + 1)-th object, i.e. 0 is coupled with 1, 4 is coupled with 5.
            amoe_pos = (4 * i - 2 * (col - 1) + 2 * ((row - 1)/ 2 - j), 4 * j - 2 * (row - 1))

            obj = AmoeObject(name = str(2 * k))
            obj.amoe_pos = amoe_pos
            context.add_obj(obj)

            if i == (col - 1) / 2 and j == (row - 1) / 2:
                schedule.add_agent(AmoeDynamicAgent(name = str(2 * k)))
            else :
                schedule.add_agent(AmoeStaticAgent(name = str(2 * k)))

            obj = AmoeObject(name = str(2 * k + 1))
            obj.amoe_pos = amoe_pos
            context.add_obj(obj)
            schedule.add_agent(AmoeFocusAgent(name = str(2 * k + 1)))

    # create the driver

    driver = Driver(context = context, schedule = schedule)

    # create the inspector

    inspector = Inspector(delay = 10)

    # create the simulator

    sim = Simulator(driver = driver)

    print("Simulating")
    sim.simulate(graphics = True, inspector = inspector, filename = filename)

if __name__ == '__main__' :
    filename = None
    if (len(sys.argv) > 1) :
        filename = sys.argv[1]
    run_sim(filename)
