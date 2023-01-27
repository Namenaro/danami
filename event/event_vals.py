from event.event_params import *


# внутренние параметры события---------------------------------------------------------
class InnerEventVals:
    inner_functions = {INNER_PARAM_MASS: mass_function}

    def __init__(self):
        self.params_values_dict = {}  # {param_name: param_value}

    def fill(self, zmeyka):
        for param_name, func in self.inner_functions.items():
            self.params_values_dict[param_name] = func(zmeyka)


# параметры, характеризующие взаимойдействе события с другими событиями на карте--------
class OuterEventVals:
    outer_functions = {OUTER_PARAM_DU: du_function,
                       OUTER_PARAM_DX: dx_function}

    def __init__(self):
        self.params_values_dict = {}  # {param_name: param_value}

    def fill(self, u_err):
        for param_name, func in self.outer_functions.items():
            self.params_values_dict[param_name] = func(u_err)

