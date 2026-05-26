import numpy as np

def checkOverlap(position1, position2, radius1, radius2):
    return np.linalg.norm(position1 - position2) <= radius1 + radius2

# Reflects fluid and brownian particles off of boundary walls elastically
def handleBoundaries(fluidState, brownianState, boxSize):
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

# Ideal collisions between the brownian particle and all overlapping fluid particles
def performBrownianToFluidCollisions(fluidState, brownianState):
    for i in range(fluidState.N):
        if checkOverlap(brownianState.position, fluidState.positions[i], brownianState.radius, fluidState.radius):
            brownianState.position, fluidState.positions[i], brownianState.velocity, fluidState.velocities[i] = (
                calculateFinalVelocities(brownianState.position, fluidState.positions[i], brownianState.velocity,
                                         fluidState.velocities[i], brownianState.mass, fluidState.mass, brownianState.radius, fluidState.radius))