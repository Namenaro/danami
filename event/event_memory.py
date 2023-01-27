from event.event_vals import OuterEventVals, InnerEventVals
from event.event_stat import EventStat
from common_utils import Point


class EventMemory:
    def __init__(self, LUE, event_vals, event_stat):
        self.LUE = LUE

        self.inner_event_vals = event_vals
        self.event_stat = event_stat

    def eval_realisation(self, zmeyka, u_err):
        inner = self.eval_realisation_inner(zmeyka)
        outer = self.eval_realisation_outer(u_err)
        return inner + outer

    def eval_realisation_inner(self, zmeyka):
        event_vals = InnerEventVals()
        event_vals.fill(zmeyka)

        e = 0
        for param_name, hist in self.event_stat.inner_hists.items():
            real_val = event_vals.params_values_dict[param_name]
            expected_val = self.inner_event_vals.params_values_dict[param_name]
            param_e = hist.get_probability_of_event(real_value=real_val, predicted_value=expected_val)
            e+=param_e
        return e

    def eval_realisation_outer(self, u_err):
        if u_err is None:
            return 0  # если событие первое, то известные внешние связи отсутсвуют

        event_vals = OuterEventVals()
        event_vals.fill(u_err)
        e = 0
        for param_name, hist in self.event_stat.outer_hists.items():
            real_val = event_vals.params_values_dict[param_name]
            expected_val = self.inner_event_vals.params_values_dict[param_name]
            param_e = hist.get_probability_of_event(real_value=real_val, predicted_value=expected_val)
            e += param_e
        return e

    def get_inner_vals_expected(self):
        return self.inner_event_vals.params_values_dict
