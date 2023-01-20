class EventRealisation:
    def __init__(self, zmeika_points, LUE, mass=None):
        # данные по внутренней структуре события
        if mass is not None:
            self.mass = mass
        else:
            self.mass = len(zmeika_points)
        self.LUE = LUE

        self.zmeika_points = zmeika_points

    def __str__(self):
        res = "EvRealis, LUE=" + str(self.LUE)+ ", mass=" + str(self.mass)
        return res
