import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import matplotlib.transforms as mtransforms


class VehicleAnimator:
    def __init__(self, sol, vx: float, length: float = 4.5, width: float = 1.8):
        self.t = sol.t
        self.vy, self.r = sol.y[0], sol.y[1]
        self.psi, self.X, self.Y = sol.y[2], sol.y[3], sol.y[4]
        self.speed = np.sqrt(vx**2 + self.vy**2) * 3.6     # [km/h]
        self.length, self.width = length, width

    def animate(self, filename: str | None = None):
        fig = plt.figure(figsize=(8, 8))
        gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])
        ax_traj = fig.add_subplot(gs[0])
        ax_speed = fig.add_subplot(gs[1])
        ax_yaw = fig.add_subplot(gs[2], sharex=ax_speed)

        # trajectory: trail grows, car moves
        path, = ax_traj.plot([], [], "b-", lw=0.8)
        ax_traj.set_xlim(self.X.min() - 5, self.X.max() + 5)   # fixed limits: an empty
        ax_traj.set_ylim(self.Y.min() - 5, self.Y.max() + 5)   # line gives no autoscale
        ax_traj.set_aspect("equal")                            # 1 m = 1 m on both axes
        ax_traj.set_xlabel("Distance [m]")
        ax_traj.set_ylabel("Distance [m]")
        car = Rectangle((-self.length / 2, -self.width / 2),
                        self.length, self.width, fc="green", ec="k")
        ax_traj.add_patch(car)

        # signals: grow in time together with the car
        speed_line, = ax_speed.plot([], [])
        yaw_line, = ax_yaw.plot([], [])
        ax_speed.set_ylabel("Speed [km/h]")
        ax_yaw.set_ylabel("Yaw rate [rad/s]")
        ax_yaw.set_xlabel("Time [s]")
        for ax, data, min_margin in ((ax_speed, self.speed, 2.0), (ax_yaw, self.r, 1e-3)):
            margin = max(0.1 * (data.max() - data.min()), min_margin)
            ax.set_xlim(self.t[0], self.t[-1])
            ax.set_ylim(data.min() - margin, data.max() + margin)
        for ax in (ax_traj, ax_speed, ax_yaw):
            ax.grid(True)
        fig.tight_layout()

        def update(i):
            # rotate by psi, then move to (X, Y)
            tr = (mtransforms.Affine2D().rotate(self.psi[i])
                  .translate(self.X[i], self.Y[i]) + ax_traj.transData)
            car.set_transform(tr)
            path.set_data(self.X[:i + 1], self.Y[:i + 1])
            speed_line.set_data(self.t[:i + 1], self.speed[:i + 1])
            yaw_line.set_data(self.t[:i + 1], self.r[:i + 1])
            return (car, path, speed_line, yaw_line)

        frames = range(0, len(self.t), 10)                # every 10th step
        self.anim = FuncAnimation(fig, update, frames=frames, interval=30)
        if filename:
            self.anim.save(filename, writer="pillow")     # GIF for the README
