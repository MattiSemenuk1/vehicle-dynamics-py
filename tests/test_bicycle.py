from vehicle_dynamics_py.params import VehicleParams
from vehicle_dynamics_py.bicycle import BicycleModel



def test_steady_state_yaw_rate():
    model = BicycleModel(VehicleParams())
    vx, delta = 20.0, 0.02
    sol = model.simulate(vx, delta, 5.0) # 1. simulate
    r_sim = sol.y[1, -1] # 2. extract the final yaw rate from the simulation
    r_ss = model.steady_state_yaw_rate(vx, delta) # 3. compute the analytic steady-state yaw rate
    assert abs(r_sim - r_ss) / abs(r_ss) < 0.01 # 4. check that the two are close
    