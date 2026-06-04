import numpy as np
from sim.ideal_interactions import handleInteractions as handleIdealInteractions
from sim.real_interactions import handleInteractions as handleRealInteractions

class FluidState:
    """
    Uses a list for [x,y] positions and [vx, vy] velocities, each row (first index) corresponds to a particles data.
    Stores mass and radius shared by fluid particles, and number of them
    """
    def __init__(self, positions, velocities, mass, radius):
        self.positions = positions
        self.velocities = velocities
        self.mass = mass
        self.radius = radius
        self.N = len(positions)

class BrownianState:
    """
    Stores position as [x,y] and velocity as [vx, vy].
    """
    def __init__(self, position, velocity, mass, radius):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.radius = radius

# Uses the given config dict to create N particles with random xy pos and vel, ensures they don't overlap
def initialiseFluid(config):
    """
    Initialises a fluid of N particles, tracked by a FluidState class, uses config for fluid size, number and placement
    :param config:
    :return:
    """
    N = config["N"]
    boxSize = config["box_size"]
    fluidRadius = config["fluid_particle_radius"]
    brownianRadius = config["brownian_particle_radius"]

    # Store where the brownian will be to avoid placing overlap
    brownianPos = np.array([config["box_size"]/2, config["box_size"]/2], dtype=float)

    positions = []
    maxAttemptsPerParticle = 10000

    # Minimum allowed distances
    minFluidFluidDist = 2 * fluidRadius
    minBrownianFluidDist = brownianRadius + fluidRadius

    # For each particle, keep trying to find a position to place that isn't already occupied
    for _ in range(N):
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

            # If all checks are passed, place this particle here
            positions.append(candidate)
            break

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

def initialiseBrownianParticle(config):
    return BrownianState(
        np.array([config["box_size"]/2, config["box_size"]/2], dtype=float),
        np.array(config["brownian_initial_velocity"], dtype=float),
        config["brownian_particle_mass"],
        config["brownian_particle_radius"]
    )

def timeStep(fluidState, brownianState, config):
    """
    Given a config and current state, compute the next euler step state over the config dt. Conduct particle interactions
    based on if ideal or non-ideal.
    """
    dt = config["dt"]

    # Update each particle pos by its v*dt
    fluidState.positions += fluidState.velocities * dt
    brownianState.position += brownianState.velocity * dt

    if config["use_LJ_potential"]:
        handleRealInteractions(fluidState, brownianState, config)
    else:
        handleIdealInteractions(fluidState, brownianState, config)

# Runs a single simulation given the config, and a random seed
# Returns the time history of squared displacements of the brownian particle
def runSingleSimulationSquaredDisplacement(config, seed=None):
    """
    # Runs a single simulation given the config, and a random seed. Returns the time history of squared displacements
    of the brownian particle
    """
    # If given a seed, use it to seed numpy rand
    if seed is not None:
        np.random.seed(seed)

    brownianState = initialiseBrownianParticle(config)
    fluidState = initialiseFluid(config)
    brownianPositions = []

    for _ in range(config["steps"]):
        timeStep(fluidState, brownianState, config)
        brownianPositions.append(brownianState.position.copy())

    positions = np.array(brownianPositions)
    initialPosition = positions[0]
    displacements = positions - initialPosition
    squaredDisplacements = np.sum(displacements**2, axis=1)

    return squaredDisplacements