import numpy as np
from scipy.spatial import KDTree
from sim.collision import handleBoundaries, performBrownianToFluidCollisions

def getLJSigma_ff(fluidParticleRadius): return 2 * fluidParticleRadius
def getLJSigma_bf(fluidParticleRadius, brownianParticleRadius): return brownianParticleRadius + fluidParticleRadius
def getLJCutoff_ff(fluidParticleRadius): return 2.5 * getLJSigma_ff(fluidParticleRadius)
def getLJCutoff_bf(fluidParticleRadius, brownianParticleRadius): return 2.5 * getLJSigma_bf(fluidParticleRadius, brownianParticleRadius)

def calculateLJForce(position1, position2, epsilon, sigma):
    separation = position1-position2
    distance = np.linalg.norm(separation)

    if distance == 0:
        return np.zeros(2)

    return 24 * epsilon * ((2*sigma**12/distance**14) - (sigma**6/distance**8)) * separation

def calculateAccelerations(fluidState, brownianState, config):
    fluidParticleRadius = config["fluid_particle_radius"]
    brownianParticleRadius = config["brownian_particle_radius"]
    epsilon = config["LJ_epsilon"]

    fluidForces = np.zeros_like(fluidState.positions)
    brownianForce = np.zeros(2)

    # Fluid to fluid LJ forces
    tree = KDTree(fluidState.positions)
    fluidPairIdxs = tree.query_pairs(r=getLJCutoff_ff(fluidParticleRadius))
    for i, j in fluidPairIdxs:
        force = calculateLJForce(fluidState.positions[i], fluidState.positions[j], epsilon, getLJSigma_ff(fluidParticleRadius))
        fluidForces[i] += force
        fluidForces[j] -= force

    # Brownian to Fluid LJ forces, only if enabled
    if config["use_LJ_for_brownian_to_fluid"]:
        nearFluidIdxs = tree.query_ball_point(brownianState.position, r=getLJCutoff_bf(fluidParticleRadius, brownianParticleRadius))
        for i in nearFluidIdxs:
            forceOnBrownian = calculateLJForce(brownianState.position, fluidState.positions[i], epsilon, getLJSigma_bf(fluidParticleRadius, brownianParticleRadius))

            brownianForce += forceOnBrownian
            fluidForces[i] -= forceOnBrownian

    fluidAccelerations = fluidForces / fluidState.mass
    brownianAcceleration = brownianForce / brownianState.mass

    return fluidAccelerations, brownianAcceleration

def handleInteractions(fluidState, brownianState, config):
    dt = config["dt"]
    boxSize = config["box_size"]

    # Update positions using current acceleration
    accelerations, brownianAcceleration = calculateAccelerations(fluidState, brownianState, config)
    fluidState.positions += fluidState.velocities * dt + 0.5 * accelerations * dt**2
    brownianState.position += brownianState.velocity * dt + 0.5 * brownianAcceleration * dt**2

    # Handle any boundary collisions before recalculating acceleration
    handleBoundaries(fluidState, brownianState, boxSize)

    # Calculate new accelerations based on new positions
    nextAccelerations, nextBrownianAcceleration = calculateAccelerations(fluidState, brownianState, config)
    # Velocity verlet
    fluidState.velocities += 0.5*(accelerations + nextAccelerations)*dt
    brownianState.velocity += 0.5*(brownianAcceleration + nextBrownianAcceleration)*dt

    if not config["use_LJ_for_brownian_to_fluid"]:
        performBrownianToFluidCollisions(fluidState, brownianState)