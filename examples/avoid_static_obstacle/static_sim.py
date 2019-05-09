
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, math

sys.path.append("../..")

from mas.multiagent import *
from mas.extension import ShowLabelObject

POS_ERROR = 5
SPIN_SPEED = math.pi / 6.0

class SpinModule(ObjectModule) :
    def act(self, resp) :
        resp.add_msg(Message(key = "avel", value = SPIN_SPEED))

        super(SpinModule, self).act(resp)

class AvoidObstacleAgent(Agent) :
    def __init__(self, name) :
        super(AvoidObstacleAgent, self).__init__(name)
        self.mods = [RadarModule(), SpinModule()]

    def get_focus(self) :
        focus_info = super(AvoidObstacleAgent, self).get_focus()

        pos = self.mem.read("pos", None)
        detect = self.mem.read("radar_detect", None)
        if detect is not None :
            for i, block in enumerate(detect) :
                if pos is None or abs(block[2] - pos[0]) > POS_ERROR or abs(block[3] - pos[1]) > POS_ERROR :
                    focus_info["block_%d" % i] =  "(%.1f, %.1f)" % (block[2], block[3])
        else :
            focus_info["detect"] = "none"

        return focus_info


def run_sim(filename = None) :
    '''
    run_sim(filename = None)
    ------------------------
    filename : the name of the file to save the data; None by default.
    '''

    # create the oracle space

    oracle = OracleSpace()

    # create the context

    context = Context(oracle = oracle)

    # create the schedule for adding agents in the running

    schedule = Schedule()

    # add objects and agents to the context

    obt = Obstacle(name ="0", a = (50.0, -50.0), b = (50.0, 50.0), radius = 2.0)
    context.add_obt(obt)

    obj = ShowLabelObject(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)

    agent = AvoidObstacleAgent(name = "0")
    agent.mem.reg("radar_dist", 100.0)
    schedule.add_agent(agent)

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
