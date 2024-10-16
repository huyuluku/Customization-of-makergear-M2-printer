'''     11/06/2019
'''

# --- Initialization ---
import numpy as np
import m2py as mp     # Imports the M2PY library

# Important print parameters
nozzleDiam = 0.600  # mm
move_speed = 4
channelNum = 1      # Change if using channel number 2 instead

# Important geometry
l = 65      # Length (along print path orientation)
w = 5     # Width
nStrips = 1 # How many strips to print
nLayers = 1  # How many layers to print

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
start = [10, 35, -126.5 + z0]         # The starting global coordinates of the tool_head (do not change unless hardware changes)

# Initializw printing
mk = mp.Makergear('COM7', 115200, printout = 0) # Set printout = 1 to send the printer commands;
                                                # Set printout = 0 to visualize the print path
mk.coord_sys(coord_sys = 'rel')                 # Sets coordinate system to relative
mk.home(axes = 'X Y Z')                         # Homes all axes to global (0,0,0)
mk.speed(speed = jog_speed)                     
mk.move(x = start[0], y = start[1], z = start[2], track = 0)  
mk.speed(speed = move_speed)

# --- Movement commands ---
# Units are mm and commands are relative to current location
# (NOT relative to global coordinate system).

if nLayers % 2 == 0:    direction = 1
else:                   direction = -1

for unit in range(nStrips):
    mk.on(channelNum)
    direction = 1
    # Print each layer of PDMS
    for layer in range(nLayers):
        if layer % 2 == 0:
            for line in range(rows):
                mk.move(x = l)
                mk.move(y = r)
                mk.move(x = -l)
                if line != rows-1:
                    mk.move(y = r)
        else:
            for line in range(rows):
                if line != 0:
                    mk.move(y = -r)    
                mk.move(x = l)
                mk.move(y = -r)
                mk.move(x = -l)
        mk.move(z = dz)
    # Print "lip" on each side, one at a time
    for h in range(edge):
        mk.move(y = direction*(2*rows-1)*r)
        mk.move(z = dz)
        mk.move(y = -direction*(2*rows-1)*r)
        if line != edge-1:
            mk.move(z = dz)
    mk.off(channelNum)
    mk.move(x = l)
    mk.move(z = -(2*edge)*dz)
    mk.on(channelNum)
    for h in range(edge):
        mk.move(y = direction*(2*rows-1)*r)
        mk.move(z = dz)
        mk.move(y = -direction*(2*rows-1)*r)
        if line != edge-1:
            mk.move(z = dz)
    mk.off(channelNum)
    if nLayers % 2 == 0:    mk.move(y = stripSpacing + (2*rows-1)*r)
    else:                   mk.move(y = stripSpacing)
    mk.move(x = -l)
    mk.move(z = -2*dz*edge - nLayers*dz)

mk.close() # This always needs to be called at the end of every script