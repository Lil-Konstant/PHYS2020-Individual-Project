import numpy as np
from sim.ideal_interactions import handleInteractions as handleIdealInteractions
from sim.real_interactions import handleInteractions as handleRealInteractions

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

# Uses the given config dict to create N particles with random xy pos and vel, ensures they don't overlap
def initialise_fluid(config):
    N = config["N"]
    boxSize = config["box_size"]
    fluidRadius = config["fluid_particle_radius"]
    brownianRadius = config["brownian_particle_radius"]

    brownianPos = np.array(config["brownian_initial_position"], dtype=float)

    positions = []
    maxAttemptsPerParticle = 10000

    # Minimum allowed distances
    minFluidFluidDist = 2 * fluidRadius
    minBrownianFluidDist = brownianRadius + fluidRadius

    for _ in range(N):
        placed = False

        for _ in range(maxAttemptsPerParticle):
            candidate = np.random.rand(2) * boxSize

            # Keep fluid particle fully inside box
            if np.any(candidate < fluidRadius):
                continue

            if np.any(candidate > boxSize - fluidRadius):
                continue

            # Keep fluid particle outside Brownian particle
            distToBrownian = np.linalg.norm(candidate - brownianPos)

            if distToBrownian < minBrownianFluidDist:
                continue

            # Keep fluid particle away from already placed fluid particles
            if len(positions) > 0:
                existingPositions = np.array(positions)
                distances = np.linalg.norm(existingPositions - candidate, axis=1)

                if np.any(distances < minFluidFluidDist):
                    continue

            positions.append(candidate)
            placed = True
            break

        if not placed:
            raise RuntimeError(
                "Could not place all particles without overlap. "
                "Try reducing N, reducing particle radii, or increasing box_size."
            )

    positions = np.array(positions)
    velocities = config["fluid_velocity_std"] * np.random.randn(N, 2)

    # Force zero bulk fluid motion
    velocities -= np.mean(velocities, axis=0)

    return FluidState(
        positions,
        velocities,
        config["fluid_particle_mass"],
        fluidRadius
    )

def initialise_brownian_particle(config):
    return BrownianState(
        np.array(config["brownian_initial_position"], dtype=float),
        np.array(config["brownian_initial_velocity"], dtype=float),
        config["brownian_particle_mass"],
        config["brownian_particle_radius"]
    )

# Given a config and current state, compute the next euler step state over the config dt
def timeStep(fluidState, brownianState, config):
    dt = config["dt"]

    # Update each particle pos by its v*dt
    fluidState.positions += fluidState.velocities * dt
    brownianState.position += brownianState.velocity * dt

    if config["use_LJ_potential"]:
        handleRealInteractions(fluidState, brownianState, config)
    else:
        handleIdealInteractions(fluidState, brownianState, config)