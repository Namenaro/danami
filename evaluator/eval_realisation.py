from structure import StructureMemory, StructureRealisation
from cogmap import Cogmap
from event import EventMemory


def eval_realisation_non_triviality(struct_realisation, struct_memory, cogmap):
    non_triviality = 0

    for global_id in struct_memory.recognition_order:
        local_id = struct_realisation.get_local_id_by_global(global_id)
        if local_id is None:
            break
        zmeyka = cogmap.get_zmeika_by_event_id(local_id)
        event_memory = struct_memory.get_event_memory_obj(global_id)
        if struct_memory.is_event_first(global_id):
            u_err = None
        else:
            predicted_point, real_point = get_predicted_and_real_point(global_id, struct_realisation, struct_memory, cogmap)
            u_err = real_point - predicted_point

        non_triviality += event_memory.eval_realisation(zmeyka, u_err)

    return non_triviality


def get_predicted_and_real_point(global_id, struct_realisation, struct_memory, cogmap):
    local_id = struct_realisation.get_local_id_by_global(global_id)
    # реальное местоположение события на карте
    real_point = cogmap.get_point_by_event_id(local_id)

    # предсказанное
    parent_global_id = struct_memory.get_parent_id(global_id)
    parent_id_in_cogmap = struct_realisation.get_local_id_by_global(parent_global_id)
    parent_real_point = cogmap.get_point_by_event_id(parent_id_in_cogmap)
    u_from_parent = struct_memory.get_u_from_parent(child_global_id=global_id)
    predicted_point = parent_real_point + u_from_parent

    return predicted_point, real_point
