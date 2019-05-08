
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import sys, os, time
import doctest

from steering_move_sim import turn_vel

def test_turn_vel() :
    '''
    >>> test_turn_vel()
    turn (1.0, 0.0) by 1.0 : (1.00, 1.00)
    turn (1.0, 1.0) by 1.41 : (0.00, 2.00)
    '''
    print("turn (1.0, 0.0) by 1.0 : (%.2f, %.2f)" % turn_vel((1.0, 0.0), 1.0))
    print("turn (1.0, 1.0) by 1.41 : (%.2f, %.2f)" % turn_vel((1.0, 1.0), 1.41))

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[turn_vel Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
