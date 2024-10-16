'''     11/06/2019
'''

# --- Initialization ---
import numpy as np
import m2py as mp     # Imports the M2PY library

# Important print parameters
nozzleDiam = 0.400  # mm
move_speed = 6
channelNum = 1      # Change if using channel number 2 instead

# Important geometry
l = 10      # Length (along print path orientation)
w = 10      # Width
nStrips = 1 # How many strips to print
l_inner = l-6*nozzleDiam

# Additional print parameters and geometry
jog_speed = 30
edgeHeight = 3 # Height of edge "hook" part of PDMS
stripSpacing = 5 # Space between strips (mm)
r = 0.88*nozzleDiam # spacing between lines
z0 = 1.0*nozzleDiam   # starting height off of bed
dz = 0.9*nozzleDiam # spacing between layers
rows = int(np.floor((w/r)/2))
edge = int(np.floor((edgeHeight/dz)/2)) - 1
print("Actual width: {0:.2f} mm".format(2*rows*r))


# Start position
start = [10.5 + nozzleDiam, 110.5, -126 + z0]         # The starting global coordinates of the tool_head (do not change unless hardware changes)

# Initializw printing
mk = mp.Makergear('COM7', 115200, printout = 1) # Set printout = 1 to send the printer commands;
                                                # Set printout = 0 to visualize the print path
mk.coord_sys(coord_sys = 'rel')                 # Sets coordinate system to relative
mk.home(axes = 'X Y Z')                         # Homes all axes to global (0,0,0)
mk.speed(speed = jog_speed)                     
mk.move(x = start[0], y = start[1], z = start[2], track = 0)  
mk.speed(speed = move_speed)

# --- Movement commands ---
# Units are mm and commands are relative to current location
# (NOT relative to global coordinate system).

for unit in range(nStrips):
    mk.on(channelNum)
    mk.move(y = (2*rows-1)*r)
    mk.off(channelNum)
    mk.move(z = nozzleDiam)
    mk.move(x = l - 2*nozzleDiam)
    mk.move(z = -nozzleDiam)
    mk.on(channelNum)
    mk.move(y = -(2*rows-1)*r)
    mk.off(channelNum)
    mk.move(z = dz)
    mk.on(channelNum)
    for line in range(rows):
        mk.move(x = -(l - 2*nozzleDiam))
        mk.move(y = r)
        mk.move(x = (l - 2*nozzleDiam))
        if line != rows-1:
            mk.move(y = r)
    mk.off(channelNum)
    mk.move(x = -(l - 2*nozzleDiam), y = stripSpacing)
    mk.move(z = -dz)

mk.close() # This always needs to be called at the end of every script