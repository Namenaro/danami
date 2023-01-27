from structure import StructureMemory, StructureRealisation, StructureTop
from event import InnerEventVals, OuterEventVals, EventMemory, EventStat
from cogmap import Cogmap
from common_utils import Point

def recognition_resume_for_top(top, struct_realisation, cogmap):
    local_parent_id = struct_realisation.get_local_id_by_global(top.global_parent_id)
    point_of_parent = cogmap.get_point_by_event_id(local_parent_id)
    expected_point = point_of_parent + top.u_from_parent

    # если оно линковано к родителю, то определяется однозначным образом
    if top.is_linked_to_parent:
        event_local_id = cogmap.get_linked_event_id(local_parent_id)

    else:
        # иначе ищем ближайшего с нужным LUE_id
        local_events_ids_list = cogmap.find_events_around_point_by_LUE(point=expected_point,
                                                                        LUE=top.LUE_id,
                                                                        wanted_num_events=1,
                                                                        exlusions=struct_realisation.get_list_of_local_ids())
        if len(local_events_ids_list) ==0:
            return None, expected_point, None
        event_local_id = local_events_ids_list[0]

    zmeyka = cogmap.get_zmeika_by_event_id(event_local_id)
    real_point = cogmap.get_point_by_event_id(event_local_id)
    return zmeyka, expected_point, real_point
