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
        WANTED_NUM_CANDIDATES = 2
        list_selected_local_ids = self.select_forward_candidates(WANTED_NUM_CANDIDATES)
        list_structure_tops = [self.cogmap_event_to_top_obj(local_event_id)
                               for local_event_id in list_selected_local_ids]
        list_candidate_structures = []

        event_memory_list = sample_top(self.structure, list_structure_tops)
        for i in range(len(event_memory_list)):
            event_memory = event_memory_list[i]
            new_structure = deepcopy(self.structure)
            new_structure.add_new_event(event_memory, u_from_parent=list_structure_tops[i].u_from_parent,
                                        parent_global_id=list_structure_tops[i].global_parent_id,
                                        is_linked_to_parent=list_structure_tops[i].is_linked_to_parent
                                        )
            list_candidate_structures.append(new_structure)

        winner_index, stat_object = self.select_winner_structure(list_candidate_structures)
        self.structure = list_candidate_structures[winner_index]
        self.stat_object = stat_object

        # наращиваем мастер-реализацию на одно событие
        winner_local_id = list_selected_local_ids[winner_index]
        winner_global_id = self.structure.recognition_order[-1]
        self.master_realisation.add_new_check_result(winner_global_id, winner_local_id)

        ################################## relax_structure (self.structure, self.stat_object)


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
        return winner_index, stat_objects[winner_index]

    def cogmap_event_to_top_obj(self, local_event_id):
        # выберем в родители ему просто того, кто ближе! даже линковку не учтем
        global_parent_id, u_from_parent = self.select_nearest_event_in_struct(local_event_id)

        local_parent_id = self.master_realisation.get_local_id_by_global(global_parent_id)
        if local_parent_id == self.master_cogmap.get_linked_event_id(local_event_id):
            is_linked_to_parent = True
        else:
            is_linked_to_parent = False

        event_realisation = self.master_cogmap.get_event_by_id(local_event_id)
        mass = event_realisation.mass
        LUE_id = event_realisation.LUE

        top = StructureTop(u_from_parent, global_parent_id, mass, LUE_id, is_linked_to_parent)
        return top

    def select_nearest_event_in_struct(self, local_event_id):
        point = self.master_cogmap.get_point_by_event_id(local_event_id)

        best_u_from_parent = None
        best_global_parent_id = None

        for global_id, id_in_cogmap in self.master_realisation.global_ids_to_locals.items():
            potential_parent_point = self.master_cogmap.get_point_by_event_id(id_in_cogmap)
            potential_u_from_parent = potential_parent_point - point
            if best_global_parent_id is None:
                best_u_from_parent = potential_u_from_parent
                best_global_parent_id = global_id
            else:
                if best_u_from_parent.norm() < potential_u_from_parent.norm():
                    best_u_from_parent = potential_u_from_parent
                    best_global_parent_id = global_id

        return best_global_parent_id, best_u_from_parent