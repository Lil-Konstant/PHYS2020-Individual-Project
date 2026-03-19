import numpy as np

class State:
    def __init__(self, positions, velocities, mass):
        self.positions = positions
        self.velocities = velocities
        self.mass = mass
        self.N = len(positions)

# Uses the given config dict to create N particles with random xy pos and vel
def initialise_particles(config):
    positions = np.random.rand(config["N"], 2) * config["box_size"]
    velocities = np.random.randn(config["N"], 2)

    # Create a state class with the generated xy pos and vels
    return State(positions, velocities, config["mass"])

# Given a config and current state, compute the next euler step state over the config dt
def timeStep(state, config):
    dt = config["dt"]
    boxSize = config["box_size"]

    # Update each particle pos by its v*dt
    state.positions += state.velocities * dt

    # Reflect any particles now hitting walls, in the x and y dimensions
    for dim in range(2):
        # Create a boolean mask of particles out of bounds (hitting walls)
        mask = (state.positions[:, dim] < 0) | (state.positions[:, dim] > boxSize)
        # Reflect the velocities of these particles hitting walls
        state.velocities[mask, dim] *= -1
        # Make sure all positions are still clamped in the box size range
        state.positions[:, dim] = np.clip(state.positions[:, dim], 0, boxSize)