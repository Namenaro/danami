from structure import StructureTop, StructureMemory, StructureRealisation
from samplers import sample_top, StatObject, select_best_stat_object


from copy import deepcopy

# Считаем, что структура уже инициализирована одним или несколькими узлами
class GrowStep:
    def __init__(self, structure, master_realisation, master_cogmap):
        self.structure = structure
        self.master_realisation = master_realisation
        self.stat_object = StatObject(structure)
        self.stat_object.fill()

        self.master_cogmap = master_cogmap


    def grow_step(self):
        wanted_num_candidates = 2
        list_structure_tops = self.select_forward_candidates(wanted_num_candidates)
        list_candidate_structures = []

        event_memory_list = sample_top(self.structure, list_structure_tops)
        for i in range(len(event_memory_list)):
            event_memory = event_memory_list[i]
            new_structure = deepcopy(self.structure)
            new_structure.add_new_event(event_memory, u_from_parent=list_structure_tops[i].u_from_parent,
                                        parent_global_id=list_structure_tops[i].global_parent_id,
                                        is_linked_to_parent=list_structure_tops[i].is_linked_to_parent
                                        )

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
        # заполняем статистику по всем сравниваемым структурам:
        stat_objects = []
        for struct_memory in list_structures:
            stat_object = StatObject(struct_memory)
            stat_object.fill()
            stat_objects.append(stat_object)

        # делаем решение, какая структура самая лучшая
        winner_index = select_best_stat_object(stat_objects)
        return list_structures[winner_index], stat_objects[winner_index]
