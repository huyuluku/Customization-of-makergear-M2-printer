import numpy as np
import m2py as mp
from pore_gauss import pore_gauss
from pore_gen import mirror_array
from pyDOE import lhs
import matplotlib.pyplot as plt
import pickle

plt.close('all')

def find_seg(line):
    uni = np.unique(line)
    if uni.size==1:
        return 1,np.array([line.size]),np.array([line[0]])
    else:
        seg_len = np.diff(np.where(np.diff(line)!=0)[0],prepend=-1,append=line.size-1)
        seg_num = seg_len.size
        seg_start = np.zeros(seg_num)
        seg_start[::2] = line[0]
        seg_start[1::2] = line[seg_len[0]]
        return seg_num,seg_len,seg_start
       
# coast distance default 2 mm
def print_line(m2,l,ch,coast,direction=1):
    tconst = 0.01
    m2.change_tool(change_to = ch)
    if np.abs(l*direction)<coast:
        m2.move(x=l*direction/2)
        m2.on(ch)
        m2.wait(np.abs(l*tconst*direction))
        m2.off(ch)
        m2.move(x=l*direction/2)
    else:
        m2.on(ch)
        m2.move(x=(l-coast)*direction)
        m2.off(ch)
        m2.move(x=coast*direction)
       
def one_line_two_mat(m2,line,dx,cdist,direct=1):
    if direct == -1:
        line = np.flip(line)
    seg_num,seg_len,seg_start = find_seg(line)
    for i in range(seg_num):
        print_line(m2,seg_len[i]*dx,int(seg_start[i])+1,cdist,direction=direct)
       
def print_two_phase(im,regionwidth,linewidth,mk,zdist=0.3,zlayer=2,c_dist=0.5,taplayer=0):
    
    region_repeat = int(regionwidth/linewidth)
    m,n = im.shape
    print_dir = 1 # keep track of direction 1 is to the right, -1 is to the left
    for zz in range(zlayer):
        if zz%2 == 0: 
            for i in range(taplayer):
                line = np.ones(im.shape[1])
                one_line_two_mat(mk,line,regionwidth,c_dist,direct=print_dir)
                print_dir=-print_dir
                mk.move(y=linewidth)
            for i in range(int(im.shape[0])):
                line = im[i,:]
                for j in range(region_repeat):
                    one_line_two_mat(mk,line,regionwidth,c_dist,direct=print_dir)
                    print_dir=-print_dir
                    mk.move(y=linewidth)
            for i in range(taplayer):
                line = np.ones(im.shape[1])
                one_line_two_mat(mk,line,regionwidth,c_dist,direct=print_dir)
                print_dir=-print_dir
                mk.move(y=linewidth)
            mk.move(y=-linewidth,z=zdist)
        else:
            for i in range(taplayer):
                line = np.ones(im.shape[1])
                one_line_two_mat(mk,line,regionwidth,c_dist,direct=print_dir)
                print_dir=-print_dir
                mk.move(y=-linewidth)
            for i in range(int(im.shape[0])):
                line = im[-i-1,:]
                for j in range(region_repeat):
                    one_line_two_mat(mk,line,regionwidth,c_dist,direct=print_dir)
                    print_dir=-print_dir
                    mk.move(y=-linewidth)
            for i in range(taplayer):
                line = np.ones(im.shape[1])
                one_line_two_mat(mk,line,regionwidth,c_dist,direct=print_dir)
                print_dir=-print_dir
                mk.move(y=-linewidth)
#    mk.home()
       
if __name__ == "__main__":
#    np.random.seed(2578)
    
    N=4
    W = 10
    thre = 0.3
    lam = 3
    lw = 0.4
    regionw = W/N
    
    model = pickle.load(open('PCA_model.p','rb'))
    n_component = 3.5
    z_sample = lhs(5,18)*n_component-n_component/2
    x_decoded = model.inverse_transform(z_sample)
    digit = x_decoded.reshape(18, N, N)
    digit = np.round((digit-np.min(digit,axis=0))/(np.max(digit,axis=0)-np.min(digit,axis=0)))
    im_array = mirror_array(digit,n=10)
    
    plot_row=4
    plot_col=4
    fig, axs = plt.subplots(plot_row,plot_col,figsize=(10,10))
    for i in range(plot_row):
        for j in range(plot_col):
            CS=axs[i,j].imshow(digit[i*plot_row+j,:,:])
            axs[i,j].axis('equal')
            axs[i,j].set_aspect('equal', adjustable='box')
            axs[i,j].set_yticklabels([])
            axs[i,j].set_xticklabels([])
            axs[i,j].set_yticks([])
            axs[i,j].set_xticks([])
    fig.suptitle('Generate Samples')
    plt.gray()
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    fefe
#    pore = pore_gauss(N,lam,lam,thre)
#    digit = pore.T_compute()*1
    im_array = mirror_array(digit[7,:,:])
    plt.figure()
    plt.imshow(im_array)
    plt.axis('off')
    
    mk = mp.Makergear('COM7', 115200, printout = 1,verbose=0)
    mk.speed(speed=30)
    mk.set_tool_coords(tool=1,x=0,y=0,z=0)
    mk.set_tool_coords(tool=2,x=39.2,y=0.0,z=-0.0)
    
    mk.home()
    mk.coord_sys(coord_sys = 'rel')
    xori = 5
    yori = 130
    zori = -125.1
    mk.move(x = xori, y = yori, z = zori, track = 0)  
    mk.move(x=0,y=0,z=0.3)
   
    im_array = mirror_array(digit[1,:,:])
    print_two_phase(im_array,regionw,lw,mk,zdist = 0.3,zlayer=2,c_dist=0.4,taplayer=25)
    mk.close()
    
    mk = mp.Makergear('COM7', 115200, printout = 1,verbose=0)
    mk.speed(speed=30)
    mk.set_tool_coords(tool=1,x=0,y=0,z=0)
    mk.set_tool_coords(tool=2,x=39.2,y=0.0,z=-0.0)
    
    mk.home()
    mk.coord_sys(coord_sys = 'rel')
    xori = 5
    yori = 175
    zori = -125.1
    mk.move(x = xori, y = yori, z = zori, track = 0)  
    mk.move(x=0,y=0,z=0.3)
    
    im_array = mirror_array(digit[12,:,:])
    print_two_phase(im_array,regionw,lw,mk,zdist = 0.3,zlayer=2,c_dist=0.4,taplayer=25)
    
    mk.close()
