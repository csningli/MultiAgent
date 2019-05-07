
# MultiAgent 2.0
# (c) 2017-2018, NiL, csningli@gmail.com

import math
from numpy import array, dot
from numpy.linalg import norm

def min_max_bound(f, a, b) :
    return max(a, min(b, f))


def vec2_norm(v) :
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def vec2_angle(v) :
    angle = 0
    v_norm = vec2_norm(v)
    if v_norm > 0.01 :
        angle = math.acos(v[0] / v_norm)
        if v[1] < 0 :
            angle = - angle + 2 * math.pi
    return angle


def vec2_sub(v1, v2) :
    return (v1[0] - v2[0], v1[1] - v2[1])


def vec2_add(v1, v2) :
    return (v1[0] + v2[0], v1[1] + v2[1])


def vec2_scale(v, f) :
    return (v[0] * f, v[1] * f)


def vec2_rotate(v, a) :
    angle = vec2_angle(v) + a
    v_norm = vec2_norm(v)
    return (v_norm * math.cos(angle), v_norm * math.sin(angle))


def vec2_turn(v, f) :
    turn = vec2_rotate(v, math.pi / 2.0)
    turn_norm = vec2_norm(turn)
    if turn_norm > 0.01 :
        turn = vec2_scale(turn, f / turn_norm)
    return vec2_add(v, turn)


def pldiff(p, p1, p2) :
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
