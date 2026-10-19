A 2-DOF bicycle model in
Python whose simulated steady-state yaw rate matches the analytic understeer-gradient value
to better than 0.001%.

Model can be run with few commands, such as:
- uv sync
- uv run pytest
- uv run python examples/step_steer.py

![Step steer response:
trajectory, speed and yaw rate](docs/step_steer.gif)