from structure import StructureMemory, StructureRealisation, StructureTop
from cogmap import Cogmap
class Prediction:
    def __init__(self, LUE_id, point, mass, global_event_id):
        self.LUE_id = LUE_id
        self.point = point
        self.mass = mass
        self.global_event_id = global_event_id

def predict_for_next_event(structure, structure_realisation, cogmap):
    num_of_next_event = len(structure_realisation)
    if num_of_next_event == len(structure):
        return None
    next_event_global_id = structure.recognition_order[num_of_next_event]
    prediction = predict_for_event(structure, structure_realisation, next_event_global_id, cogmap)
    return prediction
def predict_for_event(structure, structure_realisation, global_event_id, cogmap):
    LUE_id, mass, parent_global_id, u_from_parent = structure.get_info_about_event(global_event_id)
    id_of_parent_in_cogmap = structure_realisation.get_local_id_by_global(parent_global_id)
    point_of_parent = cogmap.get_point_by_event_id(id_of_parent_in_cogmap)
    point = point_of_parent + u_from_parent
    return Prediction(LUE_id, point, mass, global_event_id)

def predict_for_top_event(structure, structure_realisation, top_of_struct,  cogmap):
    id_of_parent_in_cogmap = structure_realisation.get_local_id_by_global(top_of_struct.global_parent_id)
    point_of_parent = cogmap.get_point_by_event_id(id_of_parent_in_cogmap)
    point = point_of_parent + top_of_struct.u_from_parent
    prediction = Prediction( top_of_struct.LUE_id, point, top_of_struct.mass, global_event_id=None)
    return prediction