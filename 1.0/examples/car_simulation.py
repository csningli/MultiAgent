
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
        force = 10.0
        index = 0
        timer_value = msg.get("timer_value", None)
        pos_x = msg.get("pos_x", None)
        pos_y = msg.get("pos_y", None)
        vel_x = msg.get("vel_x", None)
        vel_y = msg.get("vel_y", None)
        if None not in [timer_value, pos_x, pos_y, vel_x, vel_y] :
            index = int(math.floor(timer_value / 10.0)) % 4 
            pos_x = msg.get("pos_x", None)
            pos_y = msg.get("pos_y", None)
            vec = (self.targets[index][0] - float(pos_x), self.targets[index][1] - float(pos_y))
            norm = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
            if norm > 0.1 :
                self.result["local"]["forces"] = (vec[0] * force, vec[1] * force)
        return self.result

class CarObject(Object) :
    def __init__(self, name) :
        mods = [CarProcessModule(), MotionModule(), TimeSensorModule(), PositionSensorModule(), AngleSensorModule(), VelocitySensorModule(), AngularVelSensorModule(), CommunicateModule()]
        super(CarObject, self).__init__(name = name, mods = mods)

    def step(self, obj_data = None) :
        super(CarObject, self).step(obj_data = obj_data)
        self.info("Object %s's status: %s" % (self.name, self.status))

class CarContext(Context) :
    def draw(self, screen, font) :
        super(CarContext, self).draw(screen, font)

        # draw the name above each unit
        
        for unit in self.units.values() :
            if unit.shape is not None :
                r = unit.shape.get_range()
                p = unit.get_position()
                (width, height) = screen.get_size()
                p[0] = int(width / 2.0 + p[0] - 5.0) 
                p[1] = int(height / 2.0 - p[1] - r[1] - 10.0) 
                screen.blit(font.render(unit.name, 1, THECOLORS["black"]), p)
 
 
car_objects = []
car_units = []

patrol_car = CarObject(name = "0")
patrol_unit = Unit(name = patrol_car.name)
patrol_unit.set_position((0.0, 0.0))

car_objects.append(patrol_car)
car_units.append(patrol_unit)
    
car_context = CarContext(delta = 1.0 / 50.0, units = car_units)
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
    
