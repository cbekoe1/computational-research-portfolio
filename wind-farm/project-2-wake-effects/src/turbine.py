class Turbine:
    def __init__(self, x, y, rotor_diameter, thrust_coefficient, rated_power_kw):
        self.x = x
        self.y = y
        self.D = rotor_diameter
        self.R = rotor_diameter / 2.0
        self.C_T = thrust_coefficient
        self.rated_power_kw = rated_power_kw

    def position(self):
        return (self.x, self.y)
