from .cogmap_base import CogmapBase
from .utils import *

# Класс, реализующий интерфейс к ког.карте.
# Функции, которые ее заполняют, вынесены в базовый класс.

class Cogmap(CogmapBase):
    def __init__(self, pic):
        CogmapBase.__init__(self, pic)  # этой строкой мы заполнили ког.карту событиями змеек

    def find_events_around_point_by_LUE(self, point, LUE, wanted_num_events, exlusions):
        # эти константы просто для того, чтоб примитивно ограничить комбинаторный взрыв, если он будет (не должен!)
        MAX_EVENTS = wanted_num_events
        MAX_RADIUS = 50
        result_ids_in_cogmap = []
        radius = -1
        while True:
            if radius == MAX_RADIUS or MAX_EVENTS == len(result_ids_in_cogmap):
                break
            radius += 1
            candidate_points = get_coords_for_radius(center=point, radius=radius)
            for candidate_point in candidate_points:
                events_ids_list_in_point = self.points_to_events_ids.get(candidate_point, [])
                for event_id_in_cogmap in events_ids_list_in_point:
                    real_LUE = self.events_ids_to_realisations[event_id_in_cogmap].LUE
                    if real_LUE == LUE:
                        if event_id_in_cogmap not in exlusions:
                            result_ids_in_cogmap.append(event_id_in_cogmap)
        return result_ids_in_cogmap


    def get_event_by_id(self, id_in_cogmap):
        return self.events_ids_to_realisations[id_in_cogmap]

    def get_point_by_event_id(self, id_in_cogmap):
        return self.events_ids_to_points[id_in_cogmap]

    def get_linked_event_id(self, id_in_cogmap):
        return self.events_links[id_in_cogmap]

    def select_most_massive(self):
        sorted_ids_list = self.events_list_sorted_by_mass
        best_id = sorted_ids_list[0]
        best_realisation = self.events_ids_to_realisations[best_id]
        return best_realisation, best_id

    def select_n_most_massive_ids(self, n, exceptions):
        approved_ids = []
        for local_id in self.events_list_sorted_by_mass:
            if local_id in exceptions:
                continue
            approved_ids.append(local_id)

        if len(approved_ids) > n:
            return approved_ids[:n]
        return approved_ids

