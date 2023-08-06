import numpy as np

def generateNeighboursInBall(vec: list, nb_neighbours, ball):
    ball_low, ball_high = ball
    neighbours = [(np.array(vec) * (1 + np.random.uniform(ball_low, ball_high)/100)).tolist() for _ in range(nb_neighbours)]

    if nb_neighbours != 1:
        return neighbours
    else:
        return neighbours[0]

def isInBall(vec: list, center: list, ball):
    """Check if the vector is inside a ball centered at another vector"""
    ball_low, ball_high = center * (1 + ball/100)
    if np.all(vec >= ball_low) and np.all(vec <= ball_high): 
        return True
    return False