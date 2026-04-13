import numpy as np
from sim.collision import handleCollisions

class FluidState:
    def __init__(self, positions, velocities, mass, radius):
        self.positions = positions
        self.velocities = velocities
        self.mass = mass
        self.radius = radius
        self.N = len(positions)

class BrownianState:
    def __init__(self, position, velocity, mass, radius):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.radius = radius

# Uses the given config dict to create N particles with random xy pos and vel
def initialise_particles(config):
    positions = np.random.rand(config["N"], 2) * config["box_size"]
    velocities = config["fluid_velocity_std"] * np.random.randn(config["N"], 2) + config["fluid_velocity_mean"]

    # Create a state class with the generated xy pos and vels
    return FluidState(positions, velocities, config["fluid_particle_mass"], config["fluid_particle_radius"])

def initialise_brownian_particle(config):
    startingPos = config["brownian_initial_position"]
    startingPos = [config["box_size"]/2, config["box_size"]/2]
    return BrownianState(startingPos, config["brownian_initial_velocity"], config["brownian_particle_mass"], config["brownian_particle_radius"])

# Given a config and current state, compute the next euler step state over the config dt
def timeStep(fluidState, brownianState, config):
    dt = config["dt"]
    boxSize = config["box_size"]

    # Update each particle pos by its v*dt
    fluidState.positions += fluidState.velocities * dt
    brownianState.position += brownianState.velocity * dt

    # Resolve fluid-fluid and fluid-brownian collisions
    handleCollisions(fluidState, brownianState)

    # Reflect any particles now hitting walls, in the x and y dimensions
    for dim in range(2):
        # Create a boolean mask of particles out of bounds (hitting walls)
        mask = (fluidState.positions[:, dim] - fluidState.radius  < 0) | (fluidState.positions[:, dim] + fluidState.radius > boxSize)
        # Reflect the velocities of these particles hitting walls
        fluidState.velocities[mask, dim] *= -1
        # Make sure all positions are still clamped in the box size range
        fluidState.positions[:, dim] = np.clip(fluidState.positions[:, dim], 0 + fluidState.radius, boxSize - fluidState.radius)

        # Do the same for the brownian particle
        outOfBounds = (brownianState.position[dim] - brownianState.radius < 0) | (brownianState.position[dim] + brownianState.radius > boxSize)
        if outOfBounds:
            brownianState.velocity[dim] *= -1