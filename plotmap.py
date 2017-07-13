# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 20:20:49 2016

@author: Doug
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import numpy as np

def zerolocs(data,value=-1):
    for line in range (len(data)):
        for point in range (len(data[0])):
            if (data[line][point]==-32768):
                #print repr(line)+','+repr(point) + 'has zero'
                if value!=-1:
                    data[line][point]=value
    return data
    
def printnonzero(data):
    for line in range (len(data)):
        nonzero=False
        for point in range (len(data[0])):
            if (data[line][point]!=0):
                nonzero=True
        if nonzero==True:
            #print line
            pass
    
            
def zerothresh(data,valueth=0):
    for line in range (len(data)):
        for point in range (len(data[0])):
            if (data[line][point]<valueth):
                #print repr(line)+','+repr(point)+': '+repr(data[line][point]) + ' -less than zero'
                data[line][point]=0
    return data

def cleandatas(vdata):
    print "max:"+repr(np.amax(vdata))
    print "min:"+repr(np.amin(vdata))
    print "setting nodata to 0..."
    #set nodatas to zeros for now
    data=zerolocs(vdata,0)
    #set negatives to 0
    print "max:"+repr(np.amax(data))
    print "min:"+repr(np.amin(data))
    print "setting negative values to 0..."
    rdata=zerothresh(data,0)
    print "max:"+repr(np.amax(rdata))
    print "min:"+repr(np.amin(rdata))
    return rdata


def map_2_img(data,plot=False):
    
    arraytry=np.ndarray(shape=(1201,1201,3), dtype=float, order='F')
    #ghetto scale to 8 bit, set green channel to inverted heightmap, so brighter is higher       
    #normallize   float(np.amax(data)) 
    arraytry[:,:,1]=data/3500.0
    #zerray= np.zeros(1024,1024)
    for line in range(len(data)):
        for point in range (len(data[0])):
            if data[line][point]<1.0:
                arraytry[line,point,2]=1
            
    if plot==True:
        imgplot = plt.imshow(arraytry)
    else:
        return arraytry
    
def pltmap(maps):
    fig=plt.figure()
    
    outer_grid = gridspec.GridSpec(2, 2, wspace=0.0, hspace=0.0)
    offset_x=[0,.5,0,.5]
    offset_y=[0.5,.5,0,0]
    for idx in range(0,len(maps)):
        print idx             
        #fig.add_subplot(ax)
        ax=fig.add_axes([0+offset_x[idx], 0+offset_y[idx], 0.5, 0.5])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.imshow(maps[idx])
    plt.show()
    
def gridmap(maps,x=1,y=1):
    fig = plt.figure(figsize=(8, 8))
    gs1 = gridspec.GridSpec(x, y, wspace=0.0, hspace=0.0)
    offset_x=[0,.5,0,.5]
    offset_y=[0.5,.5,0,0]
    for idx in range(0,len(maps)):
        print idx             
        #fig.add_subplot(ax)
        ax=plt.subplot(gs1[idx])
        plt.imshow(maps[idx])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
    all_axes = fig.get_axes()
    #show only the outside spines
    for ax in all_axes:
        for sp in ax.spines.values():
            sp.set_visible(False)
        if ax.is_first_row():
            ax.spines['top'].set_visible(True)
        if ax.is_last_row():
            ax.spines['bottom'].set_visible(True)
        if ax.is_first_col():
            ax.spines['left'].set_visible(True)
        if ax.is_last_col():
            ax.spines['right'].set_visible(True)
    gs1.tight_layout(fig)
    plt.show()
    
    gs1.update(wspace=0.0, hspace=0.0)