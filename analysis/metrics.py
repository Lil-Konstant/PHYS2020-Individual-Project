import numpy as np

def compute_metrics(state):
    speeds = np.linalg.norm(state.velocities, axis=1)
    kinetic_energy = 0.5 * state.mass * np.mean(speeds**2)

    return {
        "speeds": speeds,
        "kinetic_energy": kinetic_energy
    }