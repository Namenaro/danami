from structure import StructureRealisation, StructureMemory
from cogmap import Cogmap
from evaluator import eval_realisation_non_triviality
from event_predictor import Prediction, predict_for_next_event

from collections import namedtuple
from bisect import insort


RealisationEntry = namedtuple('RealisationEntry', ('realisation', 'non_triviality'))


class BasicGenerationSorted:
    def __init__(self):
        self.entries = []

    def insert_new_realisation(self, realisation):
        non_triviality = eval_realisation_non_triviality(realisation)
        entry = RealisationEntry(realisation, non_triviality)
        insort(self.entries, entry, key=lambda x: -x.non_triviality)  # в порядке убывания

    def cut_extra_exemplars(self, surviving_max):
        if len(self.entries) > surviving_max:
            self.entries = self.entries[:surviving_max]

    def init_as_first_generation(self, structure, cogmap):
        global_node_id = structure.get_first_global_event_id()
        prediction = structure.get_info_to_recognise_node(global_node_id)
        for id_in_cogmap,  event_realisation in cogmap.events_ids_to_realisations:
            if event_realisation.LUE == prediction.LUE_id:
                realisation = StructureRealisation()
                realisation.add_new_event_realisation(id_in_cogmap, global_node_id)
                self.insert_new_realisation(realisation)

    def is_empty(self):
        if len(self.entries) == 0:
            return True
        return False

    def try_find_done_realisation(self, structure):
        for exemplar_entry in self.entries:
            if len(exemplar_entry.realisation) == len(structure):
                return exemplar_entry.exemplar
        return None

    def __len__(self):
        return len(self.entries)
