#! /Users/nil/anaconda3/envs/multiagent_2/bin/python

# copyright, 2018, NiL, csningli@gmail.com

import sys

sys.path.append("../py")

from console import *  

class CommandLine(MultiAgentCommandLine) :
    pass

if __name__ == '__main__' :
    c = CommandLine()
    c.run()


