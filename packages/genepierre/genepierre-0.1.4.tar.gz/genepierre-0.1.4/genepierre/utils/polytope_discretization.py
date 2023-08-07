import itertools
import numpy as np
from scipy.spatial import ConvexHull


def generateUniformDirectionsOnCube(nbrStepsForEachDirection):
    """Creates points placed uniformly on the cube"""
    all_xs = np.linspace(-1, 1, nbrStepsForEachDirection)
    all_ys = np.linspace(-1, 1, nbrStepsForEachDirection)
    all_zs = np.linspace(-1, 1, nbrStepsForEachDirection)

    directions = [all_xs, all_ys, all_zs]
    all_directions = list(itertools.product(*directions))
    if (0, 0, 0) in all_directions:
        all_directions.remove((0, 0, 0))
    all_directions = np.array(all_directions)

    return all_directions


def intersectConvexHullWithDirection(hull, direction):
    """ The sense of the vector direction matters! """
    eq = hull.equations.T
    V, b = eq[:-1], eq[-1]
    alpha = -b/np.dot(V.T, direction)
    return np.min(alpha[alpha > 0]) * direction

def intersectPolytopeWithDirections(polytopeVertices, directions):
    """Give the intersection points in the order of the given directions"""
    hull = ConvexHull(points=polytopeVertices.T)

    pts = []
    for direction in directions:
        pt = intersectConvexHullWithDirection(hull, direction)
        pts.append(pt)
    pts = np.array(pts)

    return pts

def discretizeIn26Vertices(vertices):
    try:
        directions = generateUniformDirectionsOnCube(3)
        intersections = intersectPolytopeWithDirections(vertices, directions)
    except:
        intersections = np.zeros((26, 3))

    return intersections


def getDiscretizedNormVector26(vertices):
    """Discretize a polytope in 26 uniform directions then retrieve the norm of each new vertice"""
    vertices_disc = discretizeIn26Vertices(vertices)
    return np.linalg.norm(vertices_disc, axis=1)


def getEigenValuesVectors(A: np.ndarray):
    """From a list of vertices, returns the (normalized) axes of the ellipsoid (eigenvectors) and the eigen values associated
    obtained from covariance matrix.

    Args:
        A (np.ndarray): list of vertices (columns or rows)

    Returns:
        _type_: eigenvalues in decreasing order + associated eigenvectors as columns of v
    """

    cov = A@A.T
    v, w, _ = np.linalg.svd(cov)
    eigen_values = np.sqrt(w)
    eigen_vectors = v

    return eigen_values, eigen_vectors