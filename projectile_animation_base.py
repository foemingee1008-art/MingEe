import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

g = 9.81  # gravity

def run_animation(theta_deg, v0, label="Projectile Motion"):
    theta = np.radians(theta_deg)

    # flight time
    t_flight = 2 * v0 * np.sin(theta) / g
    t = np.linspace(0, t_flight, 100)

    # trajectory
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2

    # velocity components
    vx = np.full_like(t, v0 * np.cos(theta))  # constant
    vy = v0 * np.sin(theta) - g * t

    # setup plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x) * 1.1)
    ax.set_ylim(0, max(y) * 1.2)
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    ax.set_title(label)

    traj_line, = ax.plot([], [], "b-", lw=2, label="Trajectory")
    point, = ax.plot([], [], "ro")
    arrow_vx = ax.arrow(0, 0, 0, 0, color="g", width=0.05)
    arrow_vy = ax.arrow(0, 0, 0, 0, color="r", width=0.05)

    def init():
        traj_line.set_data([], [])
        point.set_data([], [])
        return traj_line, point, arrow_vx, arrow_vy

    def update(i):
        point.set_data([x[i]], [y[i]])
        line.set_data(x[:i], y[:i])
        return line, point, velocity_arrow

        # clear previous arrows
        ax.patches.clear()

        # velocity component arrows
        ax.arrow(x[i], y[i], vx[i]*0.1, 0, color="g", width=0.05, head_width=0.3, label="vx" if i==0 else "")
        ax.arrow(x[i], y[i], 0, vy[i]*0.1, color="r", width=0.05, head_width=0.3, label="vy" if i==0 else "")

        return traj_line, point

    ani = animation.FuncAnimation(fig, update, frames=len(t), init_func=init, interval=50, blit=False, repeat=False)

    ax.legend()
    plt.show()

# 测试代码 (如果你直接运行这个文件，就会看到一条轨迹)
if __name__ == "__main__":
    run_animation(theta_deg=45, v0=20, label="Test Projectile Motion")
