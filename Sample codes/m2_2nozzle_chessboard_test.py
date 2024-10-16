'''     Print one layer of a rectangle of size w x l, with the print direction 
        along the length. Uses both channels at once for core-shell printing.
'''

# --- Initialization ---
import numpy as np
import m2py as mp     # Imports the M2PY library, and gives it a shorter name, mp

# CHANGE BEFORE EACH RUN
nozzleDiam = 0.600
w = 10
l = 10
r = 0.88*nozzleDiam # spacing between lines
rows = int(np.floor((l/r)/2))
z0 = 0.8 * nozzleDiam
dz = 0.8 * nozzleDiam
x_offset = 40.0  # x distance between nozzle 1 and nozzle 2, x2-x1
y_offset = 0.0  # y distance between nozzle 1 and nozzle 2
z_offset = 0.0  # z distance between nozzle 1 and nozzle 2

start = [10, 35, -125 + z0]         # The starting global coordinates of nozzle 1

move_speed = 40
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
for unit in range(0, rows):
   mk.move(x = w)
   mk.move(y = r)
   mk.move(x = -w)
   mk.move(y = r)
mk.off(1)

mk.move(y=-2*r*(rows)-y_offset, z=5)
mk.move(x=w)
mk.move(x=-x_offset)
mk.move(z=-5)
mk.on(2)
for unit in range(0, rows):
    mk.move(x = w)    # Move in a line by specified amount to specified direction
    mk.move(y = r)
    mk.move(x = -w)
    mk.move(y = r)
mk.off(2)

mk.move(y=-2*r*(rows)-y_offset, z=5)
mk.move(x=w)
mk.move(x=x_offset)
mk.move(z=-5)
mk.on(1)
for unit in range(0, rows):
   mk.move(x = w)
   mk.move(y = r)
   mk.move(x = -w)
   mk.move(y = r)
mk.off(1)

mk.move(y=-y_offset, z=5)
mk.move(x=-2*w)
mk.move(x=-x_offset)
mk.move(z=-5)
mk.on(2)
for unit in range(0, rows):
    mk.move(x = w)    # Move in a line by specified amount to specified direction
    mk.move(y = r)
    mk.move(x = -w)
    mk.move(y = r)
mk.off(2)

mk.move(y=-2*r*(rows)-y_offset, z=5)
mk.move(x=w)
mk.move(x=x_offset)
mk.move(z=-5)
mk.on(1)
for unit in range(0, rows):
   mk.move(x = w)
   mk.move(y = r)
   mk.move(x = -w)
   mk.move(y = r)
mk.off(1)

mk.move(y=-2*r*(rows)-y_offset, z=5)
mk.move(x=w)
mk.move(x=-x_offset)
mk.move(z=-5)
mk.on(2)
for unit in range(0, rows):
    mk.move(x = w)    # Move in a line by specified amount to specified direction
    mk.move(y = r)
    mk.move(x = -w)
    mk.move(y = r)
mk.off(2)

mk.move(y=-y_offset, z=5)
mk.move(x=-2*w)
mk.move(x=x_offset)
mk.move(z=-5)
mk.on(1)
for unit in range(0, rows):
    mk.move(x = w)    # Move in a line by specified amount to specified direction
    mk.move(y = r)
    mk.move(x = -w)
    mk.move(y = r)
mk.off(1)

mk.move(y=-2*r*(rows)-y_offset, z=5)
mk.move(x=w)
mk.move(x=-x_offset)
mk.move(z=-5)
mk.on(2)
for unit in range(0, rows):
    mk.move(x = w)    # Move in a line by specified amount to specified direction
    mk.move(y = r)
    mk.move(x = -w)
    mk.move(y = r)
mk.off(2)

mk.move(y=-2*r*(rows)-y_offset, z=5)
mk.move(x=w)
mk.move(x=x_offset)
mk.move(z=-5)
mk.on(1)
for unit in range(0, rows):
   mk.move(x = w)
   mk.move(y = r)
   mk.move(x = -w)
   mk.move(y = r)
mk.off(1)

mk.close() # This always needs to be called at the end of every script