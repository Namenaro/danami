from structure import StructureMemory, StructureRealisation, StructureTop
from globals import GLOBALS
from event import EventMemory, EventStat, InnerEventVals, OuterEventVals
from recogniser import RecogniserEngine, recognition_resume_for_top

def sample_top(structure, tops_list):
    events_stats = [EventStat() for _ in range(len(tops_list))]
    # перебираем контрастные когмапы
    contrast_cogmaps = GLOBALS.DATA.get_CONTRAST_train()
    for cogmap in contrast_cogmaps:
        engine = RecogniserEngine(structure, cogmap)
        best_realisation = engine.recognise()

        if len(best_realisation) == len(structure):
            for i in range(len(tops_list)):
                zmeyka, expected_point, real_point = \
                    recognition_resume_for_top(tops_list[i], best_realisation, cogmap)

                if zmeyka is not None:
                    u_err = real_point - expected_point
                    events_stats[i].add_realisation(zmeyka=zmeyka, u_err=u_err)

    events_memory_list = []
    for i in range(len(tops_list)):
        event_inner_vals = tops_list[i].inner_event_vals
        event_stat = events_stats[i]
        events_memory_list.append(EventMemory(event_vals=event_inner_vals, event_stat=event_stat))
    return events_memory_list



