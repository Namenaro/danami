from globals import GLOBALS
from cogmap import Cogmap
from event import EventRealisation, EventMemory
from structure import structure_realisation, structure_memory
from samplers import fill_event_memory_naive


def init_struct():
    etalon_pic = GLOBALS.DATA.get_etalon()
    etalon_cogmap = Cogmap(etalon_pic)
    event_realisation, id_in_cogmap = etalon_cogmap.select_most_massive()
    etalon_cogmap.register_exclusion_event(id_in_cogmap)

    event_memory = EventMemory(event_realisation)
    fill_event_memory_naive(event_memory)  # ходим по контрасту, собираем выборки параметров события

    # создаем структуру c одним событием
    struct = StructureMemory()
    struct.set_first_event(event_memory)
    return struct