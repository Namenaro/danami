from cogmap import Cogmap
from common_utils import Point
from grower.graph_optimisation import get_optimized_graph
from structure import StructureMemory, StructureRealisation
from event import EventMemory, EventStat, OuterEventVals, InnerEventVals
from globals import GLOBALS


def get_dammy_struct_and_realisation(cogmap, num_events):
    best_ids = cogmap.select_n_most_massive_ids(num_events, exceptions=[])
    struct_realisation, struct_memory = get_dammy_struct_and_realisation_from_events_list(best_ids, cogmap)
    return struct_realisation, struct_memory

def get_dammy_struct_and_realisation_from_events_list(cogmap_events_ids_list, cogmap):
    # создаем матрицу полносвязного графа с вершинами в cogmap_events_ids и ребрами-расстояниями
    result_matrix_us = events_list_to_matrix(cogmap_events_ids_list, cogmap)

    # оптимизируем граф (строим остовное дерево)
    graph = get_optimized_graph(result_matrix_us, cogmap_events_ids_list)

    # инициализиурем реализацию и частично заполненную структуру одним событием
    struct_realisation, struct_memory = init_by_first_event(local_event_id=graph.recognition_order[0], cogmap=cogmap)

    if len(cogmap_events_ids_list) == 1:
        return struct_realisation, struct_memory

    # заполняем структуру и реализацию остальными событиями из минимального остовного дерева
    for local_event_id in graph.recognition_order[1:]:
        global_id = GLOBALS.GLOBAL_IDS_GEN.generate_id()
        struct_realisation.add_new_check_result(global_id=global_id, id_in_cogmap=local_event_id)


        event_memory = fill_dammy_event_memory_from_cogmap_event(cogmap, local_event_id)
        parent_local_id = graph.get_parent_id(local_event_id)
        parent_point = cogmap.get_point_by_event_id(parent_local_id)
        child_point = cogmap.get_point_by_event_id(local_event_id)
        u_from_parent = child_point - parent_point
        linked_local_node_id = cogmap.get_linked_event_id(local_event_id)
        if linked_local_node_id in struct_realisation.get_list_of_local_ids():
            is_linked_to_parent = True
        else:
            is_linked_to_parent = False
        parent_global_id = struct_realisation.get_global_id_by_local(parent_local_id)
        struct_memory.add_new_event(event_memory, u_from_parent, parent_global_id, is_linked_to_parent, global_id=global_id)

    return struct_realisation, struct_memory


def init_by_first_event(local_event_id, cogmap):
    struct_realisation = StructureRealisation()
    struct_memory = StructureMemory()
    event_memory = fill_dammy_event_memory_from_cogmap_event(cogmap, local_event_id)
    global_id = GLOBALS.GLOBAL_IDS_GEN.generate_id()
    struct_memory.set_first_event(event_memory, global_id)
    struct_realisation.add_new_check_result(global_id=global_id, id_in_cogmap=local_event_id)
    return struct_realisation, struct_memory


def fill_dammy_event_memory_from_cogmap_event(cogmap, local_event_id):
    LUE = cogmap.events_ids_to_LUES[local_event_id]
    zmeyka = cogmap.get_zmeika_by_event_id(local_event_id)
    event_stat = None
    event_inner_vals = InnerEventVals()
    event_inner_vals.fill(zmeyka=zmeyka)
    event_memory = EventMemory(LUE, event_inner_vals, event_stat)
    return event_memory


def events_list_to_matrix(cogmap_events_ids_list, cogmap):
    result_matrix_us = []
    for start_node_id in cogmap_events_ids_list:
        start_node_point = cogmap.get_point_by_event_id(start_node_id)
        us_array_for_this_start_node = get_all_u_data_for_start_node(start_node_point, cogmap_events_ids_list, cogmap)
        result_matrix_us.append(us_array_for_this_start_node)
    return result_matrix_us


def get_all_u_data_for_start_node(start_node_point, cogmap_events_ids_list, cogmap):
    result_array_us = []
    for end_node_id in cogmap_events_ids_list:
        end_node_point = cogmap.get_point_by_event_id(end_node_id)
        dist = (start_node_point - end_node_point).norm()
        result_array_us.append(dist)
    return result_array_us