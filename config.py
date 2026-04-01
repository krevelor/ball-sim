#################################################################
#
# Helper file for config parameters
# Simulation paramters are presented here with brief usage explanations
# for easy program tuning
# Other files then just call get_params to pull whatever values are needed
# Some values have default/suggested values, which I find to work well as starting points
#
# Eden Carrier, 2023
#
# 


# dimension of the screen
# ranges from -gridsize to gridsize in both directions
# default: 50
GRIDSIZE = 50

# the number of balls
# the only limit on it is the strength of your pc
# depending on other settings, my laptop maxes out at around 5 - 20
N = 15

# behavior when balls interact with the edge of the screen
# "none" - walls dont do anything
# "solid" - balls ricochet
# default - depends on force of choice. see manual.
WALLSTYLE = "solid"

# the force to subject the balls to
# "none" - no force
# "gravity" - simple surface gravity. as all units are pretty much arbitrary anyway, g is chosen to work well visually
# "orbit" - force proportional to distance from origin, leads to simple orbits
# "solar" - inverse square law. adds a stationary ball to the origin to represent the sun, and prevent weird behavior with things getting too close to the origin
# default - none
FORCE = "none"

# max initial velocity
# default 1
VMAX = 10

# range of ball radii
# default - 2,5
RMIN = 2
RMAX = 5

# how to define masses
# "random" - picks random values between 1 and 32
# "const_p" - assigns mass consistent with the radius
# "constant" - sets all to 1
# default - const_p
MASSSTYLE = "random"

# toggle for drawing the trace, a record of the paths of all balls
# I recommend keeping this off in general, as it slows the sim down considerably
# default - False
SHOWTRACE = False


def get_params():
    returnval = (GRIDSIZE, N, WALLSTYLE, FORCE, VMAX, RMIN, RMAX, MASSSTYLE, SHOWTRACE)
    return returnval
