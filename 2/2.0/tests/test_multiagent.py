
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time, subprocess

tests = ["test_object.py", "test_agent.py", "test_message.py", "test_request.py",
        "test_oracle.py", "test_timer.py", "test_context.py",  "test_schedule.py",
        "test_driver.py", "test_simulator.py"]

if __name__ == '__main__' :
    for test in tests :
        if os.path.exists(test) :
            cmd = "python %s" % test
            subprocess.call(cmd, shell = True)
