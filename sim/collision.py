import numpy as np
from scipy.spatial import KDTree

def checkOverlap(position1, position2, radius1, radius2):
    return np.linalg.norm(position1 - position2) <= radius1 + radius2

def calculateFinalVelocities(position1, position2, velocity1, velocity2, mass1, mass2, radius1, radius2):
    r = position1 - position2
    dist = np.linalg.norm(r)

    # avoid divide-by-zero
    if dist == 0:
        return position1, position2, velocity1, velocity2

    n = r / dist
    v_rel = velocity1 - velocity2
    v_rel_n = np.dot(v_rel, n)

    # if separating, no collision
    if v_rel_n > 0:
        return position1, position2, velocity1, velocity2

    # update velocities
    j = -(2 * v_rel_n) / (1 / mass1 + 1 / mass2)
    velocity1_new = velocity1 + (j / mass1) * n
    velocity2_new = velocity2 - (j / mass2) * n

    # fix overlaps
    overlap = max(radius1 + radius2 - dist, 0)
    correction1 = (mass2 / (mass1 + mass2)) * overlap * n
    correction2 = (mass1 / (mass1 + mass2)) * overlap * n
    position1_new = position1 + correction1
    position2_new = position2 - correction2

    return position1_new, position2_new, velocity1_new, velocity2_new

def handleCollisions(fluidState, brownianState):
    tree = KDTree(fluidState.positions)
    fluidPairIdxs = tree.query_pairs(r=2*fluidState.radius)

    # Collide all fluid particle pairs in collision range
    for i, j in fluidPairIdxs:
        # if checkOverlap(fluidState.positions[i], fluidState.positions[j], fluidState.radius, fluidState.radius):
        fluidState.positions[i], fluidState.positions[j], fluidState.velocities[i], fluidState.velocities[j] = (
            calculateFinalVelocities(fluidState.positions[i], fluidState.positions[j], fluidState.velocities[i],
                                     fluidState.velocities[j], fluidState.mass, fluidState.mass, fluidState.radius, fluidState.radius))

    # Now check the brownian against all fluid particles once each for collision with the medium
    for i in range(fluidState.N):
        if checkOverlap(brownianState.position, fluidState.positions[i], brownianState.radius, fluidState.radius):
            brownianState.position, fluidState.positions[i], brownianState.velocity, fluidState.velocities[i] = (
                calculateFinalVelocities(brownianState.position, fluidState.positions[i], brownianState.velocity,
                                         fluidState.velocities[i], brownianState.mass, fluidState.mass, brownianState.radius, fluidState.radius))