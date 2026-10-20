from pydantic import BaseModel, Field

class VehicleParams(BaseModel):
    m: float = Field(default=1500, gt=0, description="mass [kg]")
    Iz: float = Field(default=2500, gt=0, description="yaw moment of inertia [kg*m^2]")
    a: float = Field(default=1.2, gt=0, description="distance from CG to front axle [m]")
    b: float = Field(default=1.8, gt=0, description="distance from CG to rear axle [m]")
    Cf: float = Field(default=80000, gt=0, description="front cornering stiffness [N/rad]")
    Cr: float = Field(default=80000, gt=0, description="rear cornering stiffness [N/rad]")

    @property
    def L(self) -> float:
        return self.a + self.b # wheelbase [m]

