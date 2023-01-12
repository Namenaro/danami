from structure import StructureTop, StructureMemory, StructureRealisation
from samplers import sample_top, sample_struct

from copy import deepcopy

# Считаем, что структура уже инициализирована одним или несколькими узлами
class GrowStep:
    def __init__(self, structure, master_realisation):
        self.structure = structure
        self.master_realisation = master_realisation
        self.stat_object = sample_struct(structure)

    def grow_step(self):
        list_structure_tops = self.select_candidates()
        list_candidate_structures = []
        for structure_top in list_structure_tops:
            event_memory = sample_top(self.structure, structure_top)
            new_structure = deepcopy(self.structure)
            new_structure.add_new_event(event_memory, u_from_parent=structure_top.u_from_parent)

        winner_structure, stat_object = self.select_winner_structure(list_candidate_structures)
        self.structure = winner_structure
        self.stat_object = stat_object

        # relax_structure (self.structure, self.stat_object)
        # if realxed is better: добавялем ее

    def select_candidates(self):
        # прямые и обратные
        return list_structure_tops

    def select_winner_structure(self, list_structures):
        # заполняем статистический объект с полной инфой о структуре
        # делаем решение, какая структура самая лучшая
        return winner_structure, stat_object
