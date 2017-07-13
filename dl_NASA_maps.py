# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 20:37:11 2016

@author: Doug
"""
import requests
import StringIO
import zipfile
import os
import sys
import math
import numpy as np
from plotmap import *
urly='http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/Eurasia/'
zfn=0
def getfilelist():
    r=requests.get(urly)
    
    file_list=[]
    for line in r.iter_lines():
        if line: 
            print line
            href=line.find("a href=")
            zipf=line.find(".zip\"")
            if href>=0 and zipf>=0:
                filename=line[13:zipf+4]
                file_list.append(filename)
    

    
    i=0
    ll=[]
    for item in file_list:
        ll.append((item[0],int(item[1:3]),item[3], int(item[4:7]),i))
        i=i+1
    return ll, file_list
#extract to dict
def extract_zip(input_zip):
    input_zip=zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}

def unzip_draw(filelist):
    #dl file   
    zf=requests.get(urly+filelist,stream=True)    
    zfn=extract_zip(StringIO.StringIO(zf.content))
    print "downloading and extracting "+ filelist+ "..."
    # process into numpy array
    #siz = os.path.getsize(zfn)
    siz = len(zfn[zfn.keys()[0]])
    dim = int(math.sqrt(siz/2))
    print siz
    #assert dim*dim*2 == siz, 'Invalid file size'
    
    data = np.fromstring(zfn[zfn.keys()[0]], np.dtype('>i2'), dim*dim).reshape((dim, dim))
    
    return zfn,map_2_img(cleandatas(data))


#function for finding map tiles in the file list.  missing tiles are returned as an all 0 elevation tile
def latlondata(latlon,ll):
    for i in range(0,len(ll)-1):            
        if latlon[1] == ll[i][1] and latlon[3] == ll[i][3] and latlon[0] == ll[i][0] and latlon[2] == ll[i][2]:
            return ll[i][4]

        
    
#ll,file_list=getfilelist()
#fl=latlondata(('S',10,'W',158),ll)