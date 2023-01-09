from event import EventMemory,  EventRealisation
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

    def get_info_about_event(self, global_event_id):
        return  LUE_id, mass, parent_global_id, u_from_parent