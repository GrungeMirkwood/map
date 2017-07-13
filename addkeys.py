# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:37:36 2017

@author: Doug
"""
from plotmap import *
from dl_NASA_maps import *

import pyglet
import os.path

reqstr='N37E021'
imgstr=reqstr+".png"
if os.path.isfile(imgstr) is False:
    ll,file_list=getfilelist()
    fl=file_list[latlondata((reqstr[0],int(reqstr[1:3]),reqstr[3],int(reqstr[4:8])),ll)]
    img=unzip_draw(fl)[1]
    mountain = pyglet.image.load("C:\Users\Doug\Desktop\mapmakes\mountain.png").get_image_data()
    data=mountain.get_data('RGB',mountain.width*3)
    imgconvert=(img*256).astype(np.uint8).tobytes()
    imgmap=pyglet.image.ImageData(1201,1201,'RGB',imgconvert,1201*3)
    imgmap.save(imgstr)
else:
    imgmap=pyglet.image.load(imgstr)
    
image_part = imgmap.get_region(x=1, y=1, width=1000, height=1000)
sprite = pyglet.sprite.Sprite(image_part)
sprite.x=0
sprite.y=0
sprites=[]
sprites.append(sprite)
    
    
class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__(1000,1000)

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
            if self.zoomdist<-20:
                self.zoomdist=-20
        elif scroll_y==1:
            self.zoomdist=self.zoomdist+1
            if self.zoomdist>10:
                self.zoomdist=10
        for sprite in sprites:
            sprite.scale=(1-self.zoomdist*.1) 

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
            sprite.x=sprite.x+10;
        if keys[pyglet.window.key.RIGHT]:
            sprite.x=sprite.x-10;
        if keys[pyglet.window.key.DOWN]:
            sprite.y=sprite.y+10;
        if keys[pyglet.window.key.UP]:
            sprite.y=sprite.y-10;
        
        pass
    pyglet.clock.schedule_interval(update, 1/60.)
    # Call update 60 times a second


if __name__ == '__main__':
    window = HelloWorldWindow()
    keys = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keys)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())   
    pyglet.app.run()
    

    