
from mas.multiagent import *

class TouchPointOracle(OracleSpace) :
    def touch(self, c, d = 0) :
        blocks = []
        for obj in self.get_objs_at(c, d) :
            l = ppdist_l2(obj.pos, c)
            x = obj.pos[0] - c[0]
            y = obj.pos[1] - c[1]
            if (abs(l) > 0.001) :
                x *= max(0, l - obj.radius) / float(l)
                y *= max(0, l - obj.radius) / float(l)
            blocks.append((x, y))
        for obt in self.get_obts_at(c, d) :
            diff = pldiff(c, obt.start, obt.end)
            blocks.append((- diff[0], - diff[1]))
        return blocks

class ShowLabelObject(Object) :
    def __init__(self, name, mass = 1.0, radius = 10.0) :
        super(ShowLabelObject, self).__init__(name, mass, radius)
        self.__label = self.name

    @property
    def label(self) :
        return self.__label

    @label.setter
    def label(self, value) :
        self.__label = value

    def draw(self, screen) :
        super(ShowLabelObject, self).draw(screen)
        if self.visible == True :
            font = pygame.font.Font(None, 16)
            (width, height) = screen.get_size()
            pos_draw = (int(width / 2.0 + self.pos[0] - 5.0), int(height / 2.0 - self.pos[1] - self.radius - 10.0))
            screen.blit(font.render(self.label, 1, THECOLORS["black"]), pos_draw)
