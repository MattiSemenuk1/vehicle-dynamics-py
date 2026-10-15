import matplotlib.pyplot as plt

from vehicle_dynamics_py.params import VehicleParams
from vehicle_dynamics_py.bicycle import BicycleModel
from vehicle_dynamics_py.animation import VehicleAnimator


vx = 20.0
model = BicycleModel(VehicleParams())
sol = model.simulate(vx=vx, delta=0.02, t_end=10.0)

viz = VehicleAnimator(sol, vx=vx)
viz.animate()    # trajectory on top, speed and yaw rate below
plt.show()
