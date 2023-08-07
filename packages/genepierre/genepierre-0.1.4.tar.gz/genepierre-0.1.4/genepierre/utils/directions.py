import numpy as np
import matplotlib.pyplot as plt

# 1. Directions spanned by the octahedron vertices (3)
def createD1(a1 = 1, a2 = 1, a3 = 1):
    """a1, a2, a3 are respectively the lengths of e1, e2, e3"""
    main_dir = np.diag([a1,a2,a3])
    all_dir = np.vstack([main_dir, -main_dir])
    return main_dir, all_dir

def createD2(a1 = 1, a2 = 1, a3 = 1):
    main_oct, _ = createD1(a1,a2,a3)

    e1, e2, e3 = main_oct
    pt12 = e1 + e2
    pt23 = e2 + e3
    pt13 = e1 + e3
    bar1 = (pt12 + pt23 + pt13)/3
    bar2 = np.hstack([bar1[0], bar1[1], -bar1[2]])
    bar3 = np.hstack([bar1[0], -bar1[1], bar1[2]])
    bar4 = np.hstack([bar1[0], -bar1[1], -bar1[2]])
    bar5 = np.hstack([-bar1[0], bar1[1], bar1[2]])
    bar6 = np.hstack([-bar1[0], bar1[1], -bar1[2]])
    bar7 = np.hstack([-bar1[0], -bar1[1], bar1[2]])
    bar8 = np.hstack([-bar1[0], -bar1[1], -bar1[2]])

    all_dir = np.vstack([bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8])
    return all_dir

def createD3(a1 = 1, a2 = 1, a3 = 1):
    main_oct, _ = createD1(a1,a2,a3)
    e1, e2, e3 = main_oct
    
    pt1_e12 =  e1 + e2
    pt2_e12 =  e1 - e2
    pt3_e12 = -e1 + e2
    pt4_e12 = -e1 - e2

    pt1_e23 =  e2 + e3
    pt2_e23 =  e2 - e3
    pt3_e23 = -e2 + e3
    pt4_e23 = -e2 - e3

    pt1_e13 =  e1 + e3
    pt2_e13 =  e1 - e3
    pt3_e13 = -e1 + e3
    pt4_e13 = -e1 - e3

    all_dir = np.vstack([
        pt1_e12,
        pt2_e12,
        pt3_e12,
        pt4_e12,
        pt1_e23,
        pt2_e23,
        pt3_e23,
        pt4_e23,
        pt1_e13,
        pt2_e13,
        pt3_e13,
        pt4_e13
    ])

    return all_dir
D3 = createD3(1,2,3)

def getD1(a1=1, a2=1, a3=1):
    _, D1 = createD1(a1, a2, a3)
    return D1

def getD2(a1=1, a2=1, a3=1):
    D2 = createD2(a1, a2, a3)
    return D2

def getD3(a1=1, a2=1, a3=1):
    D3 = createD3(a1, a2, a3)
    return D3

# Directions are cube vertices + octahedron vertices
# 7 dir = 14 vertices
def getD4(a1=1, a2=1, a3=1):
    D1 = getD1(a1, a2, a3)
    D2 = getD2(a1, a2, a3)
    return np.vstack([D1, D2])

# Directions are octahedron vertices + rectangle planes vertices
# 9 dir = 18 vertices
def getD5(a1=1, a2=1, a3=1):
    D1 = getD1(a1, a2, a3)
    D3 = getD3(a1, a2, a3)
    return np.vstack([D1, D3])

# Directions are cube vertices + rectangle planes vertices
# 10 dir = 20 vertices
def getD6(a1=1, a2=1, a3=1):
    D2 = getD2(a1, a2, a3)
    D3 = getD3(a1, a2, a3)
    return np.vstack([D2, D3])

# Directions are cube vertices + octahedron vertices + rectangle planes vertices
# 13 dir = 26 vertices
def getD7(a1=1, a2=1, a3=1):
    D1 = getD1(a1, a2, a3)
    D2 = getD2(a1, a2, a3)
    D3 = getD3(a1, a2, a3)
    return np.vstack([D1, D2, D3])

