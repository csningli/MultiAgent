
import sys, os, time, math

sys.path.append("../py")

from multiagent import * 

class CarProcessModule(Module) :
    targets = [
        (100.0, -100.0), 
        (100.0, 100.0), 
        (-100.0, 100.0), 
        (-100.0, -100.0), 
    ] 
    def perform(self, msg, ram) :
        self.result["local"] = {}
        self.result["post"] = {}
        vel = 30.0
        avel = 1.0
        index = 0
        timer_value = msg.get("timer_value", None)
        if None not in [timer_value, ] :
            index = int(math.floor(timer_value / 10.0)) % 4 
            self.result["local"]["moves"] = (self.targets[index][0], self.targets[index][1], vel, avel)
        return self.result

class CarObject(Object) :
    def __init__(self, name) :
        mods = [CarProcessModule(), MotionModule(), DriveModule(), TimeSensorModule(), MassSensorModule(), PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(), AngularVelSensorModule(), CommunicateModule()]
        super(CarObject, self).__init__(name = name, mods = mods)

    def step(self, obj_data = None) :
        super(CarObject, self).step(obj_data = obj_data)
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
    
