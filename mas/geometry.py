
# MultiAgent
# (c) 2017-2019, NiL, csningli@gmail.com

import math
from numpy import array, dot
from numpy.linalg import norm

NON_ZERO_LOWER_BOUND = 0.01
HALF_PI = math.pi / 2.0

def min_max_bound(f, a, b) :
    return max(a, min(b, f))


def vec2_length(v) :
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def vec2_angle(v, positive = True) :
    angle = 0
    v_norm = vec2_length(v)
    if v_norm > 0.01 :
        angle = math.acos(v[0] / v_norm)
        if v[1] < 0 :
            if positive == True :
                angle = 2 * math.pi - angle
            else :
                angle = - angle
    return angle


def vec2_sub(v1, v2) :
    return (v1[0] - v2[0], v1[1] - v2[1])


def vec2_add(v1, v2) :
    return (v1[0] + v2[0], v1[1] + v2[1])


def vec2_dot(v1, v2) :
    return v1[0] * v2[0] + v1[1] * v2[1]


def vec2_scale(v, f) :
    return (f * v[0], f * v[1])


def vec2_norm(v) :
    result = 0
    length = vec2_length(v)
    if length > NON_ZERO_LOWER_BOUND :
        result = vec2_scale(v, 1.0 / length)
    return result


def vec2_rotate(v, a) :
    angle = vec2_angle(v) + a
    v_norm = vec2_length(v)
    return (v_norm * math.cos(angle), v_norm * math.sin(angle))


def vec2_min_max(v, a, b) :
    result = v
    length = vec2_length(v)
    if  length > NON_ZERO_LOWER_BOUND :
        result = vec2_scale(result, min_max_bound(length, a, b) / length)
    return result


def pldiff(p, p1, p2) :
    diff = array((0.0, 0.0))
    drt = array(p2) - array(p1)
    drt = drt / norm(drt)
    diff = array(p1) - drt * dot(array(p1) - array(p), drt) - array(p)
    return tuple(diff)


def pldist_l2(p, p1, p2):
    diff = pldiff(p = p, p1 = p1, p2 = p2)
    return norm(array(diff))


def ppdist_l2(p1, p2) :
    return norm(array(p1) - array(p2))


def ppdist_l1(p1, p2) :
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
