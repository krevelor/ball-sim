This program is a ball simulation. The initial goal was mess around with billiard dynamics, letting balls ricochet around in a fashion consistent with conservation of energy. I had long been interested in creating something like this, but finally found the opportunity to create it for an open ended class project during undergrad.

The simulation is divided into three classes for readability. These are:
ballsim.py - the main runner class, which contains the high level set up, execution, and animation functions.
collisions.py - contains the core functions used to calculate collisions, both between balls and when balls collide with walls
config.py - helper file used for setting program parameters, along with explinations of the various options

Once configuration is set as you'd like, simply run ballsim.py and the simulation will generate and run. There is no stop condition, so the animation will continue playing until it is stopped by the user or restarted.