
import sys, os, time, math

sys.path.append("../../py")

from multiagent import * 

class CarProcessModule(Module) :

    targets = [
        (100.0, -100.0), 
        (100.0, 100.0), 
        (-100.0, 100.0), 
        (-100.0, -100.0), 
    ] 
    
    def perform(self, msg, ram) :
        super(CarProcessModule, self).perform(msg = msg, ram = ram)
        vel = 30.0
        avel = 1.0
        index = 0
        time_value = self.get_from_msg(msg = msg, symbol = "time")
        if None not in [time_value, ] :
            index = int(math.floor(time_value / 10.0)) % 4 
            self.inform_module(symbol = "move", value = (self.targets[index][0], self.targets[index][1], vel, avel))

        self.activate_sensors(symbols = ["time", "listen"])
        return self.result


class CarObject(Object) :
    def __init__(self, name) :
        mods = [
                CarProcessModule(), ForceModule(), SetAVelModule(), 
                MoveModule(), TimeSensorModule(), MassSensorModule(), 
                PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(),
                AngularVelSensorModule(), TransmitModule(), ListenModule(),
        ]
        super(CarObject, self).__init__(name = name, mods = mods)

    def step(self) :
        super(CarObject, self).step()
        self.info("Object %s's status: %s" % (self.name, self.status))


class CarContext(Context) :
    def draw(self, screen) :
        super(CarContext, self).draw(screen)

        # draw the name above each unit
        
        font = pygame.font.Font(None, 16)
        for unit in self.units.values() :
            if unit.shape is not None :
                if unit.name.isdigit() :
                    r = unit.shape.get_range()
                    p = unit.get_position()
                    (width, height) = screen.get_size()
                    p = (int(width / 2.0 + p[0] - 5.0), int(height / 2.0 - p[1] - r[1] - 10.0))
                    screen.blit(font.render(unit.name, 1, THECOLORS["black"]), p)
 

objects = []
patrol_car = CarObject(name = "0")
patrol_unit = Unit(name = patrol_car.name)
patrol_unit.set_position((0.0, 0.0))
objects.append(patrol_car)

units = []
units.append(patrol_unit)

scene_units = []
wall_west = Unit(name = "wall_west", shape = SegmentShape((-50, -10), (-50, 10)))
wall_east = Unit(name = "wall_east", shape = SegmentShape((50, -10), (50, 10)))
wall_north = Unit(name = "wall_north", shape = SegmentShape((-10, 50), (10, 50)))
wall_south = Unit(name = "wall_south", shape = SegmentShape((-10, -50), (10, -50)))
scene_units.append(wall_west)
scene_units.append(wall_east)
scene_units.append(wall_north)
scene_units.append(wall_south)
    
context = CarContext(delta = 1.0 / 50.0, units = units + scene_units)

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
    usage = "Usage: python patrol_car.py [simulate/play] [.data]"
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
    
