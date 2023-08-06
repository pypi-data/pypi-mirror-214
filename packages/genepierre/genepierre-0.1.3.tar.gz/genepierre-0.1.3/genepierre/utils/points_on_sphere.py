import numpy as np
import matplotlib.pyplot as plt
import itertools

def split_sphere(R = 1, horizontal_split = 36, vertical_split = 36, method="equal_angles"):
    theta = np.linspace(0,360,horizontal_split+1)
    if method == "equal_angles":
        phi = np.linspace(0, 180, vertical_split+1)
        c = np.cos(phi)
        s = np.sin(phi)
    elif method == "equal_area":
        c = np.linspace(-1, 1, vertical_split+1)
        s = 1 - c**2
    else:
        raise(ValueError('method must be "equal_angles" or "equal_area"'))
    x = R * np.outer(s, np.cos(theta))
    y = R * np.outer(s, np.sin(theta))
    z = R * np.outer(c, np.ones(horizontal_split+1))
    return x, y, z

def sphere_parametric(nb_theta = 36, nb_phi = 36, r = 1, center = np.zeros(3)):
    thetas = np.linspace(0, np.pi, nb_theta)
    phis = np.linspace(0, 2*np.pi, nb_phi)

    comb = itertools.product(thetas, phis)

    x0, y0, z0 = center

    points = []
    for theta, phi in comb:
        x = x0 + r*np.sin(theta)*np.cos(phi)
        y = y0 + r*np.sin(theta)*np.sin(phi)
        z = z0 + r*np.cos(theta)
        point = np.array([x,y,z])
        points.append(point)
    
    return np.array(points)