from .cogmap_base import CogmapBase
from .utils import *

# Класс, реализующий интерфейс к ког.карте.
# Функции, которые ее заполняют, вынесены в базовый класс.

class Cogmap(CogmapBase):
    def __init__(self, pic):
        CogmapBase.__init__(self, pic)  # этой строкой мы заполнили ког.карту событиями змеек
        self.exclusions = []

    def register_exclusion_event(self, id_in_cogmap):
        self.exclusions.append(id_in_cogmap)

    def find_events_around_point_by_LUE(self, point, LUE):
        # эти константы просто для того, чтоб примитивно ограничить комбинаторный взрыв, если он будет (не должен!)
        MAX_EVENTS = 20
        MAX_RADIUS = 50
        result = []
        radius = -1
        while True:
            if radius == MAX_RADIUS or MAX_EVENTS == len(result):
                break
            radius += 1
            candidate_points = get_coords_for_radius(center=point, radius=radius)
            for candidate_point in candidate_points:
                events_ids_list_in_point = self.points_to_events_ids.get(candidate_point, [])
                for event_id_in_cogmap in events_ids_list_in_point:
                    real_LUE = self.events_ids_to_realisations[event_id_in_cogmap].LUE
                    if real_LUE == LUE:
                        if event_id_in_cogmap not in self.exlusions:
                            result.append(event_id_in_cogmap)
        return result


    def get_event_by_id(self, id_in_cogmap):
        return self.events_ids_to_realisations[id_in_cogmap]

    def get_point_by_event_id(self, id_in_cogmap):
        return self.events_ids_to_points[id_in_cogmap]

    def get_linked_event_id(self, id_in_cogmap):
        return self.events_links[id_in_cogmap]
