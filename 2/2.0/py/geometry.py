
# MultiAgent 2.0 
# (c) 2017-2018, NiL, csningli@gmail.com

from numpy import array, dot
from numpy.linalg import norm


def pldiff(p, p1, p2):
    diff = array((0.0, 0.0))
    drt = array(p2) - array(p1)
    drt = drt / norm(drt)
    diff = array(p) - array(p1) - drt * dot(array(p) - array(p1), drt)
    return diff 


def pldist_l2(p, p1, p2):
    diff = pldiff(p = p, p1 = p1, p2 = p2)
    return norm(array(diff))


def ppdist_l2(p1, p2) : 
    return norm(array(p1) - array(p2))

def ppdist_l1(p1, p2) : 
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


