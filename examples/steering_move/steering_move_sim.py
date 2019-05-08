
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, random, datetime, math
random.seed(datetime.datetime.now())


sys.path.append("../..")
from mas.multiagent import *
from mas.extension import ShowLabelObject


AREA_SIZE = 200
POS_ERROR = 10
MIN_SPEED = 10
MAX_SPEED = 500
ANGLE_ERROR = math.pi / 36.0
MIN_ASPEED = math.pi / 36.0
MAX_ASPEED = math.pi / 6.0
FRICTION_FACTOR = 0.2


def turn_vel(v, f) :
    turn = vec2_rotate(v, HALF_PI)
    length = vec2_length(turn)
    if length > NON_ZERO_LOWER_BOUND :
        turn = vec2_scale(turn, f / length)
    return vec2_add(v, turn)


class RandomTargetModule(Module) :
    def process(self) :
        pos = self.mem.read("pos", None)
        target = self.mem.read("target", None)
        if pos is not None and (target is None or ppdist_l2(target, pos) <= POS_ERROR) :
            if target is not None :
                finishes = self.mem.read("finishes", None)
                if finishes is not None :
                    self.mem.reg("finishes", finishes + 1)
                else :
                    self.mem.reg("finishes", 1)
            self.mem.reg("target", (math.floor(random.random() * AREA_SIZE), math.floor(random.random() * AREA_SIZE)))


class SteeringMoveModule(ObjectModule) :
    def act(self, resp) :
        target = self.mem.read("target", None)
        if target is not None :
            pos = self.mem.read("pos", None)
            vel = self.mem.read("vel", None)
            angle = self.mem.read("angle", None)
            if pos is not None and vel is not None and angle is not None :
                pos_diff = vec2_sub(target, pos)
                if vec2_length(pos_diff) > POS_ERROR :
                    target_angle = vec2_angle(pos_diff)
                    angle_diff = target_angle - angle
                    if angle_diff > math.pi :
                        angle_diff = angle_diff - 2 * math.pi
                    if angle_diff < - math.pi :
                        angle_diff = angle_diff + 2 * math.pi
                    target_vel = (math.cos(angle), math.sin(angle))
                    if abs(angle_diff) <= ANGLE_ERROR :
                        target_vel = vec2_scale(target_vel, min_max_bound(vec2_length(pos_diff) * 3, MIN_SPEED, MAX_SPEED))
                    else :
                        sign = angle_diff / abs(angle_diff)
                        target_avel = sign * min_max_bound(abs(angle_diff), MIN_ASPEED, MAX_ASPEED)
                        resp.add_msg(Message(key = "avel", value = target_avel))
                        target_vel = vec2_scale(target_vel, (1.0 - FRICTION_FACTOR) * max(MIN_SPEED, vec2_length(vel)))
                        target_vel = turn_vel(target_vel, target_avel)

                    resp.add_msg(Message(key = "vel", value = target_vel))

        super(SteeringMoveModule, self).act(resp)


class SteeringAgent(Agent) :
    def __init__(self, name) :
        super(SteeringAgent, self).__init__(name)
        self.mods = [SteeringMoveModule(), RandomTargetModule()]

    @property
    def focus(self) :
        focus_info = {}

        target = self.mem.read("target", None)
        if target is not None :
            focus_info["target"] =  "(%4.2f, %4.2f)" % (target[0], target[1])

        pos = self.mem.read("pos", None)
        if pos is not None :
            focus_info["pos"] =  "(%4.2f, %4.2f)" % (pos[0], pos[1])

        finishes = self.mem.read("finishes", None)
        if finishes is not None :
            focus_info["finishes"] =  "%d" % finishes

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
