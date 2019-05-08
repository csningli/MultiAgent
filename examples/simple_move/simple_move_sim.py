
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, random, datetime, math
random.seed(datetime.datetime.now())

sys.path.append("../..")
from mas.multiagent import *


AREA_SIZE = 200
POS_ERROR = 5
MIN_SPEED = 100
MAX_SPEED = 500

class TargetModule(Module) :
    def __init__(self) :
        super(TargetModule, self).__init__()
        self.index = 0
        self.targets = [
            (100, 0), (100, 100),
            (0, 100), (-100, 100),
            (-100, 0), (-100, -100),
            (0, -100), (100, -100),
        ]

    def process(self) :
        pos = self.mem.read("pos", None)
        target = self.mem.read("target", None)
        if pos is not None and (target is None or ppdist_l2(target, pos) <= POS_ERROR) :
            self.mem.reg("target", self.targets[self.index])
            self.index = (self.index + 1) % len(self.targets)


class SimpleMoveModule(ObjectModule) :
    def act(self, resp) :
        target = self.mem.read("target", None)
        pos = self.mem.read("pos", None)
        if target is not None and pos is not None:
            diff = vec2_sub(target, pos)
            resp.add_msg(Message(key = "angle", value = vec2_angle(diff)))
            resp.add_msg(Message(key = "vel", value = vec2_min_max(vec2_scale(diff, 3), MIN_SPEED, MAX_SPEED)))

        super(SimpleMoveModule, self).act(resp)


class SimpleMoveAgent(Agent) :
    def __init__(self, name) :
        super(SimpleMoveAgent, self).__init__(name)
        self.mods = [SimpleMoveModule(), TargetModule()]

    def focus(self) :
        focus_info = super(SimpleMoveAgent, self).get_focus() 

        target = self.mem.read("target", None)
        if target is not None :
            focus_info["target"] =  "(%4.2f, %4.2f)" % (target[0], target[1])

        pos = self.mem.read("pos", None)
        if pos is not None :
            focus_info["pos"] =  "(%4.2f, %4.2f)" % (pos[0], pos[1])

        return focus_info


def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the oracle space

    oracle = OracleSpace()

    # create the context

    context = Context(oracle = oracle)

    # create the schedule for adding agents in the running

    schedule = Schedule()

    # add objects and agents to the context

    obj = Object(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)
    schedule.add_agent(SimpleMoveAgent(name = "0"))

    # create the driver

    driver = Driver(context = context, schedule = schedule)

    # create the inspector

    # inspector = Inspector(delay = 10)

    # create the simulator

    sim = Simulator(driver = driver)

    print("Simulating")
    sim.simulate(graphics = True, filename = filename)


if __name__ == '__main__' :
    filename = None
    if (len(sys.argv) > 1) :
        filename = sys.argv[1]
    run_sim(filename = filename)
