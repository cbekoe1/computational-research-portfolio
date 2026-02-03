import math
from .turbine import Turbine
from .wake_model import velocity_deficit, is_in_wake

class WindFarm:
    def __init__(self, turbines, U_inf, k, air_density=1.225):
        """
        turbines: list of Turbine objects
        U_inf: free-stream wind speed [m/s]
        k: wake expansion coefficient
        """
        self.turbines = turbines
        self.U_inf = U_inf
        self.k = k
        self.air_density = air_density

    def _upstream_turbines(self, idx):
        """
        Return turbines that are upstream of turbine idx
        (wind from left to right: smaller x is upstream).
        """
        x_target = self.turbines[idx].x
        return [t for t in self.turbines if t.x < x_target]

    def effective_wind_speed_at(self, idx):
        """
        Compute effective wind speed at turbine idx
        using root-sum-square of velocity deficits.
        """
        target = self.turbines[idx]
        U_inf = self.U_inf
        deficits = []

        for up in self._upstream_turbines(idx):
            if is_in_wake(target.x, target.y, up.x, up.y, up.R, self.k):
                dx = target.x - up.x
                dU = velocity_deficit(dx, U_inf, up.C_T, up.R, self.k) * U_inf
                deficits.append(dU)

        if not deficits:
            return U_inf

        # Root-sum-square combination
        total_deficit = math.sqrt(sum(dU ** 2 for dU in deficits))
        U_eff = max(U_inf - total_deficit, 0.0)
        return U_eff

    def power_at(self, idx):
        """
        Very simple power model: P ~ U^3, capped at rated power.
        """
        t = self.turbines[idx]
        U_eff = self.effective_wind_speed_at(idx)
        # Reference: rated power at 12 m/s (example)
        U_ref = 12.0
        if U_eff <= 0:
            return 0.0

        P_ref = t.rated_power_kw
        P = P_ref * (U_eff / U_ref) ** 3
        return min(P, t.rated_power_kw)

    def farm_power(self):
        return sum(self.power_at(i) for i in range(len(self.turbines)))
