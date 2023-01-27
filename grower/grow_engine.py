from structure import StructureTop, StructureMemory, StructureRealisation
from samplers import sample_top, StatObject, fill_event_memory_naive
from globals import GLOBALS


class GrowEngine:
    def __init__(self, master_struct, master_realisation):
        self.master_structure = master_struct
        self.master_realisation = master_realisation

        self.growing_structure = StructureMemory()
        self.growing_realisation = StructureRealisation()

        self._grow_first_step()

        self.stat_object = StatObject(self.growing_structure)
        self.stat_object.fill()


    def grow_step(self):
        SUCCESS = True
        FAIL = False

        num_step = len(self.master_realisation)
        global_event_id = self.master_structure.recognition_order[num_step]

        top = self._init_top_for_struct(global_event_id)
        event_memory = sample_top(self.growing_structure, [top])[0]

        if event_memory.has_empty_hists():
            return FAIL

        self.growing_structure.add_new_event(event_memory,
                                             u_from_parent=top.u_from_parent,
                                             parent_global_id=top.global_parent_id,
                                             is_linked_to_parent=top.is_linked_to_parent)

        self.growing_realisation.add_new_check_result(global_id=global_event_id,
                                                      id_in_cogmap=self.master_realisation.get_local_id_by_global(
                                                          global_event_id))

        self.stat_object = StatObject(self.growing_structure)
        self.stat_object.fill()

        return SUCCESS

    def _init_top_for_struct(self, global_event_id):
        LUE, inner_params_vals, parent_global_id, u_from_parent = self.master_structure.get_info_about_event(
            global_event_id)
        is_linked_to_parent = self.master_structure.is_linked_to_parent(global_event_id)
        top = StructureTop(u_from_parent,
                           global_parent_id=parent_global_id,
                           LUE=LUE,
                           is_linked_to_parent=is_linked_to_parent,
                           inner_event_vals=inner_params_vals)
        return top

    def _grow_first_step(self):
        print("Initialising structure by first event...")
        # ходим по контрасту, собираем выборки параметров события
        global_event_id = self.master_structure.recognition_order[0]
        LUE, inner_params_vals, parent_global_id, u_from_parent = self.master_structure.get_info_about_event(
            global_event_id)
        event_memory = fill_event_memory_naive(inner_event_vals=inner_params_vals,
                                               LUE=LUE,
                                               sample_size=GLOBALS.CONTRAST_SAMPLE_LEN_FOR_STAT)

        self.growing_structure.set_first_event(event_memory)
        self.growing_realisation.add_new_check_result(global_id=global_event_id,
                                                      id_in_cogmap=self.master_realisation.get_local_id_by_global(
                                                          global_event_id))
        print("Structure initialised")

