#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 16:07:52 2021

@author: hangshu
"""
import math
import numpy as np
from mecode import G

def printstruct_flat(Nx, Ny, phi, alpha, h1,h2, offset):
    top_x = h2/np.tan(alpha)
    
    for j in range(Ny):
        g.move(x=offset)
        if j%2 ==0:
            for i in range(int((Nx-1)/2)):
                g.move(x=l)
                g.move(x=top_x, y=h1)
                g.move(x=l-top_x, y=-h1)
                
            g.move(x=l)
            for i in range(int((Nx-1)/2)):
                g.move(x=-(l-top_x), y=-h2)
                g.move(x=-top_x, y=h2)
                g.move(x=-l)
                
            g.move(x=-(l-top_x), y=-h2)
            g.move(x=-top_x, y=h2)
            g.move(x=-offset)
            if j < Ny-1:
                g.move(y=-(h1+h2))
            
        else:
            for i in range(int((Nx-1)/2)):
                g.move(x=l)
                g.move(x=top_x, y=-h2)
                g.move(x=l-top_x, y=h2)
            g.move(x=l)
            for i in range(int((Nx-1)/2)):
                g.move(x=-(l-top_x), y=h1)
                g.move(x=-top_x, y=-h1)
                g.move(x=-l)
            g.move(x=-(l-top_x), y=h1)
            g.move(x=-top_x, y=-h1)   
            g.move(x=-offset)
            if j<Ny-1:
                g.move(y=-(h1+h2))

def printstruct_twist(Nx, Ny, h1, h2, alpha, beta, phi, offset, lb, lt):
    
    #calculate geometry
    up_x = lt*np.cos(beta)
    up_y = lt*np.sin(beta)
    down_x =(h2/np.sin(alpha))*np.sin(np.pi/2+beta-alpha)
    down_y=(h2/np.sin(alpha))*np.cos(np.pi/2+beta-alpha)  
    
    base_x = h1/np.tan(phi)
    for j in range(Ny):
        
        if j%2 ==0:
            g.move(y=offset+j*(down_x-base_x)+np.floor(j/2)*(lb-up_x))
            for i in range(int((Nx-1)/2)):
                g.move(y=up_x, x = -up_y)
                g.move(y=base_x, x=-h1)
                g.move(y=lb-base_x, x=h1)
                
            g.move(y=up_x, x= -up_y)
            for i in range(int((Nx-1)/2)):
                g.move(y=-(up_x-down_x), x=(up_y+down_y))
                g.move(y=-down_x, x=-down_y)
                g.move(y=-lb)
                
            g.move(y=-(up_x-down_x), x=(up_y+down_y))
            g.move(y=-down_x, x=-down_y)
            g.move(y=-(offset+j*(down_x-base_x)+np.floor(j/2)*(lb-up_x)))
            if j < Ny-1:
                g.move(x=(h1+down_y))
            
        else:
            g.move(y=offset+j*(down_x-base_x)+np.floor(j/2)*(lb-up_x))
            for i in range(int((Nx-1)/2)):
                g.move(y=lb)
                g.move(y=down_x, x=down_y)
                g.move(y=(up_x-down_x), x=-(up_y+down_y))
            g.move(y=lb)
            for i in range(int((Nx-1)/2)):
                g.move(y=-(lb-base_x), x=-h1)
                g.move(y=-base_x, x=h1)
                g.move(y=-up_x, x=up_y)
            g.move(y=-(lb-base_x), x=-h1)
            g.move(y=-base_x, x=h1) 

            g.move(y=-(offset+j*(down_x-base_x)+np.floor(j/2)*(lb-up_x)))
            if j<Ny-1:
                
                g.move(x=(h1+down_y+up_y))


    return(down_y,up_y)
if __name__ =="__main__":
    g=G(outfile='Rotating_triangle_2D_soliton_sample.PGM')
    Kagome = "twist" #no twist variation 
    pcom=9
    defspeed=44*60 # mm/s
    normalpsi=20
    filthickness=0.100 # mm
    #numlayers=17
    numlayers=16
    layeroffset=0.5*filthickness
    g.set_pressure(pcom,normalpsi)
    os=5 # vertical offsets in printpath
    Nx = 10
    Ny = 10
    phi = 60*np.pi/180 #base triangle shapetwist_x,twist_y,h1,h2_new,top_x,top_y,twist_xshort,bot_x,
    alpha = 60*np.pi/180 #topological triangle shape
    beta = 90*np.pi/180 #twist angle
    lb = 10#mm
    lt = lb
    offset = 0
   
    h2 = 0.5*lt*np.tan(alpha) #height of topological triangle 
    h1 = lb*np.sin(phi) #height of structural triangle 
    g.toggle_pressure(pcom)
    g.feed(defspeed)
    for nz in range(0,numlayers):
        # def printstruct(edgelen,numextra,devangle,cw):

        if Kagome =="flat":
            g.write('M3') #start printing 
            printstruct_flat(Nx, Ny, phi, alpha, h1,h2, offset)
            g.write('M4') #end printing 
            g.move(y=(Ny-1)*(h1+h2))
            g.move(z=layeroffset)
            
        elif Kagome =="twist":    

            g.write('M3') #start printing 
            down_y,up_y=printstruct_twist(Nx, Ny, h1, h2, alpha, beta, phi, offset, lb, lt)
            g.write('M4') #end printing 
            g.move(x=-(np.floor((Ny-1)/2)*(h1+down_y+up_y)+np.ceil((Ny-1)/2)*(h1+down_y)))
            g.move(z=layeroffset)
            
    g.toggle_pressure(pcom)
    g.view(backend='matplotlib')
    g.teardown()
