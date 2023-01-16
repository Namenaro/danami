from event.parameter import Parameter
from event.event_realisation import EventRealisation

class EventMemory:
    def __init__(self, event_realisation):
        self.LUE = event_realisation.LUE

        # эмпирические вероятности значений по всем независимым переменным, описывающим событие
        self.param_LUE = Parameter(expected_value=1, is_binary=True)
        self.param_mass = Parameter(expected_value=event_realisation.mass)
        self.param_u_dx = Parameter(expected_value=0)
        self.param_u_dy = Parameter(expected_value=0)

    # интерфейсные методы--------------------------------
    def set_samples(self, masses=None, u_dxs=None, u_dys=None, LUE_s=None):
        self.param_LUE.set_sample(LUE_s)
        self.param_mass.set_sample(masses)
        self.param_u_dx.set_sample(u_dxs)
        self.param_u_dy.set_sample(u_dys)

    def add_realisation_to_stat(self, event_realisation, u_dx, u_dy):
        if event_realisation is None:
            self.param_LUE.add_value(0)
        else:
            self.param_LUE.add_value(1)
            self.param_mass.add_value(event_realisation.mass)
            self.param_u_dx.add_value(u_dx)
            self.param_u_dy.add_value(u_dy)

    def eval_realisation(self, event_realisation, u_dx, u_dy):
        e = self.eval_mass(event_realisation.mass) + \
            self.eval_u_dx(u_dx) + \
            self.eval_u_dy(u_dy) + \
            self.eval_LUE()
        return e

    #-------------------------------------------------------
    # оценки вклада в нетривиальность от каждого параметра события
    # Эти методы вызываются только как служебные в функции eval_realisation
    def eval_mass(self, real_mass):
        e = 1 - self.param_mass.get_probability(real_mass, self.predicted_value)
        return e

    def eval_u_dx(self, real_u_dx):
        e = 1 - self.param_mass.get_probability(real_u_dx)
        return e

    def eval_u_dy(self, real_u_dy):
        e = 1 - self.param_mass.get_probability(real_u_dy)
        return e

    def eval_LUE(self):
        e = 1 - self.param_mass.get_probability(real_value=1)
        return e

    # Геттеры-------------------------------------
    def get_mass(self):
        return self.param_mass.expected_value

    def get_LUE(self):
        return self.LUE