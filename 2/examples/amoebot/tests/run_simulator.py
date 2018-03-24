#! /Users/nil/anaconda3/envs/multiagent_2/bin/python

# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time
import doctest

sys.path.append("..")
sys.path.append("../../../2.0/py")

from multiagent import * 
from amoebot import * 

def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the context
    
    context = AmoeContext()

    # add an object to the context

    obj = Object(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)
    obj = Object(name = "1")
    obj.pos = (0, 0)
    context.add_obj(obj)

    # create the schedule for adding objects/obstacles/agents in the running   

    schedule = Schedule()
   
    # add an agent to existing object

    schedule.add_agent(Agent(name = "0"))

    # add a new object and an new agent accordingly 

    #obj = Object(name = "1")
    #obj.pos = (-10, 0)
    #schedule.add_obj(obj, 30)

    #schedule.add_agent(agent = Agent(name = "1"), delay = 30)

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



