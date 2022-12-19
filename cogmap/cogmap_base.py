from event import EventRealisation
from common_utils import IdsGenerator
from cogmap.LUE_rule import LUERule
from cogmap.utils import *
# Обьект-сцена, хранит информацию какие типы точек 2-го порядка найдены и кто с кем слинкован одной змейкой

# ожидает на вход картинки, бинаризованные так: 1 редкое событие, 0 - фон (частое)

class CogmapBase:
    def __init__(self, pic):
        self.pic = pic
        self.hor_img = None
        self.ver_img = None
        self._fill_hor_ver()
        self.rules = self._init_rules()

        self.local_ids_gen = IdsGenerator()

        self.points_to_events_ids = {}  # {point:  [id_in_cogmap] }
        self.events_ids_to_realisations = {}  # {id_in_cogmap:  EventRealisation }
        self.events_ids_to_points = {}   # id_in_cogmap: Point
        self.events_links = {}  # {id_in_cogmap:  id_in_cogmap}

        self._fill()

    def _fill_hor_ver(self):
        dammy_generator = IdsGenerator()
        rule_hor = LUERule(dx=1, dy=0, max_rad=1, is_horizontal=True, LUE_names_generator=dammy_generator)
        rule_ver = LUERule(dx=0, dy=1, max_rad=1, is_horizontal=True, LUE_names_generator=dammy_generator)
        seqs_hor = rule_hor.apply_to_binary_map(self.pic)
        seqs_ver = rule_ver.apply_to_binary_map(self.pic)
        self.hor_img = seqs_starts_to_binary_map(map_shape=self.pic.shape, seqs=seqs_hor)
        self.ver_img = seqs_starts_to_binary_map(map_shape=self.pic.shape, seqs=seqs_ver)

    def _init_rules(self):
        LUE_events_ids_gen = IdsGenerator()
        rule1 = LUERule(dx=0, dy=1, max_rad=5, is_horizontal=True, LUE_names_generator=LUE_events_ids_gen)
        rule2 = LUERule(dx=1, dy=0, max_rad=5, is_horizontal=False, LUE_names_generator=LUE_events_ids_gen)
        return [rule1, rule2]

    def _fill(self):
        for rule in self.rules:
            if rule.is_horizontal:
                found_seqs = rule.apply_to_binary_map(self.hor_img)
            else:
                found_seqs = rule.apply_to_binary_map(self.ver_img)
            if len(found_seqs) > 0:
                for seq in found_seqs:
                    self._register_seq(seq, rule)

    def _register_seq(self, seq, rule):
        # событие начало
        id_of_start_in_cogmap = self.local_ids_gen.generate_id()
        start_event_point = seq[0]
        start_event = EventRealisation(seq, LUE=rule.start_LUE_id)

        # событие конец
        id_of_end_in_cogmap = self.local_ids_gen.generate_id()
        end_event_point = seq[-1]
        end_event = EventRealisation(seq, LUE=rule.end_LUE_id)

        # регистрация событий на карте:
        # 1. регистрируем событие в точке
        if start_event_point not in  self.points_to_events_ids.keys():
            self.points_to_events_ids[start_event_point]=[]
        if end_event_point not in self.points_to_events_ids.keys():
            self.points_to_events_ids[end_event_point] = []
        self.points_to_events_ids[start_event_point].append(id_of_start_in_cogmap)
        self.points_to_events_ids[end_event_point].append(id_of_end_in_cogmap)

        # 2. свазяваем данные по событию с его локальным именем, уникальным в этой карте
        self.events_ids_to_realisations[id_of_start_in_cogmap] = start_event
        self.events_ids_to_realisations[id_of_end_in_cogmap] = end_event

        # 3. помечаем, какие события порождены одной змейкой
        self.events_links[id_of_start_in_cogmap] = id_of_end_in_cogmap
        self.events_links[id_of_end_in_cogmap] = id_of_start_in_cogmap

        # 4. события в точки
        self.events_ids_to_points[id_of_start_in_cogmap] = start_event_point
        self.events_ids_to_points[id_of_end_in_cogmap] = end_event_point
