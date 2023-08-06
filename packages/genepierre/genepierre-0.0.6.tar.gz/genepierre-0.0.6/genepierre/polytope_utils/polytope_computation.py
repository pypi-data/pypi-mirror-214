import numpy as np
import biorbd
import pycapacity.human as capacity
import identification_study.utils.model_computation as mcomp
from pycapacity.algorithms import iterative_convex_hull_method

def getPolytope(model: biorbd.Model, Q: np.ndarray, bodyName: str, endEffector: list, tol=1, withBias: bool = True, name: str = None) -> dict:
    zeros = np.zeros(model.nbQ())

    model.updateMuscles(Q, True)
    model.UpdateKinematicsCustom(Q, zeros, zeros)

    t_min, t_max = mcomp.getMuscleTensions(model)
    N = -mcomp.getMomentArmMatrix(model, Q).T
    J = mcomp.getStationJacobian(model, Q, bodyName, endEffector)

    error = False
    vertices = np.array([])
    face_indices = np.array([])
    muscle_force_vertices = np.array([])
    try:
        if withBias:
            Tau_grav = model.InverseDynamics(Q, zeros, zeros)
            pol = capacity.force_polytope(
                J, N, t_min, t_max, tol, -Tau_grav.to_array(), options = { "calculate_faces": True })
            vertices = pol.vertices
            face_indices = pol.face_indices
            muscle_force_vertices = pol.mucsle_force_vertices
        else:
            pol = capacity.force_polytope(
                J, N, t_min, t_max, tol, options = { "calculate_faces": True })
            vertices = pol.vertices
            face_indices = pol.face_indices
    except Exception as e:
        # print("Error in polytope computation.")
        # print(e.args)
        error = True

    toReturn = {
        "name": name,
        "error": error,
        "J": J,
        "N": N,
        "t_min": t_min,
        "t_max": t_max,
        "tol": tol,
        "vertices": vertices,
        "face_indices": face_indices,
        "muscle_force_vertices": muscle_force_vertices
    }
    return toReturn


def getPolytopeInDirection(model: biorbd.Model, Q: np.ndarray, bodyName: str, endEffector: list, direction: np.ndarray, tol=1, withBias: bool = True, name: str = None) -> dict:
    zeros = np.zeros(model.nbQ())

    model.updateMuscles(Q, True)
    model.UpdateKinematicsCustom(Q, zeros, zeros)

    t_min, t_max = mcomp.getMuscleTensions(model)
    N = -mcomp.getMomentArmMatrix(model, Q).T
    J = mcomp.getStationJacobian(model, Q, bodyName, endEffector)

    error = False
    vertices = np.array([])
    face_indices = np.array([])
    try:
        if withBias:
            Tau_grav = model.InverseDynamics(Q, zeros, zeros)
            vertices, H, d, face_indices, _, _ = iterative_convex_hull_method(direction@J.T, N, t_min, t_max, tol, -Tau_grav.to_array())
            # vertices, H, d, face_indices = capacity.force_polytope(
            #     direction@J, N, t_min, t_max, tol, -Tau_grav.to_array())
        else:
            # vertices, H, d, face_indices = capacity.force_polytope(
            #     J, N, t_min, t_max, tol)
            vertices, H, d, face_indices, _, _ = iterative_convex_hull_method(direction@J.T, N, t_min, t_max, tol)
    except Exception as e:
        # print("Error in polytope computation.")
        # print(e.args)
        error = True

    toReturn = {
        "name": name,
        "error": error,
        "J": J,
        "N": N,
        "t_min": t_min,
        "t_max": t_max,
        "tol": tol,
        "vertices": vertices,
        "face_indices": face_indices
    }
    return toReturn