
import sys, os, time, math, random

sys.path.append("../../py")

from multiagent import Driver, Simulator, Module, Data, Zipper, Player, test_func
from amoebot import AmoebotObject, AmoebotUnit, AmoebotContext, AmoebotAggregator, ExpandModule, ContractModule

class BotProcessModule(Module) :
    delay = 10
    choices = [(1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0)]
    expanded = False
    def perform(self, msg, ram) :
        super(BotProcessModule, self).perform(msg = msg, ram = ram)
        if self.delay > 0 :
            self.delay -= 1
        else :
            if self.expanded :
                self.inform_module(symbol = "contract", value = "head")
            else :
                self.inform_module(symbol = "expand", value = random.choice(self.choices))
            self.expanded = not self.expanded
            self.delay = 10
        #self.activate_sensors(symbols = ["time", "listen"])
        return self.result

objects = []
obj = AmoebotObject(name = "0", mods = [BotProcessModule(), ExpandModule(), ContractModule()])
objects.append(obj)
obj1 = AmoebotObject(name = "1", mods = [])
objects.append(obj1)
obj2 = AmoebotObject(name = "2", mods = [])
objects.append(obj2)
obj3 = AmoebotObject(name = "3", mods = [])
objects.append(obj3)
obj4 = AmoebotObject(name = "4", mods = [])
objects.append(obj4)

units = []
unit = AmoebotUnit(name = obj.name)
unit.set_head_pos((0.0, 0.0))
unit.set_tail_pos((0.0, 0.0))
units.append(unit)

unit1 = AmoebotUnit(name = obj1.name)
unit1.set_head_pos((2.0, 0.0))
unit1.set_tail_pos((2.0, 0.0))
units.append(unit1)

unit2 = AmoebotUnit(name = obj2.name)
unit2.set_head_pos((-2.0, 0.0))
unit2.set_tail_pos((-2.0, 0.0))
units.append(unit2)

unit3 = AmoebotUnit(name = obj3.name)
unit3.set_head_pos((0.0, 2.0))
unit3.set_tail_pos((0.0, 2.0))
units.append(unit3)

unit4 = AmoebotUnit(name = obj4.name)
unit4.set_head_pos((0.0, -2.0))
unit4.set_tail_pos((0.0, -2.0))
units.append(unit4)

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
    
