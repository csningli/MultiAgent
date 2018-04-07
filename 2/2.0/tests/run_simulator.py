
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import *

def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the context

    context = Context()

    # add an object to the context

    obj = Object(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)

    # add obstacles

    context.add_obt(Obstacle(name ="0", a = (0.0, 200.0), b = (200.0, 0.0), radius = 2.0))
    context.add_obt(Obstacle(name ="1", a = (0.0, 200.0), b = (-200.0, 0.0), radius = 2.0))
    context.add_obt(Obstacle(name ="2", a = (0.0, -200.0), b = (200.0, 0.0), radius = 2.0))
    context.add_obt(Obstacle(name ="3", a = (0.0, -200.0), b = (-200.0, 0.0), radius = 2.0))

    # create the schedule for adding objects/obstacles/agents in the running

    schedule = Schedule()

    # add an agent to existing object

    schedule.add_agent(Agent(name = "0"))

    # add a new object and an new agent accordingly

    obj = Object(name = "1")
    obj.pos = (-10, 0)
    schedule.add_obj(obj, 30)

    schedule.add_agent(agent = Agent(name = "1"), delay = 30)

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
