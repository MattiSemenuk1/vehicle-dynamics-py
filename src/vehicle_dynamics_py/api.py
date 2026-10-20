from fastapi import FastAPI
from pydantic import BaseModel, Field
from vehicle_dynamics_py.params import VehicleParams
from vehicle_dynamics_py.bicycle import BicycleModel

app = FastAPI()

class SimRequest(BaseModel):
    vx: float = Field(gt=0)          # [m/s]
    delta: float                     # [rad]
    t_end: float = Field(gt=0)       # [s]
    params: VehicleParams = VehicleParams()

class SimResponse(BaseModel):
    t: list[float]
    r: list[float]
    r_ss_analytic: float

@app.post("/simulate", response_model=SimResponse)
def simulate(req: SimRequest):
    model = BicycleModel(req.params)                        # 1. build the model
    sol = model.simulate(req.vx, req.delta, req.t_end)      # 2. run it
    return SimResponse(                                     # 3. pack the answer
        t=sol.t.tolist(),
        r=sol.y[1].tolist(),                                # y[1] is yaw rate r
        r_ss_analytic=model.steady_state_yaw_rate(req.vx, req.delta),
    )

@app.get("/health")
def health():
    return {"status": "ok"}