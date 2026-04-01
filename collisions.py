#################################################################
#
# Helper file for collision methods
# Collisions are energy conserving, and ball-ball collisions conserve momentum
# Eden Carrier, 2023
#
# 

import config


# simply reflects ball or wraps to opposite side, depending on settings
def wall_collision( pos, vel, rad ):
    (GRIDSIZE,_,WALLSTYLE,_,_,_,_,_,_) = config.get_params()
    if WALLSTYLE == "solid":
        if pos[0] + rad >= GRIDSIZE and vel[0] > 0:
            vel[0] *= -1
        elif pos[0] - rad <= -1 * GRIDSIZE and vel[0] < 0:
            vel[0] *= -1

        if pos[1] + rad >= GRIDSIZE and vel[1] > 0:
            vel[1] *= -1
        elif pos[1] - rad <= -1 * GRIDSIZE and vel[1] < 0:
            vel[1] *= -1
    elif WALLSTYLE == "wrap": 
        if pos[0] >= GRIDSIZE:
            pos[0] -= 100
        elif pos[0] <= -1 * GRIDSIZE:
            pos[0] += 100

        if pos[1] >= GRIDSIZE:
            pos[1] -= 100
        elif pos[1] <= -1 * GRIDSIZE:
            pos[1] += 100

# helper method to project vector a onto vector b
def proj( a, b ):
    num = a[0]*b[0] + a[1]*b[1]
    den = b[0]**2 + b[1]**2
    c = [0,0]
    c[0] = b[0] * num/den
    c[1] = b[1] * num/den
    return c

# method for calculating changes in momenta when balls collide
# assumes perfectly elastic collisions (energy and momentum conserving)
def ball_collision( pos1, vel1, m1, r1, pos2, vel2, m2, r2 ):
    # check balls are close enough to collide
    mindist = r1 + r2
    D = [ pos2[0] - pos1[0], pos2[1] - pos1[1] ]
    if D[0]**2 + D[1]**2 > mindist**2:
        return
    # do calculations in terms of orthogonal and parallel components of velocity
    # vectors in new coordinate system
    v1O = proj( vel1, D )
    v1P = [ vel1[0] - v1O[0], vel1[1] - v1O[1] ]
    v2O = proj( vel2, D )
    v2P = [ vel2[0] - v2O[0], vel2[1] - v2O[1] ]

    # need actual magnitudes in relavant direction
    v1,v2 = 0,0
    if v1O[0] * D[0] + v1O[1] * D[1] < 0:
        # positive direction
        v1 = (v1O[0]**2 + v1O[1]**2)**0.5
    else:
        # negative direction
        v1 = -1 * (v1O[0]**2 + v1O[1]**2)**0.5
    if v2O[0] * D[0] + v2O[1] * D[1] < 0:
        # positive direction
        v2 = (v2O[0]**2 + v2O[1]**2)**0.5
    else:
        # negative direction
        v2 = -1 * (v2O[0]**2 + v2O[1]**2)**0.5
    
    # check collision will actually happen
    if v1 - v2 > 0:
        return

    # initial momentum and energy
    # 1/2s are neglected as they can be canceled through immediately
    P = m1*v1 + m2*v2
    E = m1*v1**2 + m2*v2**2

    # the system of equations has exactly two solutions, corresponding
    # to the initial and final conditions of the system. to determine
    # the result, I therefore simply take the one of the answers which isn't
    # the initial condition
    
    result = [0,0]
    
    # calc new v1
    root = (P*m1)**2 - (m1**2 + m1*m2) * (P**2 - m2*E)
    root = root**0.5
    val1 = P*m1 + root
    val1 /= m1**2 + m1*m2
    val2 = P*m1 - root
    val2 /= m1**2 + m1*m2
    # pick answer which isn't the initial value
    if abs(val1 - v1) < abs(val2 - v1):
        result[0] = val2
    else:
        result[0] = val1

    # calc new v2
    root = (P*m2)**2 - (m2**2 + m1*m2) * (P**2 - m1*E)
    root = root**0.5
    val1 = P*m2 + root
    val1 /= m2**2 + m1*m2
    val2 = P*m2 - root
    val2 /= m2**2 + m1*m2
    # pick answer which isn't the initial value
    if abs(val1 - v2) < abs(val2 - v2):
        result[1] = val2
    else:
        result[1] = val1

    # turn results back into usual velocity system
    
    scale1 = result[0] / v1 if v1 != 0 else 0
    scale2 = result[1] / v2 if v2 != 0 else 0

    v1O = [ scale1 * v1O[0], scale1 * v1O[1] ]
    v2O = [ scale2 * v2O[0], scale2 * v2O[1] ]

    vel1[0] = v1O[0] + v1P[0]
    vel1[1] = v1O[1] + v1P[1]
    vel2[0] = v2O[0] + v2P[0]
    vel2[1] = v2O[1] + v2P[1]
    
