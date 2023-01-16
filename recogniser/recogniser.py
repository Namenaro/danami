from recogniser.event_predictor import Prediction, predict_for_next_event, predict_for_top_event
from realisations_generation import BasicGenerationSorted
from globals import GLOBALS
from cogmap import Cogmap
from structure import StructureMemory, StructureRealisation, StructureTop

from copy import deepcopy

class RecogniserEngine:
    def __init__(self, structure, cogmap):
        self.structure = structure
        self.cogmap = cogmap
        self.generations_list = []

    def recognise(self): # возвращает один "лучший" экземпляр структуры (не обязательно доросший до конца)
        self._init_first_generation()
        if self.generations_list[0].is_empty:
            return None

        for i in range(1, len(self.structure)):
            # если пусто  предыдущее , надо вернуть лушую реализуацию из предыдущего поколения
            if self.generations_list[-1].is_empty():
                return self.generations_list[-1].get_best_realisation()
            self._create_next_generaion()

        # если после всех шагов роста последнее поколение не пусто, то выозвращаем его лучший экземпляр
        if not self.generations_list[-1].is_empty():
            return self.generations_list[-1].get_best_realisation()
        # если последнее оказалось пусто возвращаем лучшее с предпоследнего (оно всегда есть и непусто)
        return self.generations_list[-2].get_best_realisation()


    # служебные методы----------------------------------------------
    def _init_first_generation(self):
        first_generation = BasicGenerationSorted()
        first_generation.init_as_first_generation(self.structure, self.cogmap)

    def _create_next_generaion(self):
        next_generation = BasicGenerationSorted()
        # предыдущее поколение всегда есть и не пусто
        for realisation_entry in self.self.generations_list[-1]:
            children_realisations_list = self._get_children_for_exemplar(realisation_entry)
            for child_realisations in children_realisations_list:
                next_generation.insert_new_exemplar(child_realisations)

        # обрезаем размер, чтобы избежать взрыва
        next_generation.cut_extra_exemplars(GLOBALS.SURVIVIVING_MAX)
        self.generations_list.append(next_generation)



    def _get_children_for_realisation(self, realisation):
        prediction = predict_for_next_event(self.structure, realisation, self.cogmap)

        # если уже есть связанное событие на карте, то результат распознавания однозначен
        target_local_event_id = realisation.try_get_event_check_result_by_linked_event(self.structure, prediction.global_event_id)
        if target_local_event_id is not None:
            child_realisation = deepcopy(realisation)
            child_realisation.add_event_check_result(prediction.global_event_id, target_local_event_id)
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
            child_realisation.add_new_event_realisation(local_event_id, prediction.global_event_id)
            realisations_list.append(child_realisation)
        return realisations_list



