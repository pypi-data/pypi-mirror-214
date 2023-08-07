import numpy as np
import biorbd


def getModelAsVector(model: biorbd.Model) -> list:
    vec = []
    for m in range(model.nbMuscles()):
        muscle = model.muscle(m)
        c = muscle.characteristics()
        vec.append(c.forceIsoMax())
        vec.append(c.optimalLength())
        vec.append(c.tendonSlackLength())

        g = muscle.position()
        o = g.originInLocal().to_array().tolist()
        i = g.insertionInLocal().to_array().tolist()
        vec += o + i
    return vec


def getModelFromVector(vec: list, model_path: str) -> biorbd.Model:
    vec = np.array(vec)
    model = biorbd.Model(model_path)
    for m in range(model.nbMuscles()):
        muscle = model.muscle(m)

        c = muscle.characteristics()
        c.setForceIsoMax(vec[m*9+0])
        c.setOptimalLength(vec[m*9+1])
        c.setTendonSlackLength(vec[m*9+2])

        g = muscle.position()
        g.setOrigin(np.array(vec[m*9+3: m*9+6]))
        g.setInsertionInLocal(np.array(vec[m*9+6: m*9+9]))
    return model


def getMomentArmMatrix(model: biorbd.Model, Q: np.ndarray) -> np.ndarray:
    """Return L, not -L.T"""
    return model.musclesLengthJacobian(Q).to_array()


def getStationJacobian(model, Q, bodyName: str, endEffector: list):
    x, y, z = endEffector
    point = biorbd.NodeSegment(biorbd.Vector3d(x, y, z))
    return model.markersJacobian(Q, biorbd.String(bodyName), point, False).to_array()


def getMuscleTensions(model):
    nbMuscles = model.nbMuscles()

    # ligne 1 = tensions min, ligne 2 = tensions max
    tensions = np.zeros((2, nbMuscles))
    for i in range(nbMuscles):
        t_min, t_max = getMuscleTensionsId(model, i)
        tensions[0, i] = t_min
        tensions[1, i] = t_max

    np.nan_to_num(tensions, copy=False)

    return tensions[0, :], tensions[1, :]


def getMuscleTensionsId(model, muscleId: int):
    muscle = biorbd.HillThelenType(model.muscle(muscleId))
    muscleState = muscle.state()

    a_ce = muscle.FlCE(muscleState)
    a_pe = muscle.FlPE()

    if a_ce > 1:
        a_ce = 1
    elif a_ce < 0:
        a_ce = 0

    if a_pe > 1:
        a_pe = 0.1
    elif a_pe < 0:
        a_pe = 0

    forceIsoMax = muscle.characteristics().forceIsoMax()
    if forceIsoMax < 0:
        forceIsoMax = 0
    t_min = a_pe * forceIsoMax
    t_max = (a_ce + a_pe) * forceIsoMax

    return t_min, t_max