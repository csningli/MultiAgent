#! /Users/nil/anaconda3/envs/multiagent_1_0/bin/python

# MultiAgent 1.1
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time, subprocess

tests = ["test_module.py", "test_object.py", "test_unit.py", "test_context.py",
        "test_driver.py", "test_zipper.py"]

if __name__ == '__main__' :
    for test in tests :
        if os.path.exists(test) :
            cmd = "python %s" % test
            subprocess.call(cmd, shell = True)





