
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, random, datetime, math
random.seed(datetime.datetime.now())


sys.path.append("../..")
from mas.multiagent import *
from mas.extension import ShowLabelObject


AREA_LENGTH = 200
POS_ERROR = 10
ANGLE_ERROR = 0.1
MIN_SPEED = 5
MAX_SPEED = 100


class SteeringProcessModule(Module) :
    def process(self) :
        pos = self.mem.read("pos", None)
        target = self.mem.read("target", None)
        if pos is not None and (target is None or ppdist_l2(target, pos) <= POS_ERROR) :
            self.mem.reg("target", (math.floor(random.random() * AREA_LENGTH), math.floor(random.random() * AREA_LENGTH)))


class SteeringMoveModule(ObjectModule) :
    def act(self, resp) :
        target = self.mem.read("target", None)
        if target is not None :
            pos = self.mem.read("pos", None)
            vel = self.mem.read("vel", None)
            angle = self.mem.read("angle", None)
            if pos is not None and vel is not None and angle is not None :
                pos_diff = vec2_sub(target, pos)
                if vec2_norm(pos_diff) > POS_ERROR :
                    target_angle = vec2_angle(pos_diff)
                    angle_diff = target_angle - angle

                    target_vel = (math.cos(angle), math.sin(angle))
                    if abs(angle_diff) <= ANGLE_ERROR :
                        target_vel = vec2_scale(target_vel, min_max_bound(norm(array(pos_diff)), MIN_SPEED, MAX_SPEED))
                    else :
                        target_avel = ANGLE_ERROR * angle_diff / abs(angle_diff)
                        print("target_avel:", target_avel)
                        resp.add_msg(Message(key = "avel", value = target_avel))
                        target_vel = vec2_turn(vec2_scale(target_vel, vec2_norm(vel)), target_avel)

                    print("target_vel:", target_vel)
                    resp.add_msg(Message(key = "vel", value = target_vel))

        super(SteeringMoveModule, self).act(resp)


class SteeringAgent(Agent) :
    def __init__(self, name) :
        super(SteeringAgent, self).__init__(name)
        self.mods = [SteeringMoveModule(), SteeringProcessModule()]

    @property
    def focus(self) :
        focus_info = {}

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

    obj = ShowLabelObject(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)
    schedule.add_agent(SteeringAgent(name = "0"))

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
