#! /Users/nil/anaconda3/envs/multiagent_2/bin/python

# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys

sys.path.append("../../2.0/py")

from multiagent import *
from utils import *

amoebot_radius = 10.0

def pq_to_xy(a) :
    b = array([0.0, 0.0])
    p = a[0]
    q = a[1]
    x = 2 * amoebot_radius * p + 2 * amoebot_radius *  math.cos(math.pi / 3.0) * q
    y = 2 * amoebot_radius *  math.cos(math.pi / 6.0) * q
    b[0] = x
    b[1] = y
    return b

def wq_to_xy(a) :
    b = array([0.0, 0.0])
    p = a[0]
    q = a[1]
    x = -2 * amoebot_radius * p -2 * amoebot_radius *  math.cos(math.pi / 3.0) * q
    y = 2 * amoebot_radius *  math.cos(math.pi / 6.0) * q
    b[0] = x
    b[1] = y
    return b

def xy_to_pq(b) :
    a = array([0.0, 0.0])
    x = b[0]
    y = b[1]
    q = int(float(y) / (2 * amoebot_radius *  math.cos(math.pi / 6.0)))
    p = int((float(x) -  2 * amoebot_radius *  math.cos(math.pi / 3.0) * q) / (2 * amoebot_radius)) - q
    a[0] = p
    a[1] = q
    return a


class AmoeObject(Object) :
    def draw(self, screen) :
        if self.visible == True :
            p = Vec2d(self.pos)
            rot = Vec2d(self.rot)
            r = self.radius
            (width, height) = screen.get_size()

            # adjust the drawing coordinates to make sure (0, 0) stays in the center

            p.x = int(width / 2.0 + p.x)
            p.y = int(height / 2.0 - p.y)

            head = Vec2d(rot.x, -rot.y) * self.radius * 0.9
            pygame.draw.circle(screen, self.stroke_color, p, int(r), 2)
            pygame.draw.circle(screen, self.fill_color, p, int(r/2.0), 4)


class AmoeOracleSpace(OracleSpace) :
    def add_obj(self, obj) :
        if check_attrs(obj, {
                "body" : None,
                "name" : None,
                "pos" : None,
                #"angle" : None,
                #"rot" : None,
                #"vel" : None,
                #"avel" : None,
                #"force" : None,
            }) and obj.name not in self.objs.keys() :
            self.objs[obj.name] = obj

    def add_obt(self, obt) :
        if check_attrs(obt, {
                "body" : None,
                "a" : None,
                "b" : None,
                "radius" : None,
            }) and obt.name not in self.obts.keys() :
            self.obts[obt.name] = obt

    def draw(self, screen) :
        # draw objs

        for obj in self.objs.values() + self.obts.values() :
            obj.draw(screen)

        # draw connection between the coupled objects

        # later


class AmoeContext(Context) :
    def draw(self, screen) :
        (width, height) = screen.get_size()

        # draw the grids

        grid_line_color = THECOLORS["lightgray"]

        unit = 2 * amoebot_radius *  math.cos(math.pi / 6.0)

        start = [0, height / 2]
        end = [width, height / 2]
        pygame.draw.line(screen, THECOLORS["gray"], start, end, 1)

        q_ceil = int(math.ceil((height / unit) / 2))
        for i in range(1, q_ceil) :
            start = [0, height / 2 + unit * i]
            end = [width, height / 2 + unit * i]
            pygame.draw.line(screen, THECOLORS["gray"], start, end, 1)
            start = [0, height / 2 - unit * i]
            end = [width, height / 2 - unit * i]
            pygame.draw.line(screen, THECOLORS["gray"], start, end, 1)


        distance = pldist_l2((-width / 2.0, height / 2.0), (0, 0), pq_to_xy((0, 1)))
        start = pq_to_xy((0, q_ceil))
        start[0] = int(width / 2.0 + start[0])
        start[1] = int(height / 2.0 - start[1])
        end = pq_to_xy((0, -q_ceil))
        end[0] = int(width / 2.0 + end[0])
        end[1] = int(height / 2.0 - end[1])
        pygame.draw.line(screen, grid_line_color, start, end, 1)
        start = wq_to_xy((0, q_ceil))
        start[0] = int(width / 2.0 + start[0])
        start[1] = int(height / 2.0 - start[1])
        end = wq_to_xy((0, -q_ceil))
        end[0] = int(width / 2.0 + end[0])
        end[1] = int(height / 2.0 - end[1])
        pygame.draw.line(screen, grid_line_color, start, end, 1)

        for i in range(1, int(1.5 * math.ceil(distance / unit))) :
            start = pq_to_xy((i, q_ceil))
            start[0] = int(width / 2.0 + start[0])
            start[1] = int(height / 2.0 - start[1])
            end = pq_to_xy((i, -q_ceil))
            end[0] = int(width / 2.0 + end[0])
            end[1] = int(height / 2.0 - end[1])
            pygame.draw.line(screen, grid_line_color, start, end, 1)
            start = pq_to_xy((-i, q_ceil))
            start[0] = int(width / 2.0 + start[0])
            start[1] = int(height / 2.0 - start[1])
            end = pq_to_xy((-i, -q_ceil))
            end[0] = int(width / 2.0 + end[0])
            end[1] = int(height / 2.0 - end[1])
            pygame.draw.line(screen, grid_line_color, start, end, 1)
            start = wq_to_xy((i, q_ceil))
            start[0] = int(width / 2.0 + start[0])
            start[1] = int(height / 2.0 - start[1])
            end = wq_to_xy((i, -q_ceil))
            end[0] = int(width / 2.0 + end[0])
            end[1] = int(height / 2.0 - end[1])
            pygame.draw.line(screen, grid_line_color, start, end, 1)
            start = wq_to_xy((-i, q_ceil))
            start[0] = int(width / 2.0 + start[0])
            start[1] = int(height / 2.0 - start[1])
            end = wq_to_xy((-i, -q_ceil))
            end[0] = int(width / 2.0 + end[0])
            end[1] = int(height / 2.0 - end[1])
            pygame.draw.line(screen, grid_line_color, start, end, 1)

        super(AmoeContext, self).draw(screen)


def run_sim(filename = None) :
    '''
    >>> run_sim()
    '''

    # create the oracle space

    oracle = AmoeOracleSpace()

    # create the context

    context = AmoeContext(oracle = oracle)

    # create the schedule for adding agents in the running

    schedule = Schedule()

    # add objects and agents to the context

    for i in range(1) : # the (2 * i)-th object is coupled with the (2 * i + 1)-th object, i.e. 0 is coupled with 1, 4 is coupled with 5.
        obj = AmoeObject(name = str(2 * i))
        obj.pos = (0, 0)
        context.add_obj(obj)
        schedule.add_agent(Agent(name = str(2 * i)))
        obj = AmoeObject(name = str(2 * i + 1))
        obj.pos = (0, 0)
        context.add_obj(obj)
        schedule.add_agent(Agent(name = str(2 * i + 1)))

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
    print("ok")
    run_sim(filename)
