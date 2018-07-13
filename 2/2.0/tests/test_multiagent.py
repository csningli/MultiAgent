
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import sys, os, time, subprocess

tests = [ "test_agent.py", "test_commander.py", "test_cmdline.py", "test_context.py",
        "test_data.py", "test_driver.py", "test_inspector.py", "test_lookmixin.py",
        "test_memory.py", "test_message.py", "test_module.py",
        "test_object.py", "test_objmod.py", "test_obstacle.py", "test_oracle.py",
        "test_radarmod.py", "test_radiomod.py", "test_request.py",
        "test_schedule.py", "test_shot.py", "test_simulator.py",
        "test_timer.py", ]

if __name__ == '__main__' :
    for test in tests :
        if os.path.exists(test) :
            cmd = "python %s" % test
            subprocess.call(cmd, shell = True)
