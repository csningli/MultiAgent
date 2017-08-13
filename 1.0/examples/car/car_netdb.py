import sys, os, time, math, json

sys.path.append("../../../../NetDB/1.0/py")

from netdb import MetaPoint, RecordPoint

class Step(MetaPoint) :
    pass

class Unit(MetaPoint) :
    pass

class Pos(MetaPoint) :
    pass

class Angle(MetaPoint) :
    pass

class Pointer(MetaPoint) :
    pass

class Fill(MetaPoint) :
    pass

class Stroke(MetaPoint) :
    pass

class State(RecordPoint) :
    init_fields = {
        "Step" : None, 
        "Unit" : None, 
        "Pos" : None, 
        "Angle" : None, 
        "Pointer" : None, 
        "Fill" : None, 
        "Stroke" : None, 
    }



