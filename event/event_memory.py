from event.parameter import Parameter

class EventMemory:
    def __init__(self, event_realisation):
        self.LUE = event_realisation.LUE

        # эмпирические вероятности значений по всем вариабельным переменным, описывающим событие
        self.param_LUE = Parameter(expected_value=1, is_binary=True)
        self.param_mass = Parameter(event_realisation.mass)
        self.param_u_dx = Parameter(expected_value=0)
        self.param_u_dy = Parameter(expected_value=0)


    def set_samples(self, masses=None, u_dxs=None, u_ys=None, LUE_s=None):
        pass

    def eval_realisation(self, event_realisation):  # самый важный интерфейсный метод
        pass

    def eval_mass(self, real_mass):
        pass

    def eval_u_dx(self, real_u_dx):
        pass

    def eval_u_dy(self, real_u_dy):
        pass

    def eval_LUE(self):
        pass