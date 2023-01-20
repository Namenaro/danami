from structure import StructureMemory, StructureRealisation, StructureTop
from globals import GLOBALS
from event import EventMemory, EventRealisation
from recogniser import RecogniserEngine, recognition_resume_for_top

def sample_top(structure, tops_list):
    event_memory_list = [_top_to_dammy_event_memory(top) for top in tops_list]

    # перебираем контрастные когмапы
    contrast_cogmaps = GLOBALS.DATA.get_CONTRAST_train()
    for cogmap in contrast_cogmaps:
        engine = RecogniserEngine(structure, cogmap)
        best_realisation = engine.recognise()

        if len(best_realisation) == len(structure):

            for i in range(len(tops_list)):
                event_local_id, event_realisation, expected_point, real_point = \
                    recognition_resume_for_top(tops_list[i], best_realisation, cogmap)

                if event_realisation is None:
                    event_memory_list[i].add_realisation_to_stat(None, u_dx=None, u_dy=None)
                else:
                    du = real_point - expected_point
                    u_dx = du.x
                    u_dy = du.y
                    event_memory_list[i].add_realisation_to_stat(event_realisation, u_dx=u_dx, u_dy=u_dy)

    return event_memory_list


def _top_to_dammy_event_memory(top):
    master_realisation = EventRealisation(zmeika_points=None, LUE=top.LUE_id, mass=top.mass)
    event_memory = EventMemory(master_realisation)
    return event_memory
