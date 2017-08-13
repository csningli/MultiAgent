
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
        mods = [CarProcessModule(), ForceModule(), SpinModule(), MoveModule(), TimeSensorModule(), MassSensorModule(), PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(), AngularVelSensorModule(), TransmitModule(), ListenModule()]
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
                    p[0] = int(width / 2.0 + p[0] - 5.0) 
                    p[1] = int(height / 2.0 - p[1] - r[1] - 10.0) 
                    screen.blit(font.render(unit.name, 1, THECOLORS["black"]), p)
 
 
car_objects = []
car_units = []
scene_units = []

wall = Unit(name = "wall", shape = SegmentShape((0, -50), (200, -50)))
scene_units.append(wall)

patrol_car = CarObject(name = "0")
patrol_unit = Unit(name = patrol_car.name)
patrol_unit.set_position((0.0, 0.0))

car_objects.append(patrol_car)
car_units.append(patrol_unit)
    
car_context = CarContext(delta = 1.0 / 50.0, units = car_units + scene_units)
car_driver = Driver(context = car_context, objects = car_objects, data = Data())
car_simulator = Simulator(driver = car_driver)

@test_func
def test_simulator() :
    car_simulator.simulate(steps = None, inspector = None, graphics = True)
    data = car_simulator.driver.data
    if data is not None : 
        data.to_file()
    
if __name__ == '__main__' :
    test_simulator()
    
