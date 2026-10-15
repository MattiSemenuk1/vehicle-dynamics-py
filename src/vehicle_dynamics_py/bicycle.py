import numpy as np
from scipy.integrate import solve_ivp
from vehicle_dynamics_py.params import VehicleParams

class BicycleModel:
    def __init__(self, params: VehicleParams):
        self.p = params                    # store the parameters on the object

    def derivatives(self, t: float, x: np.ndarray, vx: float, delta: float) -> np.ndarray:
        vy, r, psi, X, Y = x
        p = self.p                         # short alias, so you can write p.m, p.Cf ...
        slip_angle_front = delta - (vy + p.a * r) / vx
        slip_angle_rear = - (vy - p.b * r) / vx
        Fyf = p.Cf * slip_angle_front
        Fyr = p.Cr * slip_angle_rear
        vy_dot = (Fyf + Fyr) / p.m - r * vx
        r_dot = (p.a * Fyf - p.b * Fyr) / p.Iz
        psi_dot = r
        X_dot = vx * np.cos(psi) - vy * np.sin(psi)
        Y_dot = vx * np.sin(psi) + vy * np.cos(psi)
        return np.array([vy_dot, r_dot, psi_dot, X_dot, Y_dot])
    
        return np.array([vy_dot, r_dot])

    def understeer_gradient(self) -> float:
        K = self.p.m / self.p.L * (self.p.b / self.p.Cf - self.p.a / self.p.Cr)  # K from self.p

        return K
    def steady_state_yaw_rate(self, vx: float, delta: float) -> float:
        K = self.understeer_gradient()

        r_ss = vx * delta / (self.p.L + K * vx**2)
                                   # analytic r_ss, uses self.understeer_gradient()
        return r_ss
    
    def simulate(self, vx: float, delta: float, t_end: float):
       return solve_ivp(self.derivatives, (0.0, t_end), np.zeros(5),
        args=(vx, delta), max_step=0.01)
