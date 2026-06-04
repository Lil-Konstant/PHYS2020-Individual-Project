import numpy as np

def computeFluidMetrics(fluidState, epsilon):
    """
    Given a fluid state and a potential well depth, computes and returns a dict of speed, KE, reduced temp
    and reduced LJ temp
    """

    # Remove any bulk motion in the fluid in case there is any
    thermalVelocities = fluidState.velocities - np.mean(fluidState.velocities, axis=0)

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
    """
    Based on the initial setup state, estimate what the temperature should be - used for plotting and temps when sim isn't
    running
    """

    velocityStd = np.array(config["fluid_velocity_std"], dtype=float)
    reducedTemperature = (config["fluid_particle_mass"]* np.mean(velocityStd**2))
    reducedLJTemperature = reducedTemperature / config["LJ_epsilon"]
    return reducedTemperature, reducedLJTemperature