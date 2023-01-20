from structure import StructureRealisation, StructureMemory
from cogmap import Cogmap
from evaluator import eval_realisation_non_triviality
from recogniser.event_predictor import Prediction, predict_for_next_event
from evaluator import measure_win_quality

from collections import namedtuple
from bisect import insort


RealisationEntry = namedtuple('RealisationEntry', ('realisation', 'non_triviality'))


class BasicGenerationSorted:
    def __init__(self):
        self.entries = []

    def insert_new_realisation(self, realisation, structure, cogmap):
        non_triviality = eval_realisation_non_triviality(realisation, structure, cogmap)
        entry = RealisationEntry(realisation, non_triviality)
        insort(self.entries, entry, key=lambda x: -x.non_triviality)  # в порядке убывания

    def cut_extra_exemplars(self, surviving_max):
        if len(self.entries) > surviving_max:
            self.entries = self.entries[:surviving_max]

    def init_as_first_generation(self, structure, cogmap):
        global_node_id = structure.get_first_event_id()
        LUE_id, mass, parent_global_id, u_from_parent = structure.get_info_about_event(global_node_id)
        for id_in_cogmap,  event_realisation in cogmap.events_ids_to_realisations.items():
            if event_realisation.LUE == LUE_id:
                realisation = StructureRealisation()
                realisation.add_new_check_result(global_id=global_node_id, id_in_cogmap=id_in_cogmap)
                self.insert_new_realisation(realisation, structure, cogmap)

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

    def get_best_realisation(self):
        return self.entries[0].realisation

    def get_all_realisations_sorted(self):
        all_realisations_sorted = []
        for entry in self.entries:
            all_realisations_sorted.append(entry.realisation)
        return all_realisations_sorted

    def get_all_energies_sorted(self):
        all_energies_sorted = []
        for entry in self.entries:
            all_energies_sorted.append(entry.non_triviality)
        return all_energies_sorted

    def get_win_quality(self):
        return measure_win_quality(self.get_all_energies_sorted())


