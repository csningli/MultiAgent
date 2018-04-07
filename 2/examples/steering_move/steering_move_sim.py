
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, random, datetime, math
random.seed(datetime.datetime.now())

sys.path.append("../../2.0/py")

from multiagent import *
from utils import *

class SteeringObject(Object) :
    def __init__(self, name, mass = 1.0, radius = 10.0) :
        super(SteeringObject, self).__init__(name, mass, radius)
        self.__label = self.name

    @property
    def label(self) :
        return self.__label

    @label.setter
    def label(self, value) :
        self.__label = value


class SteeringContext(Context) :
    def handle_reqt(self, reqt) :
        resp = super(SteeringContext, self).handle_reqt(reqt)
        return self.resp

    def draw(self, screen) :
        super(SteeringContext, self).draw(screen)


def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the oracle space

    oracle = OracleSpace()

    # create the context

    context = SteeringContext(oracle = oracle)

    # create the schedule for adding agents in the running

    schedule = Schedule()

    # add objects and agents to the context

    obj = SteeringObject(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)
    schedule.add_agent(Agent(name = "0"))

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
    run_sim(filename)
