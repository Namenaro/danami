from globals import GLOBALS
from cogmap import Cogmap
from event import EventRealisation, EventMemory
from structure import StructureMemory, StructureRealisation
from samplers import fill_event_memory_naive


def init_struct(cogmap):

    event_realisation, id_in_cogmap = cogmap.select_most_massive()

    event_memory = EventMemory(event_realisation)
    fill_event_memory_naive(event_memory, sample_size=GLOBALS.CONTRAST_SAMPLE_LEN_FOR_STAT)  # ходим по контрасту, собираем выборки параметров события

    # создаем структуру c одним событием
    struct = StructureMemory()
    struct.set_first_event(event_memory)

    # создаем мастер-реализацию
    ...
    return struct, master_realisation