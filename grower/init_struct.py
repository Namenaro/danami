from globals import GLOBALS
from cogmap import Cogmap
from event import EventMemory
from structure import StructureMemory, StructureRealisation
from samplers import fill_event_memory_naive


def init_struct(cogmap):
    print("Initialising structure by first event...")
    zmeyka, _ = cogmap.select_most_massive()

    event_memory = fill_event_memory_naive(zmeyka, sample_size=GLOBALS.CONTRAST_SAMPLE_LEN_FOR_STAT)  # ходим по контрасту, собираем выборки параметров события

    # создаем структуру c одним событием
    struct = StructureMemory()
    struct.set_first_event(event_memory)

    print("Structure initialised")
    return struct
