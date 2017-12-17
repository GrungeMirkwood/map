# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:37:36 2017

@author: Doug
"""
from plotmap import *
from dl_NASA_maps import *

import pyglet
import os.path

class MapTile(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs): 
        super(MapTile, self).__init__(*args, **kwargs)
        self.xoff=0
        self.yoff=0
        self.origin=False
#    def update(self, dt): 
#        self.x += self.velocity_x * dt 
#        self.y += self.velocity_y * dt

reqstr=[]
origin='N36E021'


#calc origin
if  origin[0]=='N':
    yorigin=1*int(origin[1:3])
else:
    yorigin=-1*int(origin[1:3])
if  origin[3]=='E':
    xorigin=1*int(origin[4:8])
else:
    xorigin=-1*int(origin[4:8])

def namefromorigdist(xorigin,yorigin,xdist,ydist):
    name=str()    
    print xdist,ydist    
    if ydist-yorigin>=0:
        name=name+'N'
    else:
        name=name+'S'
    name=name+"{0:02d}".format(abs(ydist))
    if xdist-xorigin>=0:
        name=name+'E'
    else:
        name=name+'W'
    name=name+"{0:03d}".format(abs(xdist))
    return name
    
tiling_distance=15
for i in range(0,tiling_distance):
    for j in range(0,tiling_distance):
        reqstr.append(namefromorigdist(xorigin,yorigin,xorigin+i,yorigin+j))
        
print reqstr
#qreqstr=reqstr
#reqstr=['N37E021','N37E022','N37E023','N38E021','N38E022','N38E023','N36E021','N36E022','N36E023']
sprites=[]
for reqst in reqstr:
    #check if file already DL'ed. if not, DL and save png  
    imgstr=reqst+".png"
    if os.path.isfile(imgstr) is False:
        print "getting filelist"
        ll,file_list=getfilelist()
for reqst in reqstr:
    #check if file already DL'ed. if not, DL and save png  
    imgstr=reqst+".png"
    if os.path.isfile(imgstr) is False:
        fileindex=latlondata((reqst[0],int(reqst[1:3]),reqst[3],int(reqst[4:8])),ll)        
        if fileindex is not None:        
            fl=file_list[latlondata((reqst[0],int(reqst[1:3]),reqst[3],int(reqst[4:8])),ll)]
            img=unzip_draw(fl)[1]
        else:
            img=np.concatenate((np.zeros((1201,1201,2)),np.ones((1201,1201,1))),axis=2)
        imgconvert=(img*255).astype(np.uint8).tobytes()
        imgmap=pyglet.image.ImageData(1201,1201,'RGB',imgconvert,-1201*3)
        imgmap.save(imgstr)
    else:
        imgmap=pyglet.image.load(imgstr)
    
    #calc map offsetting
    if  reqst[0]=='N':
        yoff=1*int(reqst[1:3])
    else:
        yoff=-1*int(reqst[1:3])
    if  reqst[3]=='E':
        xoff=1*int(reqst[4:8])
    else:
        xoff=-1*int(reqst[4:8])

    yoffori=yorigin-yoff
    xoffori=xorigin-xoff
    
    image_part = imgmap.get_region(x=0, y=0, width=1201, height=1201)
    #create sprite at offset    
    mtile = MapTile(image_part)
    mtile.x=-xoffori*1201
    mtile.y=-yoffori*1201
    mtile.xoff=-xoffori
    mtile.yoff=-yoffori
    if mtile.xoff == 0 and mtile.yoff == 0:
        mtile.origin=True
    sprites.append(mtile)
    origin=sprites[0]

        
class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__(1900,1000)

        self.label = pyglet.text.Label('Hello, KIRA!')
        self.zoomdist=0
    def on_draw(self):
        self.clear()
        self.label.draw()
        for sprite in sprites:
            sprite.draw()

    def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
        #print repr(x)+" "+repr(y)+" "+repr(scroll_x)+" "+repr(scroll_y)+" "    
        if scroll_y==-1:
            self.zoomdist=self.zoomdist-1
            if self.zoomdist<-25:
                self.zoomdist=-25
        elif scroll_y==1:
            self.zoomdist=self.zoomdist+1
            if self.zoomdist>20:
                self.zoomdist=20
        for sprite in sprites:
            prevx=sprite.x
            prevy=sprite.y
            scale=(np.exp(self.zoomdist/4.0))
            sprite.scale=scale
            print sprite.x,sprite.y,sprite.width,sprite.height,sprite.xoff,sprite.yoff,x,y
            if sprite.xoff != 0:
                sprite.x=sprite.width*sprite.xoff+origin.x
            if sprite.yoff != 0:
                sprite.y=sprite.height*sprite.yoff+origin.y
            print "after"
            print sprite.x,sprite.y,sprite.width,sprite.height
#        for sprite in sprites:
#            sprite.y=sprite.y-(y-prevy)
#            sprite.x=sprite.x-(x-prevx)
#    def on_key_press(self,key,modifiers):
#        if key==pyglet.window.key.LEFT:
#            sprite.x=sprite.x-1;
#        if key==pyglet.window.key.RIGHT:
#            sprite.x=sprite.x+1;
#        if key==pyglet.window.key.DOWN:
#            sprite.y=sprite.y-1;
#        if key==pyglet.window.key.UP:
#            sprite.y=sprite.y+1;

    def update(dt):
        # Move 10 pixels per second
        #sprite.x += dt * 10
        if keys[pyglet.window.key.LEFT]:
            for sprite in sprites:            
                sprite.x=sprite.x+10;
        if keys[pyglet.window.key.RIGHT]:
            for sprite in sprites:
                sprite.x=sprite.x-10;
        if keys[pyglet.window.key.DOWN]:
            for sprite in sprites:
                sprite.y=sprite.y+10;
        if keys[pyglet.window.key.UP]:
            for sprite in sprites:
                sprite.y=sprite.y-10;
        
        pass
    pyglet.clock.schedule_interval(update, 1/120.)
    # Call update 60 times a second


if __name__ == '__main__':
    window = HelloWorldWindow()
    keys = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keys)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())   
    pyglet.app.run()
    

    