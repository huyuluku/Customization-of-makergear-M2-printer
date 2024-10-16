'''     Print one layer of a rectangle of size w x l, with the print direction 
        along the length. Uses both channels at once for core-shell printing.
'''

# --- Initialization ---
import numpy as np
import math
import m2py as mp     # Imports the M2PY library, and gives it a shorter name, mp

# CHANGE BEFORE EACH RUN
nozzleDiam = 0.600
theta = math.pi/2
w = 40
l = 40
r = 0.88*nozzleDiam # spacing between lines
rows = int(np.floor((l/r)/2))
offset = r/math.tan(theta)
z0 = 0.8 * nozzleDiam
dz = 0.8 * nozzleDiam

start = [10, 35, -125.0 + z0]         # The starting global coordinates of the tool_head (do not change unless hardware changes)
layers = 2

move_speed = 45
jog_speed = 30

mk = mp.Makergear('COM7', 115200, printout = 0) # Initializes the printer. If printout = 1, the printer gets sent commands; if printout = 0, Spyder just plots the coordinates in the visualizer.
mk.coord_sys(coord_sys = 'rel')                 # Sets coordinate system to relative
mk.home(axes = 'X Y Z')                         # Homes all axes to global (0,0,0)
mk.speed(speed = jog_speed)                     # Movement speed in mm/s
mk.move(x = start[0], y = start[1], z = start[2], track = 0)    # Moves the tool head to the start location, relative to (0,0,0). Set this after you manually check nozzle height off of the printbed.
mk.speed(speed = move_speed)

# --- Movement commands ---
# Units are mm, and commands are relative to current location (NOT relative to global coordinate system).

mk.on(1)
#mk.on(2)
for i in range(layers):
    if np.mod(i,2) == 0:
        for unit in range(0, rows):
            mk.move(x = w)    # Move in a line by specified amount to specified direction
            mk.move(x = offset, y = r)
            mk.move(x = -w)
            mk.move(x = offset, y = r)
    else:
        for unit in range(0, rows):
            mk.move(x = w)    # Move in a line by specified amount to specified direction
            mk.move(x= -offset, y = -r)
            mk.move(x = -w)
            mk.move(x= -offset, y = -r)        
    mk.move(z = dz)
mk.off(1)
#mk.off(2)
mk.move(x = -5, z = 50)

mk.close() # This always needs to be called at the end of every script