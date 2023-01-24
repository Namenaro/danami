from recogniser.event_predictor import Prediction, predict_for_next_event, predict_for_top_event
from recogniser.realisations_generation import BasicGenerationSorted, RealisationEntry
from globals import GLOBALS
from cogmap import Cogmap
from structure import StructureMemory, StructureRealisation, StructureTop

from copy import deepcopy

class RecogniserEngine:
    def __init__(self, structure, cogmap):
        self.structure = structure
        self.cogmap = cogmap
        self.generations_list = []
        self.win_quality = None

    def recognise(self):  # возвращает один "лучший" экземпляр структуры (не обязательно доросший до конца)
        self._init_first_generation()
        if self.generations_list[0].is_empty():
            return None

        for i in range(1, len(self.structure)):
            # если пусто  предыдущее , надо вернуть лушую реализуацию из предыдущего поколения
            if self.generations_list[-1].is_empty():
                self.win_quality = self.generations_list[-2].get_win_quality()
                return self.generations_list[-2].get_best_realisation()
            self._create_next_generaion()

        # если после всех шагов роста последнее поколение не пусто, то выозвращаем его лучший экземпляр
        if not self.generations_list[-1].is_empty():
            self.win_quality = self.generations_list[-1].get_win_quality()
            return self.generations_list[-1].get_best_realisation()

        # если последнее оказалось пусто возвращаем лучшее с предпоследнего (оно всегда есть и непусто)
        self.win_quality = self.generations_list[-2].get_win_quality()
        return self.generations_list[-2].get_best_realisation()

    def get_win_quality(self):
        return self.win_quality

    def get_all_win_qualities(self):
        win_qualities = []
        for generation in self.generations_list:
            win_qualities.append(generation.get_win_quality())
        return win_qualities

    # служебные методы----------------------------------------------
    def _init_first_generation(self):
        first_generation = BasicGenerationSorted()
        first_generation.init_as_first_generation(self.structure, self.cogmap)
        self.generations_list.append(first_generation)

    def _create_next_generaion(self):
        next_generation = BasicGenerationSorted()
        # предыдущее поколение всегда есть и не пусто
        for realisation_entry in self.generations_list[-1].entries:
            children_realisations_list = self._get_children_for_realisation(realisation_entry.realisation)
            for child_realisations in children_realisations_list:
                next_generation.insert_new_realisation(child_realisations, structure=self.structure, cogmap=self.cogmap)

        # обрезаем размер, чтобы избежать взрыва
        next_generation.cut_extra_exemplars(GLOBALS.SURVIVIVING_MAX)
        self.generations_list.append(next_generation)



    def _get_children_for_realisation(self, realisation):
        prediction = predict_for_next_event(self.structure, realisation, self.cogmap)

        # если уже есть связанное событие на карте, то результат распознавания однозначен
        linked_parent_local_event_id = realisation.try_get_event_check_result_by_linked_event(self.structure, prediction.global_event_id)
        if linked_parent_local_event_id is not None:
            target_local_event_id = self.cogmap.get_linked_event_id(linked_parent_local_event_id)
            child_realisation = deepcopy(realisation)
            child_realisation.add_new_check_result(global_id=prediction.global_event_id, id_in_cogmap=target_local_event_id)
            return [child_realisation]

        # находим не более GROW_MAX кандидатов на его результат проверки
        # причем событий-кандидатов проверяем, не учтено ли оно уже в этом экземпляре
        realisations_list = []
        local_events_ids_list = self.cogmap.find_events_around_point_by_LUE(point=prediction.point,
                                                                        LUE=prediction.LUE_id,
                                                                        wanted_num_events=GLOBALS.SURVIVIVING_MAX,
                                                                        exlusions=realisation.get_list_of_local_ids())
        for local_event_id in local_events_ids_list:
            child_realisation = deepcopy(realisation)
            child_realisation.add_new_check_result(global_id=prediction.global_event_id, id_in_cogmap=local_event_id )
            realisations_list.append(child_realisation)
        return realisations_list


