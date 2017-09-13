
from numpy import array, dot
from numpy.linalg import norm

def bias_to_line(point, p1, p2):
    bias = array((0.0, 0.0))
    direction = array(p2) - array(p1)
    direction = direction / norm(direction)
    bias = array(point) - array(p1) - direction * dot(array(point) - array(p1), direction)
    return bias

def distance_to_line(point, p1, p2):
    bias = bias_to_line(point = point, p1 = p1, p2 = p2)
    return norm(array(bias))
