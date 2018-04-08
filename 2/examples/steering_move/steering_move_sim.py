
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, random, datetime, math
random.seed(datetime.datetime.now())

sys.path.append("../../2.0/py")

from numpy import array

from multiagent import *
from utils import *

class SteeringObject(Object) :
    def __init__(self, name, mass = 1.0, radius = 10.0) :
        super(SteeringObject, self).__init__(name, mass, radius)
        self.__label = self.name

    @property
    def label(self) :
        return self.__label

    @label.setter
    def label(self, value) :
        self.__label = value

    def draw(self, screen) :
        super(SteeringObject, self).draw(screen)
        if self.visible == True :
            font = pygame.font.Font(None, 16)
            (width, height) = screen.get_size()
            pos_draw = (int(width / 2.0 + self.pos[0] - 5.0), int(height / 2.0 - self.pos[1] - self.radius - 10.0))
            screen.blit(font.render(self.label, 1, THECOLORS["black"]), pos_draw)

class SteeringProcessModule(Module) :
    def process(self) :
        pos = self.mem.read("pos", None)
        target = self.mem.read("target", None)
        if pos is not None and (target is None or ppdist_l2(target, pos) < 5) :
            self.mem.reg("target", (math.floor(random.random() * 200), math.floor(random.random() * 200)))


class SteeringMoveModule(ObjectModule) :
    def act(self, resp) :
        target = self.mem.read("target", None)
        if target is not None :
            pos = self.mem.read("pos", None)
            vel = self.mem.read("vel", None)
            angle = self.mem.read("angle", None)
            if pos is not None and vel is not None and angle is not None :
                vel_target = (target[0] - pos[0], target[1] - pos[1])
                speed_target = norm(array(vel_target))
                if speed_target > 0.001 :
                    angle_target = math.acos(vel_target[0] / speed_target)
                    if vel_target[1] <  0 :
                        angle_target = - angle_target + 2 * math.pi

                    avel_perform = angle_target - angle
                    if abs(avel_perform) > 0.01 :
                        if abs(avel_perform) < 0.5 :
                            resp.add_msg(Message(key = "angle", value = angle_target))
                        else :
                            if avel_perform > 0 :
                                avel_perform = max(0.001, avel_perform)
                            else :
                                avel_perform = min(-0.001, avel_perform)
                            resp.add_msg(Message(key = "avel", value = avel_perform))
                            speed_target = min(1, norm(array(vel)))

                    vel_perform = (math.cos(angle) * speed_target, math.sin(angle) * speed_target)
                    resp.add_msg(Message(key = "vel", value = vel_perform))

        super(SteeringMoveModule, self).act(resp)


class SteeringAgent(Agent) :
    def __init__(self, name) :
        super(SteeringAgent, self).__init__(name)
        self.config(mods = [SteeringMoveModule(), SteeringProcessModule()])

    @property
    def focus(self) :
        focus_info = {
        }

        target = self.mem.read("target", None)
        if target is not None :
            focus_info["target"] =  "(%4.2f, %4.2f)" % (target[0], target[1])

        pos = self.mem.read("pos", None)
        if pos is not None :
            focus_info["pos"] =  "(%4.2f, %4.2f)" % (pos[0], pos[1])

        return focus_info


def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the oracle space

    oracle = OracleSpace()

    # create the context

    context = Context(oracle = oracle)

    # create the schedule for adding agents in the running

    schedule = Schedule()

    # add objects and agents to the context

    obj = SteeringObject(name = "0")
    obj.pos = (0, 0)
    context.add_obj(obj)
    schedule.add_agent(SteeringAgent(name = "0"))

    # create the driver

    driver = Driver(context = context, schedule = schedule)

    # create the inspector

    # inspector = Inspector(delay = 10)

    # create the simulator

    sim = Simulator(driver = driver)

    print("Simulating")
    sim.simulate(graphics = True, filename = filename)


if __name__ == '__main__' :
    filename = None
    if (len(sys.argv) > 1) :
        filename = sys.argv[1]
    run_sim(filename)
