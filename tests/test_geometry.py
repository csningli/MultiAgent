
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time, subprocess

tests = [ "test_min_max_bound.py", "test_vec2_length.py", "test_vec2_angle.py",
        "test_vec2_sub.py", "test_vec2_add.py", "test_vec2_dot.py", "test_vec2_scale.py", "test_vec2_norm.py",
        "test_vec2_rotate.py", "test_vec2_min_max.py",
        "test_pldiff.py", "test_pldist_l2.py", "test_ppdist_l2.py", "test_ppdist_l1.py",
        ]

if __name__ == '__main__' :
    for test in tests :
        if os.path.exists(test) :
            cmd = "python %s" % test
            subprocess.call(cmd, shell = True)
