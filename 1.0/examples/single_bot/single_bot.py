
import sys, os, time, math

sys.path.append("../../py")

from multiagent import Driver, Simulator, Data, test_func
from amoebot import AmoebotObject, AmoebotUnit, AmoebotContext 

objects = []
obj = AmoebotObject(name = "0", mods = [])
objects.append(obj)

units = []
unit = AmoebotUnit(name = obj.name)
unit.set_head_pos((0.0, 0.0))
unit.set_tail_pos((0.0, 0.0))
units.append(unit)

context = AmoebotContext(delta = 1.0 / 50.0, units = units)

@test_func()
def simulate(filename = None) :
    driver = Driver(context = context, objects = objects, data = Data())
    simulator = Simulator(driver = driver)
    simulator.simulate(steps = None, inspector = None, graphics = True)
    data = simulator.driver.data
    if data is not None : 
        if filename is not None :
            filename = data.to_file(filename)
        else :
            filename = data.to_file()

@test_func()
def play(filename) :
    data = Data()
    data.from_file(filename)
  
    zipper = Zipper(data = data, context = context, objects = objects)
    player = Player(zipper = zipper)
    player.play(steps = None, inspector = None, graphics = True)
    
    
if __name__ == '__main__' :
    usage = "Usage: python single_bot.py [simulate/play] [.data]"
    if len(sys.argv) < 2 :
        print(usage)
        exit(1)
        
    filename = None
    if len(sys.argv) > 2 :
        filename = sys.argv[2]
    if sys.argv[1] == "simulate" : 
        simulate(filename)
    elif sys.argv[1] == "play" :
        if filename is not None :
            play(filename)
        else :
            print("[.data] is invalid: %s" % filename)
            print(usage)
            exit(1)
    
