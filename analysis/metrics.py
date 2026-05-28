import numpy as np

def computeFluidMetrics(fluidState, epsilon):
    thermalVelocities = fluidState.velocities - np.mean(fluidState.velocities, axis=0) # Remove any bulk motion in the fluid

    speeds = np.linalg.norm(thermalVelocities, axis=1)
    averageKineticEnergy = 0.5 * fluidState.mass * np.mean(speeds**2)
    reducedTemperature = averageKineticEnergy # in units of k (boltzmann not Kelvin)

    return {
        "speeds": speeds,
        "kinetic_energy": averageKineticEnergy,
        "reduced_temperature": reducedTemperature,
        "reduced_LJ_temperature": reducedTemperature / epsilon
    }

def estimateConfiguredTemperatures(config):
    velocityStd = np.array(config["fluid_velocity_std"], dtype=float)
    reducedTemperature = (config["fluid_particle_mass"]* np.mean(velocityStd**2))
    reducedLJTemperature = reducedTemperature / config["LJ_epsilon"]
    return reducedTemperature, reducedLJTemperature