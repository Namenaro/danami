from structure import StructureMemory, StructureRealisation, StructureTop
from event import EventRealisation
from cogmap import Cogmap
from common_utils import Point

def recognition_resume_for_top(top, structure, struct_realisation, cogmap):
    if len(struct_realisation) != len(structure):
        return None

    # если оно линковано к родителю, то определяется однозначным образом
    local_parent_id = struct_realisation.get_local_id_by_global(top.global_parent_id)
    if top.is_linked_to_parent:
        linked_event_id_in_cogmap = cogmap.get_linked_event_id(local_parent_id)
        return linked_event_id_in_cogmap

    # иначе ищем ближайшего с нужным LUE_id
    point_of_parent = cogmap.get_point_by_event_id(local_parent_id)
    expected_point = point_of_parent + top.u_from_parent
    local_events_ids_list = cogmap.find_events_around_point_by_LUE(point=expected_point,
                                                                        LUE=top.LUE_id,
                                                                        wanted_num_events=1,
                                                                        exlusions=struct_realisation.get_list_of_local_ids())
    event_local_id = local_events_ids_list[0]
    event_realisation = cogmap.get_event_by_id(event_local_id)
    real_point = cogmap.get_point_by_event_id(event_local_id)
    return event_local_id, event_realisation, expected_point, real_point
