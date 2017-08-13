import sys, os, time, math, json

sys.path.append("../../py")
sys.path.append("../../../../NetDB/1.0/py")
sys.path.append("../../../../TaskTerm/1.0/py")

from multiagent import *
from netdb import NetDB, Selector, Predicate
from taskterm import TaskTerm
from car_netdb import Step, Unit, Pos, Angle, Pointer, Fill, Stroke, State


def data_to_net(src) :
    solid = {}
    if os.path.exists(src) :
        data = {}
        with open(src, 'r') as f : 
            data = json.load(f)
        if data is not None and len(data) > 0 :
            solid["State"] = []
            for (step, step_data) in data.items() :
                for (unit, unit_data) in step_data.items() :
                    if unit not in ["_global_", ] :
                        state = {"Step" : str(step), "Unit" : str(unit)}
                        pos = unit_data.get("pos", None)
                        if pos is not None :
                            pos_list = pos.split(' ') 
                            state["Pos"] = "%.2f %.2f" % (float(pos_list[0]), float(pos_list[1]))
                        angle = unit_data.get("angle", None)
                        if angle is not None :
                            state["Angle"] = "%.2f" % float(angle)
                        pointer = unit_data.get("pointer", None)
                        if pointer is not None :
                            p_list = pointer.split(' ')
                            state["Pointer"] = "%d %d %d" % (float(p_list[0]), float(p_list[1]), float(p_list[2]))
                        fill = unit_data.get("fill", None)
                        if fill is not None :
                            f_list = fill.split(' ')
                            state["Fill"] = "%d %d %d" % (float(f_list[0]), float(f_list[1]), float(f_list[2]))
                        stroke = unit_data.get("stroke", None)
                        if stroke is not None :
                            s_list = stroke.split(' ')
                            state["Stroke"] = "%d %d %d" % (float(s_list[0]), float(s_list[1]), float(s_list[2]))
                            
                        if len(state) > 2 :
                            solid["State"].append(state)
    return solid


class MultiAgentAnalyse(TaskTerm) :
    _name_ = 'MAS'
    _version_ = 'v1.0'
    _comment_ = 'copyright (c) NiL, csningli@gmail.com.'
   
    db = None
    def __init__(self) :
        super(MultiAgentAnalyse, self).__init__()
        self.db = NetDB(name = "DB")
        self.db.add_cons(name = "Step", cons = Step)
        self.db.add_cons(name = "Unit", cons = Unit)
        self.db.add_cons(name = "Pos", cons = Pos)
        self.db.add_cons(name = "Angle", cons = Angle)
        self.db.add_cons(name = "Pointer", cons = Pointer)
        self.db.add_cons(name = "Fill", cons = Fill)
        self.db.add_cons(name = "Stroke", cons = Stroke)
        self.db.add_cons(name = "State", cons = State)
        

    
    def dump(self) :
        """
        None -> \'.net\'; Call the \'dump()\' method of NetDB.
        """
        self.db.dump()

    def sel(self, fts) :
        """
        list<dict> -> list<State>; Select states according to filters in \'fts\';
        Usage: sel [{"Key":"Value"}, {}, ...]
        """
         
        points = None 
        
        pos_line = self.db.get_or_create_line(line_name = "Pos")
        angle_line = self.db.get_or_create_line(line_name = "Angle")
        step_line = self.db.get_or_create_line(line_name = "Step")
        unit_line = self.db.get_or_create_line(line_name = "Unit")
        state_line = self.db.get_or_create_line(line_name = "State")
        
        if None not in [pos_line, angle_line, step_line, unit_line, state_line] :
            predicates = []
            fts_list = eval(fts)
            for ft in fts_list : 
                target = State()

                pos = ft.get("Pos", None)
                if pos is not None :
                    target.put("Pos", pos_line.add_point(Pos(present = str(pos))))

                angle = ft.get("Angle", None)
                if angle is not None :
                    target.put("Angle", angle_line.add_point(Angle(present = str(angle))))

                step = ft.get("Step", None)
                if step is not None :
                    target.put("Step", step_line.add_point(Step(present = str(step))))

                unit = ft.get("Unit", None)
                if unit is not None :
                    target.put("Unit", unit_line.add_point(Unit(present = str(unit))))

                predicates.append((Predicate.record_point_filter, target))
                
            if len(predicates) > 0 :
                points = Selector(predicates = predicates).select_points(state_line)
                
        if points is not None :
            print("Selection result:")
            print("-" * 35)
            for point in points :
                print("%s" % point.fields)
        else :
            print("No return.")


if __name__ == '__main__' :
    if len(sys.argv) > 1 :
        src = sys.argv[1]
        if os.path.exists(src) :
            n = MultiAgentAnalyse()
            ext = os.path.splitext(src)[1]
            if ext == ".data" :
                n.db.hollow(data_to_net(src))
            elif ext == ".net" :  
                n.db.load(src)
            else : 
                print("Invalid file type:", ext)
                exit(1)
            n.run()
        else :
            print("Invalid file path:", sys.argv[1])
    else :
        print("Too few arguments.")
        print("Usage: python car_analyse.py [path_to_data_file]")
        

