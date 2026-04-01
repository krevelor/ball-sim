#################################################################
#
# Ball sim main file
# Eden Carrier, 2023
#
# 




import numpy as np
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import random
import math
import config
import collisions as col

# simulation parameters - pulled from config.py
(GRIDSIZE, N, WALLSTYLE, FORCE, VMAX, RMIN, RMAX, MASSSTYLE, SHOWTRACE) = config.get_params()

dims = ( -1*GRIDSIZE, GRIDSIZE )

fig = plt.figure()
ax = plt.axes(xlim=dims, ylim=dims)

# initialize sim objects info
balls = []
for i in range(N):
    ball, = ax.plot([],[])
    balls.append( ball )

rads = []
for i in range(N):
    rads.append( random.randint(RMIN,RMAX) )

ms = []
for i in range(N):
    if MASSSTYLE == "random":
        ms.append(2**(5*random.random()))
    elif MASSSTYLE == "const_p":
        ms.append( rads[i]**2 )
    elif MASSSTYLE == "constant":
        ms.append( 1 )

pos = []
for i in range(N):
    pos.append( [random.randint(-1*GRIDSIZE, GRIDSIZE),random.randint(-1*GRIDSIZE, GRIDSIZE)] )

vel = []
for i in range(N):
    theta = 2*math.pi * random.random()
    v = VMAX * random.random()
    vel.append( [ v*math.cos(theta), v*math.sin(theta) ] )


# make sun if solar sim
if FORCE == "solar":
    ball, = ax.plot([],[])
    balls.append(ball)
    rads.append(10)
    ms.append(10**7)
    pos.append([0,0])
    vel.append([0,0])
    N += 1


# if tracing is enabled, set up plots for each path
traces = []
traceobj = []
if SHOWTRACE:
    for i in range(N):
        trace, = ax.plot([],[])
        traceobj.append(trace)
        traces.append( [[pos[i][0], pos[i][1]]] )

# end init #####################################################################

# helper method for drawing arbitrarily sized circles
def ball_data( pos, rad ):
    xs = []
    ys = []
    points = 60 * rad
    for th in range(points):
        theta = th / points * 2 * math.pi
        x = pos[0] + math.cos(theta) * rad
        y = pos[1] + math.sin(theta) * rad
        xs.append(x)
        ys.append(y)
    return xs,ys

# helper method to get trace data into proper format for plotting
def trace_data( i ):
    xs = np.array( traces )[i,:,0]
    ys = np.array( traces )[i,:,1]
    return xs, ys

# switcher method for different acceleration behaviors
def force( pos, vel, mass ):
    F = []
    if FORCE == "gravity":
        F = [0, -2 * mass] # gravity, but values arent tuned
    elif FORCE == "orbit":
        F = [-1*pos[0] / GRIDSIZE, -1*pos[1] / GRIDSIZE]
    elif FORCE == "solar":
        r2 = max( pos[0]**2 + pos[1]**2, 10**(-6) )
        rh = r2**0.5
        GM = 100
        F = [-1 * GM * mass / r2 * pos[0] / rh, -1 * GM * mass / r2 * pos[1] / rh]
    F[0] /= mass
    F[1] /= mass
    return F        # the acceleration vector



# animation machinery
# method to advance sim, called 10x each frame
def next_step():
    global pos, vel
    timestep = 1/100
    forceflag = (FORCE != "none")
    for i in range(N):
        # iterate each ball
        # use velocity as dx/dt, use force (if any) for dy/dt
        if forceflag:
            dvdt = force( pos[i], vel[i], ms[i] )
        pos[i][0] += timestep * vel[i][0]
        pos[i][1] += timestep * vel[i][1]
        #if SHOWTRACE:
        #    traces[i].append( [pos[i][0] , pos[i][1]] )
        if FORCE == "solar" and i+1 == N:
            break
        if forceflag:
            vel[i][0] += timestep * dvdt[0]
            vel[i][1] += timestep * dvdt[1]
        # if walls are enabled, check if each ball collides with wall
        if not WALLSTYLE == "none":
            col.wall_collision( pos[i], vel[i], rads[i] )
    # once all balls have moved, check for ball-ball collisions
    for i in range(N):
        for j in range(i+1,N):
            col.ball_collision( pos[i], vel[i], ms[i], rads[i], pos[j], vel[j], ms[j], rads[j] )

# initalizer to set up animation start
def init():
    for i in range(N):
        balls[i].set_data([],[])
        if SHOWTRACE:
            traceobj[i].set_data([],[])
    if SHOWTRACE:
        return tuple(balls) + tuple(traceobj)
    else:
        return tuple(balls)

# wrapper for next_step called once per animation frame
def animate(i):
    # to avoid redrawing too often while maintaining a small enough
    # time step for good simulation, numerical simulation happens
    # ten times before each frame is drawn
    for _ in range(10):
        next_step()
    # only want to record position once per animation frame, but need to do all
    # traces at once so the array can be sliced properly for their plotting info
    if SHOWTRACE:
        for j in range(N):
            traces[j].append( [pos[j][0] , pos[j][1]] )
    for j in range(N):
        (xs, ys) = ball_data( pos[j], rads[j] )
        balls[j].set_data(xs,ys)
        if SHOWTRACE:
            (xs, ys) = trace_data( j )
            traceobj[j].set_data(xs,ys)
            #print( np.array( traces ).shape )
    if SHOWTRACE:
        return tuple(balls) + tuple(traceobj)
    else:
        return tuple(balls)

# actual animation runner
ani = anim.FuncAnimation(fig, animate, init_func=init, interval=1, blit=True)
plt.gca().set_aspect('equal')
plt.show()

