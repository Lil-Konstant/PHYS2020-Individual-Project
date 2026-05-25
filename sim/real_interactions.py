import numpy as np
from scipy.spatial import KDTree

def calculateLJForce(position1, position2, velocity1, velocity2, mass1, mass2, radius1, radius2):
    force = 0

    return force

def handleInteractions(fluidState, brownianState):
    tree = KDTree(fluidState.positions)
    fluidPairIdxs = tree.query_pairs(r=2*fluidState.radius)