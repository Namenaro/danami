from event import EventMemory, EventRealisation
from common_utils import Point
from samplers.utils import get_random_point, get_random_contrast_cogmap


# ходим по контрасту, собираем выборки параметров события
def fill_event_memory_naive(event_memory, sample_size):
    masses = []
    u_dxs = []
    u_dys = []
    LUE_s = []

    for _ in range(sample_size):
        random_point = get_random_point()
        random_contrast_cogmap = get_random_contrast_cogmap()
        event_realisation, event_point = gather_best_realisation_of_event(event_memory, random_contrast_cogmap, random_point)
        if event_realisation is None:
            LUE_s.append(0)
        else:
            LUE_s.append(1)
            du = event_point - random_point
            u_dys.append(du.y)
            u_dxs.append(du.x)
            masses.append(event_realisation.mass)
        event_memory.set_samples(masses=masses, u_dxs=u_dxs, u_dys=u_dys, LUE_s=LUE_s)


# вспомогательный метод
def gather_best_realisation_of_event(event_memory, cogmap, point):
    # за лучший берем ближайший
    result_ids_in_cogmap = cogmap.find_events_around_point_by_LUE(point, event_memory.LUE, wanted_num_events=1)
    if len(result_ids_in_cogmap)==0:
        return None
    id_in_cogmap = result_ids_in_cogmap[0]
    event_point = cogmap.get_point_by_event_id(id_in_cogmap)
    event_realisation = cogmap.get_event_by_id(result_ids_in_cogmap)
    return event_realisation, event_point