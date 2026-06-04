from scipy.spatial import KDTree
from sim.collision import handleBoundaries, calculateFinalVelocities, performBrownianToFluidCollisions

def handleInteractions(fluidState, brownianState, config):
    """
    Called by the engine, spatial partitions the fluid based on fluid radius for collision range, conducts ideal
    reflection for colliding particles and updates velocities. Reflects any objects off of boundaries.
    """
    boxSize = config["box_size"]

    tree = KDTree(fluidState.positions)
    fluidPairIdxs = tree.query_pairs(r=2*fluidState.radius)

    # Collide all fluid particle pairs in collision range
    for i, j in fluidPairIdxs:
        fluidState.positions[i], fluidState.positions[j], fluidState.velocities[i], fluidState.velocities[j] = (
            calculateFinalVelocities(fluidState.positions[i], fluidState.positions[j], fluidState.velocities[i],
                                     fluidState.velocities[j], fluidState.mass, fluidState.mass, fluidState.radius, fluidState.radius))

    performBrownianToFluidCollisions(fluidState, brownianState)
    handleBoundaries(fluidState, brownianState, boxSize)