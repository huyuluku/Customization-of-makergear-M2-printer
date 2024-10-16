'''     Print one layer of a rectangle of size w x l, with the print direction 
        along the length. Uses both channels at once for core-shell printing.
'''

# --- Initialization ---
import numpy as np
import math
import m2py as mp     # Imports the M2PY library, and gives it a shorter name, mp

# CHANGE BEFORE EACH RUN
nozzleDiam = 0.600
alpha = math.pi/4  # angle of printing
w = 40
l = 40
r = 0.88*nozzleDiam # spacing between lines
rows_from_x = int(np.floor(w*math.sin(alpha)/r))
rows_from_y = int(np.floor(l*math.cos(alpha)/r))
rows = min(rows_from_x, rows_from_y)
diff_row = rows_from_x - rows_from_y
z0 = 0.8 * nozzleDiam
dz = 0.8 * nozzleDiam

start = [10, 35, -125.0 + z0]         # The starting global coordinates of the tool_head (do not change unless hardware changes)
layers = 2

move_speed = 45
jog_speed = 30

mk = mp.Makergear('COM7', 115200, printout = 0) # Initializes the printer. If printout = 1, the printer gets sent commands; if printout = 0, Spyder just plots the coordinates in the visualizer.
mk.coord_sys(coord_sys = 'abs')                 # Sets coordinate system to relative
mk.home(axes = 'X Y Z')                         # Homes all axes to global (0,0,0)
mk.speed(speed = jog_speed)                     # Movement speed in mm/s
mk.move(x = start[0], y = start[1], z = start[2], track = 0)    # Moves the tool head to the start location, relative to (0,0,0). Set this after you manually check nozzle height off of the printbed.
mk.speed(speed = move_speed)

# --- Movement commands ---
# Units are mm, and commands are relative to current location (NOT relative to global coordinate system).

mk.on(1)
for row1 in range(0, rows):
    if np.mod(row1, 2) == 0:
        mk.move(x=r/math.sin(alpha)*row1, y=0)
        mk.move(x=0, y=r/math.cos(alpha)*row1)
    else:
        mk.move(x=0, y=r/math.cos(alpha)*row1)
        mk.move(x=r/math.sin(alpha)*row1, y=0)  
for row2 in range(0, rows):
    if np.mod(row2, 2) == 0:
        mk.move(x=w, y=l-r/math.cos(alpha)*row2)
        mk.move(x=w-r/math.sin(alpha)*row2, y=l)
    else:
        mk.move(x=w-r/math.sin(alpha)*row2, y=l)
        mk.move(x=w, y=l-r/math.cos(alpha)*row2)
if diff_row < 0:
    for row3 in range(0, abs(diff_row)):
        if np.mod(row3, 2) == 0:
            mk.move(x=0, y=w*math.tan(alpha)+r/math.cos(alpha)*row3)
            mk.move(x=w, y=r/math.cos(alpha)*row3)
        else:
            mk.move(x=w, y=r/math.cos(alpha)*row3)
            mk.move(x=0, y=w*math.tan(alpha)+r/math.cos(alpha)*row3) 
if diff_row > 0:
    for row3 in range(0, diff_row):
        if np.mod(row3, 2) == 0:
            mk.move(x=r/math.sin(alpha)*row3, y=l)
            mk.move(x=l/math.tan(alpha)+r/math.sin(alpha)*row3, y=0)
        else:
            mk.move(x=l/math.tan(alpha)+r/math.sin(alpha)*row3, y=0)
            mk.move(x=r/math.sin(alpha)*row3, y=l)
if diff_row == 0:
    mk.move(w,0)
    mk.move(0,l)

mk.off(1)
mk.move(x = -5, z = 50)

mk.close() # This always needs to be called at the end of every script