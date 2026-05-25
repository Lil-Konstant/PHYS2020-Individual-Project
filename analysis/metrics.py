import numpy as np
import sim.constants as constants

def computeFluidMetrics(fluidState):
    thermalVelocities = fluidState.velocities - np.mean(fluidState.velocities, axis=0) # Remove any bulk motion in the fluid

    speeds = np.linalg.norm(thermalVelocities, axis=1)
    averageKineticEnergy = 0.5 * fluidState.mass * np.mean(speeds**2)
    reducedTemperature = averageKineticEnergy # in units of k (boltzmann not Kelvin)

    return {
        "speeds": speeds,
        "kinetic_energy": averageKineticEnergy,
        "reduced_temperature": reducedTemperature,
        "reduced_LJ_temperature": reducedTemperature / constants.LJ_epsilon
    }