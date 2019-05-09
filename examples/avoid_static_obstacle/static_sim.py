
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys

sys.path.append("../../2.0/")

from mas.multiagent import *
from mas.extension import ShowLabelObject


class DetectAgent(Agent) :
    def __init__(self, name) :
        super(DetectAgent, self).__init__(name)
        self.mods = [RadarModule(), ]

    @property
    def focus(self) :
        focus_info = {
        }

        detect = self.mem.read("radar_detect", None)
        for i, block in enumerate(detect) :
            focus_info["block_%d" % i] =  "%s" % block

        if len(focus_info) < 1 :
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

    obj = ShowLabelObject(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)
    schedule.add_agent(DetectAgent(name = "0"))

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
