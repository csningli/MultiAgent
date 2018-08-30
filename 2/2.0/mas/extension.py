
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
