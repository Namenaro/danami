from structure import StructureMemory, StructureRealisation, StructureTop
from globals import GLOBALS
from event import EventMemory, EventStat, InnerEventVals, OuterEventVals
from recogniser import RecogniserEngine, recognition_resume_for_top

def sample_top(structure, top):
    event_stat = EventStat()

    # перебираем контрастные когмапы
    contrast_cogmaps = GLOBALS.DATA.get_CONTRAST_train()
    for cogmap in contrast_cogmaps:
        engine = RecogniserEngine(structure, cogmap)
        best_realisation = engine.recognise()

        if len(best_realisation) == len(structure):

            zmeyka, expected_point, real_point = \
                    recognition_resume_for_top(top, best_realisation, cogmap)

            if zmeyka is not None:
                u_err = real_point - expected_point
                event_stat.add_realisation(zmeyka=zmeyka, u_err=u_err)
    event_inner_vals = top.inner_event_vals
    event_memory = EventMemory(LUE=top.LUE_id, event_vals=event_inner_vals, event_stat=event_stat)
    return event_memory



