from structure import StructureMemory, StructureRealisation, StructureTop
from globals import GLOBALS
from event import EventMemory, EventRealisation

def sample_top(structure, structure_top):
    # перебираем контрастные когмапы
    # на каждой распознаем структуру и относительно нее событие на карте
    # для этого события замеряем dx dy (заносим в выборку)
    # массу (заносим в выборку)
    #  а также бинарный факт о нахождении искомого ЛУЕ

    # имея эти выборки, создаем EventMemory, в качестве реализации задаем данные из top (просто без змейки)
    #  и заполянем его выборками
    return event_memory