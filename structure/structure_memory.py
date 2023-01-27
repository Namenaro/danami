from event import EventMemory
from globals import GLOBALS


# Хранит глобальные айдишники выученных событий и относительные управления между ними.
# порядок разпознавания


class StructureMemory:
    def __init__(self):
        self.events = {}  # {global_id: EventMemory}
        self.recognition_order = []  # [global_id_1, ..., global_id_n]
        self.child_to_parent = {}  # {child_global_id: parent_id}
        self.us_from_parent_to_child = {}  # {(parent_id, child_id): u}
        self.linked_pairs = {}  # {first_global_node_id: second_global_node_id}

    def __len__(self):
        return len(self.recognition_order)

    def get_all_global_ids(self):
        return self.recognition_order

    def get_info_about_event(self, global_event_id):
        event_memory = self.events[global_event_id]
        LUE = event_memory.LUE
        inner_params_vals = event_memory.get_inner_vals_expected()

        parent_global_id = self.child_to_parent[global_event_id]
        u_from_parent = None  # это может быть первый узел, и тогда родителя у него нет
        if parent_global_id is not None:
            u_from_parent = self.us_from_parent_to_child[(parent_global_id, global_event_id)]
        return LUE, inner_params_vals, parent_global_id, u_from_parent

    def add_new_event(self, event_memory, u_from_parent, parent_global_id, is_linked_to_parent):
        global_id = GLOBALS.GLOBAL_IDS_GEN.generate_id()

        self.events[global_id] = event_memory
        self.recognition_order.append(global_id)
        self.child_to_parent[global_id] = parent_global_id
        self.us_from_parent_to_child[(parent_global_id, global_id)] = u_from_parent
        if is_linked_to_parent:
            self.linked_pairs[global_id] = parent_global_id
            self.linked_pairs[parent_global_id] = global_id

    def get_event_memory_obj(self, global_id):
        return self.events[global_id]

    def get_linked_to_this_event(self, this_event_global_id):
        return self.linked_pairs.get(this_event_global_id, None)

    def get_first_event_id(self):
        global_id = self.recognition_order[0]
        return global_id

    def set_first_event(self, event_memory, global_id):
        self.child_to_parent[global_id] = None
        self.us_from_parent_to_child[(None, global_id)] = None
        self.recognition_order.append(global_id)
        self.events[global_id] = event_memory

    def is_event_first(self, this_event_global_id):
        if self.recognition_order[0] == this_event_global_id:
            return True
        return False

    def get_parent_id(self, child_global_id):
        return self.child_to_parent[child_global_id]

    def get_u_from_parent(self, child_global_id):
        global_parent_id = self.get_parent_id(child_global_id)
        return self.us_from_parent_to_child[(global_parent_id, child_global_id)]