#! /Users/nil/anaconda3/bin/python

import sys, os, time, subprocess

tests = ["test_module.py", "test_object.py", "test_unit.py", "test_context.py",
        "test_driver.py", "test_zipper.py"]

if __name__ == '__main__' :
    for test in tests :
        cmd = "python %s" % test
        subprocess.call(cmd, shell = True)





