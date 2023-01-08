from event import EventMemory,  EventRealisation
from globals import GLOBAL_IDS_GEN

# Хранит глобальные айдишники выученных событий и относительные управления между ними.
# порядок разпознавания
class StructureMemory:
    def __init__(self):
        self.events = {}  # {global_id: EventMemory}
        self.events_coords = {}  # координаты в относительной ск относительно центра конструкции
        self.recognition_order = []  # [global_id_1, ..., global_id_n]
        self.events_addrs = {} # {global_id: global_id} # относительно какого события считать это при распознавании

    def get_u(self, id_from, id_to):
        point_to = self.events_coords[id_to]
        point_from = self.events_coords[id_from]
        u = point_to - point_from
        return u

    def add_node(self, event_memory, u, id_parent):
        global_id = GLOBAL_IDS_GEN.generate_id()

        self.events[global_id] = event_memory
        self.recognition_order.append(global_id)
        self.events_coords[global_id] = self.events_coords[id_parent] + u
        self.events_addrs[global_id] = id_parent

        self._recalc_coords()


    def __len__(self):
        return len(self.events)


    def recalc_coords(self):
        # перемещаем центр СК в центр масс структуры