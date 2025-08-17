import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # gravity

# Function to simulate projectile motion
def projectile_motion(theta, v0, h0, t_max=10, dt=0.05):
    theta_rad = np.radians(theta)
    t = np.arange(0, t_max, dt)
    x = v0 * np.cos(theta_rad) * t
    y = h0 + v0 * np.sin(theta_rad) * t - 0.5 * g * t**2
    return x, y

# Function to check distance to target
def distance_to_target(x, y, target):
    valid_idx = np.where(y >= 0)  # only keep above ground
    if len(valid_idx[0]) == 0:
        return float("inf")
    x_valid, y_valid = x[valid_idx], y[valid_idx]
    dist = np.min(np.sqrt((x_valid - target[0])**2 + (y_valid - target[1])**2))
    return dist

# Theoretical max range (for feasibility check)
def max_range(v0, theta, h0):
    theta_rad = np.radians(theta)
    term = v0 * np.sin(theta_rad)
    discriminant = term**2 + 2 * g * h0
    if discriminant < 0:
        return 0
    t_flight = (term + np.sqrt(discriminant)) / g
    return v0 * np.cos(theta_rad) * t_flight

# Streamlit UI
st.title("🎯 Projectile Motion Simulator with AI Mode")

mode = st.radio("Choose Mode:", ["Manual Mode", "AI Mode"])

# ========== Manual Mode ==========
if mode == "Manual Mode":
    theta = st.number_input("Launch Angle (degrees)", 0, 90, 45)
    v0 = st.number_input("Initial Velocity (m/s)", 1.0, 100.0, 20.0)
    h0 = st.number_input("Initial Height (m)", 0.0, 50.0, 1.0)

    scale = st.slider("Plot Scale (m)", 10, 200, 50, step=10)

    if st.button("Simulate"):
        x, y = projectile_motion(theta, v0, h0)

        fig, ax = plt.subplots()
        ax.plot(x, y, label=f"θ={theta}°, v0={v0} m/s")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xlim(0, scale)
        ax.set_ylim(0, scale)
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_title("Projectile Motion (Manual Mode)")
        ax.legend()
        st.pyplot(fig)

# ========== AI Mode ==========
else:
    search_type = st.radio("Search Mode:", ["Fix Angle, Find Velocity", "Fix Velocity, Find Angle"])
    h0 = st.number_input("Initial Height (m)", 0.0, 50.0, 1.0)
    target_x = st.number_input("Target X position (m)", 0.0, 200.0, 30.0)
    target_y = st.number_input("Target Y position (m)", 0.0, 100.0, 5.0)
    scale = st.slider("Plot Scale (m)", 10, 200, 50, step=10)

    if search_type == "Fix Angle, Find Velocity":
        theta = st.number_input("Launch Angle (degrees)", 1, 89, 45)
        v_candidates = np.linspace(5, 100, 15)  # search space
    else:
        v0 = st.number_input("Initial Velocity (m/s)", 5.0, 100.0, 20.0)
        theta_candidates = np.linspace(5, 85, 15)  # search space

    if st.button("Run AI"):
        target = (target_x, target_y)
        best_dist = float("inf")
        best_x, best_y = None, None
        label_text = ""

        fig, ax = plt.subplots()

        impossible = False

        if search_type == "Fix Angle, Find Velocity":
            # Feasibility check: max range at high speed
            if target_x > max_range(200, theta, h0):
                impossible = True
            else:
                for i, v0_try in enumerate(v_candidates):
                    x, y = projectile_motion(theta, v0_try, h0)
                    dist = distance_to_target(x, y, target)
                    st.write(f"Attempt {i+1}: v0={v0_try:.2f} m/s, miss={dist:.2f}")
                    ax.plot(x, y, "--", color="gray", alpha=0.5)
                    if dist < best_dist:
                        best_dist = dist
                        best_x, best_y = x, y
                        label_text = f"θ={theta}°, v0={v0_try:.2f}"

        else:  # Fix velocity, find angle
            # Feasibility check: max range at 45°
            if target_x > max_range(v0, 45, h0):
                impossible = True
            else:
                for i, theta_try in enumerate(theta_candidates):
                    x, y = projectile_motion(theta_try, v0, h0)
                    dist = distance_to_target(x, y, target)
                    st.write(f"Attempt {i+1}: θ={theta_try:.1f}°, miss={dist:.2f}")
                    ax.plot(x, y, "--", color="gray", alpha=0.5)
                    if dist < best_dist:
                        best_dist = dist
                        best_x, best_y = x, y
                        label_text = f"θ={theta_try:.1f}°, v0={v0}"

        # Draw results
        ax.scatter(target_x, target_y, color="red", s=50, label="Target")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xlim(0, scale)
        ax.set_ylim(0, scale)
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_title(f"Projectile Motion (AI Mode - {search_type})")

        # If impossible, show warning
        if impossible or best_dist > 1.0:
            st.error("⚠️ Impossible to reach target with given parameters.")
        else:
            ax.plot(best_x, best_y, color="blue", linewidth=2, label=f"Best: {label_text}")
            st.success(f"✅ Best result: {label_text}, miss={best_dist:.2f} m")

        ax.legend()
        st.pyplot(fig)








