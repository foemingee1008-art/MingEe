import numpy as np
import pandas as pd

g = 9.81  # gravitational acceleration

# generate data
rows = []
for _ in range(5000):
    theta_deg = np.random.uniform(10, 80)     # shooting angle
    v0 = np.random.uniform(5, 50)            # initial velocity
    theta = np.radians(theta_deg)

    t_flight = 2 * v0 * np.sin(theta) / g
    t = np.linspace(0, t_flight, num=50)

    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2

    rows.append([theta_deg, v0, x[-1], y[-1]])  # final point

data = pd.DataFrame(rows, columns=["theta_deg", "v0", "X", "Y"])
data.to_csv("projectile_data.csv", index=False)

print("✅ Data generated and saved as projectile_data.csv")
