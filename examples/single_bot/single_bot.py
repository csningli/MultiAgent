
import sys, os, time, math, random

sys.path.append("../../py")

from multiagent import Driver, Simulator, Module, Data, Zipper, Player, test_func
from amoebot import *

class BotProcessModule(Module) :
    sleep = 10
    choices = [(1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0)]
    def perform(self, msg, ram) :
        super(BotProcessModule, self).perform(msg = msg, ram = ram)
        expanded = self.get_from_ram(ram = ram, symbol = ".expanded")
        delay = self.get_from_ram(ram = ram, symbol = ".delay")
        if None not in [expanded, delay] : 
            neighbors = self.get_from_msg(msg = msg, symbol = "neighbor")
            if neighbors is not None and len(neighbors) > 0 :
                for neighbor in neighbors :
                    neighbor_pos = neighbor[0][0]
                    self.inform_module(symbol = "share", value = (neighbor_pos, "oops")) 
            if delay > 0 :
                delay -= 1
            else :
                if expanded :
                    self.inform_module(symbol = "contract", value = "head")
                else :
                    self.inform_module(symbol = "expand", value = random.choice(self.choices))
                self.put_to_ram(ram = ram, symbol = ".expanded", value = not expanded)
                delay = 10
            self.put_to_ram(ram = ram, symbol = ".delay", value = delay)
            self.activate_sensors(symbols = ["time", "neighbor", "head_pos", "tail_pos"])
        return self.result

objects = []
units = []
for i in range(5) :
    name = str(i)
    mods = [BotProcessModule()]
    if i < 1 :
        mods += [ExpandModule(), ContractModule(), NeighborModule(), ShareModule()]
    obj = AmoebotObject(name = name, mods = mods)
    obj.put_to_mem(symbol = ".expanded", value = False)
    obj.put_to_mem(symbol = ".delay", value = 0)
    objects.append(obj)
    unit = AmoebotUnit(name = name)
    units.append(unit)
        
units[0].set_head_pos((0.0, 0.0))
units[0].set_tail_pos((0.0, 0.0))
units[1].set_head_pos((2.0, 0.0))
units[1].set_tail_pos((2.0, 0.0))
units[2].set_head_pos((-2.0, 0.0))
units[2].set_tail_pos((-2.0, 0.0))
units[3].set_head_pos((0.0, 2.0))
units[3].set_tail_pos((0.0, 2.0))
units[4].set_head_pos((0.0, -2.0))
units[4].set_tail_pos((0.0, -2.0))

context = AmoebotContext(delta = 1.0 / 50.0, units = units)

@test_func()
def simulate(filename = None) :
    driver = Driver(aggr = AmoebotAggregator(), context = context, objects = objects, data = Data())
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
    
