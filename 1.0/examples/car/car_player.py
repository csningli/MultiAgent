#! /Users/nil/anaconda3/bin/python

import sys, os, time

sys.path.append("../../py")

from multiagent import * 
from car_simulation import car_objects, car_context

@test_func
def test_player(filename) :
    data = Data()
    data.from_file(filename)
  
    zipper = Zipper(data = data, context = car_context, objects = car_objects)
    car_player = Player(zipper = zipper)
    car_player.play(steps = None, inspector = None, graphics = True)
    
if __name__ == '__main__' :
    if (len(sys.argv) < 2) : 
        print('Usage: test_player.py filename')
        exit()
    test_player(sys.argv[1])



