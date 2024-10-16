# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:41:38 2020

@author: Lab414
"""

import numpy as np
import m2py as mp     # Imports the M2PY library

# function which print a parallelgram with width a heigh b and angle phi
def parallelgram_print(a,b,phi,d,start='lb',finish=1):
    xspace = np.floor(a/d)+1
    if phi == np.pi/2:
        xmove = 0
    else:
        xmove = b/np.tan(phi)
    
    if start=='lb':
        for i in range(np.int(np.floor(xspace/2))):
            mk.move(x=xmove,y=b)
            mk.move(x=d)
            mk.move(x=-xmove,y=-b)
            if finish or i<np.int(np.floor(xspace/2))-1:
                mk.move(x=d)
    elif start=='rt':
        for i in range(np.int(np.floor(xspace/2))):
            mk.move(x=-xmove,y=-b*np.sin(phi))
            mk.move(x=-d)
            mk.move(x=xmove,y=b)
            if finish or i<np.int(np.floor(xspace/2))-1:
                mk.move(x=-d)
    elif start=='rb':
        for i in range(np.int(np.floor(xspace/2))):
            mk.move(x=xmove,y=b)
            mk.move(x=-d)
            mk.move(x=-xmove,y=-b)
            if finish or i<np.int(np.floor(xspace/2))-1:
                mk.move(x=-d)
    elif start=='lt':
        for i in range(np.int(np.floor(xspace/2))):
            mk.move(x=-xmove,y=-b)
            mk.move(x=d)
            mk.move(x=xmove,y=b)
            if finish or i<np.int(np.floor(xspace/2))-1:
                mk.move(x=d)
                
# Important print parameters
nozzleDiam = 0.6  # mm
move_speed1 = 30
move_speed2 = 30
rotation_speed = 97
channelNum1 = 1      # Change if using channel number 2 instead
channelNum2 = 2

d = 0.65 #extrusion width
dz = 0.45 # layer height
l = 80

region1_width = 40
region2_width = 0
period = 1
angle = np.pi/2


# Important geometry

# Additional print parameters and geometry
jog_speed = 45

# Start position
start =[90, 35, -135.2 + dz]  # The starting global coordinates of the toolhead
#channel_offset = [39.25,0.45,1.65]

# Initializw printing
mk = mp.Makergear('COM7', 115200, printout = 1) # Set printout = 1 to send the printer commands;
                                                # Set printout = 0 to visualize the print path
mk.coord_sys(coord_sys = 'rel')                 # Sets coordinate system to relative
mk.home(axes = 'X Y Z')                         # Homes all axes to global (0,0,0)
mk.speed(speed = jog_speed)                     
mk.move(x = start[0], y = start[1], z = start[2], track = 0)  
mk.speed(speed = move_speed1)


for i in range(period):
    mk.on(channelNum1)
    mk.rotate(speed=rotation_speed)
    parallelgram_print(region1_width,l,angle,d,'lb',1)
    mk.rotate(speed=0)
    mk.off(channelNum1)
mk.move(z=dz)

mk.speed(speed = move_speed2)
for i in range(period):
    mk.on(channelNum1)
    if i<period-1:
        parallelgram_print(region1_width,l,angle,d,'rb',1)
    else:
        parallelgram_print(region1_width,l,angle,d,'rb',0)
    mk.off(channelNum1)
    mk.rotate(speed=0)
mk.move(z=dz)

mk.speed(speed = move_speed1)
for i in range(period):
    mk.on(channelNum1)
    mk.rotate(speed=rotation_speed)
    parallelgram_print(region1_width,l,angle,d,'lb',1)
    mk.off(channelNum1)
    mk.rotate(speed=0)
    
mk.home(axes='X Y Z')
mk.close()        
