class EventRealisation:
    def __init__(self, zmeika_points, LUE):
        # данные по внутренней структуре события
        self.mass = len(zmeika_points)
        self.LUE = LUE

        self.zmeika_points = zmeika_points
