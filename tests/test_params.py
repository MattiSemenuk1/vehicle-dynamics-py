import pytest
from pydantic import ValidationError
from vehicle_dynamics_py.params import VehicleParams

def test_negative_mass_rejected():
    with pytest.raises(ValidationError):
        VehicleParams(m=-1)  # mass cannot be negative