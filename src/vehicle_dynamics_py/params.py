from dataclasses import dataclass

@dataclass
class VehicleParams:
    m: float = 1500 # mass [kg]
    Iz: float = 2500 # yaw moment of inertia [kg*m^2]
    a: float = 1.2# distance from CG to front axle [m]
    b: float = 1.8 # distance from CG to rear axle [m]
    Cf: float = 80000 # front cornering stiffness [N/rad]
    Cr: float = 80000 # rear cornering stiffness [N/rad])
    
    @property
    def L(self) -> float:
        return self.a + self.b # wheelbase [m]

