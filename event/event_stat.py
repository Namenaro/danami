from event.event_params import *
from event.event_vals import OuterEventVals, InnerEventVals
from event.hist import Hist


class EventStat:
    def __init__(self):
        self.inner_hists = {}  # param_name: hist_obj
        self.outer_hists = {}

        for param_name in InnerEventVals.inner_functions.keys:
            self.inner_hists[param_name] = Hist()

        for param_name in OuterEventVals.outer_functions.keys:
            self.outer_hists[param_name] = Hist()


    def add_realisation(self, zmeyka, u_err):
        for param_name, func in InnerEventVals.inner_functions.items():
            self.inner_hists[param_name].add(func(zmeyka))

        for param_name in OuterEventVals.outer_functions.keys:
            self.outer_hists[param_name].add(func(u_err))
