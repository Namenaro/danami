from structure import StructureTop, StructureMemory, StructureRealisation
from samplers import sample_top, sample_struct

from copy import deepcopy

# Считаем, что структура уже инициализирована одним или несколькими узлами
class GrowStep:
    def __init__(self, structure, master_realisation, master_cogmap):
        self.structure = structure
        self.master_realisation = master_realisation
        self.stat_object = sample_struct(structure)
        self.master_cogmap = master_cogmap

    def grow_step(self):
        list_structure_tops = self.select_forward_candidates(wanted_num_candidates=2)
        list_candidate_structures = []
        for structure_top in list_structure_tops:
            event_memory = sample_top(self.structure, structure_top)
            new_structure = deepcopy(self.structure)
            new_structure.add_new_event(event_memory, u_from_parent=structure_top.u_from_parent,
                                        parent_global_id=structure_top.global_parent_id,
                                        is_linked_to_parent=structure_top.is_linked_to_parent)

        winner_structure, stat_object = self.select_winner_structure(list_candidate_structures)
        self.structure = winner_structure
        self.stat_object = stat_object

        # relax_structure (self.structure, self.stat_object)
        # if realxed is better: добавялем ее

    def select_forward_candidates(self, wanted_num_candidates):
        exceptions = self.master_realisation.get_list_of_local_ids()
        best_ids = self.master_cogmap.select_n_most_massive_ids(wanted_num_candidates, exceptions)
        return best_ids

    def select_winner_structure(self, list_structures):
        # заполняем статистический объект с полной инфой о структуре
        # делаем решение, какая структура самая лучшая
        return winner_structure, stat_object
