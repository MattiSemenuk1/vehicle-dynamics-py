from fastapi.testclient import TestClient
from vehicle_dynamics_py.api import app

client = TestClient(app)

def test_simulate_matches_analytic():
    resp = client.post("/simulate", json={"vx": 20, "delta": 0.05, "t_end": 5})
    assert resp.status_code == 200
    body = resp.json()
    r_sim = body["r"][-1]            # last simulated yaw rate
    r_ss = body["r_ss_analytic"]
    assert abs(r_sim - r_ss) / abs(r_ss) < 0.01 # 4. check that the two are close


def test_negative_speed_rejected():
    resp = client.post("/simulate", json={"vx": -20, "delta": 0.05, "t_end": 5})
    assert resp.status_code == 422