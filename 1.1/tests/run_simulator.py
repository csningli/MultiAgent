#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("../py")

from multiagent import * 

def run_sim() :
    '''
    >>> run_sim()
    '''
    context = Context()

    obj = Object(name = "0")
    obj.pos = (-20, 0)
    context.add_obj(obj)
    obj = Object(name = "1")
    obj.pos = (-40, 0)
    context.add_obj(obj)
    context.add_obt(Obstacle(name ="0", a = (0.0, 10.0), b = (10.0, 0.0), radius = 2.0))

    schedule = Schedule()
    schedule.add_agent(Agent(name = "0"))
    schedule.add_agent(agent = Agent(name = "1"), delay = 30)
    driver = Driver(context = context, schedule = schedule)
    sim = Simulator(driver = driver)
    print("Simulate")
    sim.simulate(graphics = True)



if __name__ == '__main__' :
    run_sim()



