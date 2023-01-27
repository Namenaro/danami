from event import EventMemory, EventStat, InnerEventVals, OuterEventVals
from common_utils import Point
from samplers.utils import get_random_point, get_random_contrast_cogmap


# ходим по контрасту, собираем выборки параметров события
def fill_event_memory_naive(zmeyka, sample_size):
    event_stat = EventStat()
    for _ in range(sample_size):
        random_point = get_random_point()
        random_contrast_cogmap = get_random_contrast_cogmap()
        real_event_inner_vals, event_point = gather_best_realisation_of_event(event_memory, random_contrast_cogmap, random_point)
        if real_event_inner_vals is not None:
            du = event_point - random_point
            event_stat.add_realisation(zmeyka, du)
    inner_event_vals = InnerEventVals(zmeyka)
    return EventMemory(event_stat=event_stat, event_vals=inner_event_vals)


# вспомогательный метод
def gather_best_realisation_of_event(event_memory, cogmap, point):
    # за лучший берем ближайший
    result_ids_in_cogmap = cogmap.find_events_around_point_by_LUE(point, event_memory.LUE, wanted_num_events=1, exlusions=[])
    if len(result_ids_in_cogmap) == 0:
        return None, None
    id_in_cogmap = result_ids_in_cogmap[0]
    event_point = cogmap.get_point_by_event_id(id_in_cogmap)
    zmeyka = cogmap.get_zmeika_by_event_id(id_in_cogmap)
    real_event_inner_vals = InnerEventVals()
    real_event_inner_vals.fill(zmeyka)
    return real_event_inner_vals, event_point
