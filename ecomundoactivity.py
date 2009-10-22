#!/usr/bin/env python

### Simulacion de un ecosistema, en el que existe pasto, conejos y zorros.
### By Gonzalo Odiard, 2006 godiard at gmail.com
### GPL License - http://www.gnu.org/copyleft/gpl.html

import gobject, gtk , cairo
import math, random
import os
import hippo

import pango
import logging
from gettext import gettext as _
import World,Animals,Green
import sugar
from sugar.activity import activity
from sugar.graphics import style
from sugar.graphics.toolbutton import ToolButton


world = World.World()

class Tile:
    def __init__ (self,x,y):
        self.X = x
        self.Y = y
        self.STATE = 0;


def drawGrid(ctx):    
    ctx.set_line_width(2)
    ctx.set_source_rgb(0,0,0)
    for n in range(0,World.CANT_TILES):
        ctx.move_to(World.MARGEN,World.MARGEN +(World.SIZE_TILE*n))
        ctx.line_to(World.SIZE_TILE * (World.CANT_TILES-1) + World.MARGEN,
            World.MARGEN +(World.SIZE_TILE*n))
        ctx.move_to(World.MARGEN +(World.SIZE_TILE*n),World.MARGEN)
        ctx.line_to(World.MARGEN +(World.SIZE_TILE*n),
            World.SIZE_TILE * (World.CANT_TILES-1)+ World.MARGEN)
        ctx.stroke()

def initWorld(): 
    world.state = []
    world.animals = []
    for n in range(0,World.CANT_TILES):
        world.state.append([])
        for p in range(0,World.CANT_TILES):
            tile = Tile(n,p)
            world.state[n].append(tile)
            

def drawStateWorld(ctx):
    #print "drawStateWorld"
    ctx.move_to(0,0)
    ctx.rectangle(0,0,World.SIZE_WORLD+(2*World.MARGEN),World.SIZE_WORLD+(2*World.MARGEN))
    #ctx.set_source_rgb(style.COLOR_PANEL_GREY.get_gdk_color())
    ctx.set_source_rgb(192.0/256.0,192.0/256.0,192.0/256.0)    
    ctx.fill()


    for n in range(0,World.CANT_TILES-1):
        for p in range(0,World.CANT_TILES-1):
            ctx.save()
            Green.getImagesGreen(world,ctx,n,p)
            #Green.getColorTile(world,ctx,n,p)
            ctx.restore()
    for n in range(len(world.animals)):
        #print "Animal",n
        animal = world.animals[n]
        ctx.save()
        animal.draw(ctx)
        ctx.restore()

def initGreen():
    for n in range(world.initialGreen):
        x = int(random.random()*World.CANT_TILES)
        y = int(random.random()*World.CANT_TILES)
        world.state[x][y].STATE = 2

def initAnimals():
    for n in range(world.initialRabbits):
        x = int(random.random()*(World.CANT_TILES-1))
        y = int(random.random()*(World.CANT_TILES-1))
        #print "Init Rabbit",x,y
        animal = Animals.Rabbit(x,y,world)
        world.animals.append(animal)
    for n in range(world.initialFoxs):
        x = int(random.random()*(World.CANT_TILES-1))
        y = int(random.random()*(World.CANT_TILES-1))
        #print "Init Fox",x,y
        animal = Animals.Fox(x,y,world)
        world.animals.append(animal)
                                        

def updateState(drawingarea):    
    #print "update State"
    if (world.playState):
        Green.grow(world)
        n = 0
        
        while (n < len(world.animals)):
            animal = world.animals[n]
            animal.move(world)
            if (not animal.checkLive()):
                cantAnimals = len(world.animals)
                world.animals[n] = cantAnimals
                world.animals.remove(cantAnimals)
            else :
                #Actualizo donde esta
                x1 = World.MARGEN+(World.SIZE_TILE*animal.posX)
                y1 = World.MARGEN +(World.SIZE_TILE*animal.posY)
                n = n+1
        drawingarea.queue_draw_area(0, 0,World.SIZE_WORLD, World.SIZE_WORLD)
        source_id = gobject.timeout_add(1000, updateState,drawingarea)    


class EcomundoActivity(activity.Activity):
    
    def __init__(self,handle):
        activity.Activity.__init__(self,handle)
        
        self.set_title("Ecomundo")
        print "Init activity Ecomundo"
        #print os.path.abspath(__file__)

        toolbox = activity.ActivityToolbox(self)
        self.toolbar = gtk.Toolbar()

        toolbox.add_toolbar(_('Ecomundo'), self.toolbar)
        self.toolbar.show()
        self.set_toolbox(toolbox)
        toolbox.show()

        self.btnNew = ToolButton('reload')
        self.btnNew.connect('clicked', self.onBtNewClicked)
        self.toolbar.insert(self.btnNew, -1)
        self.btnNew.show()

        self.btPlay = ToolButton('next')
        self.btPlay.connect('clicked', self.onBtPlayClicked)
        self.toolbar.insert(self.btPlay, -1)
        self.btPlay.show()

        self.btStop = ToolButton('process-stop')
        self.btStop.connect('clicked', self.onBtStopClicked)
        self.toolbar.insert(self.btStop, -1)
        self.btStop.show()

        self.btStop.props.sensitive = False;
        self.btPlay.props.sensitive = True;

        toolbox.set_current_toolbar(1)

        hBox = gtk.HBox(False, 0)
        self.set_canvas(hBox)
        
        self.drawingarea1 = gtk.DrawingArea()
        self.drawingarea1.set_size_request(World.SIZE_WORLD+(2*World.MARGEN),World.SIZE_WORLD+(2*World.MARGEN))
        self.drawingarea1.show()

        hBox.pack_start(self.drawingarea1, False, True, 5)
        
        table = gtk.Table(rows=4, columns=2, homogeneous=False)
        hBox.pack_start(table, False, False, 5)

        label_attributes = pango.AttrList()
        label_attributes.insert(pango.AttrSize(14000, 0, -1))
        label_attributes.insert(pango.AttrForeground(65535, 65535, 65535, 0, -1))

        lbTitle = gtk.Label()
        lbTitle.set_attributes(label_attributes)
        lbTitle.set_text(_('Initial Values'))
        #table.attach(lbTitle, 0, 1, 0, 1,yoptions=gtk.SHRINK,xpadding=5) 
        table.attach(lbTitle, 0, 2, 0, 1,yoptions=gtk.SHRINK,xpadding=10) 

        lbGreen = gtk.Label()
        lbGreen.set_attributes(label_attributes)
        lbGreen.set_text(_('Green'))
        table.attach(lbGreen, 0, 1, 1, 2,yoptions=gtk.SHRINK,xoptions=gtk.SHRINK,xpadding=10) 

        adjGreen = gtk.Adjustment(10, 1, 400, 1, 1, 0)
        self.spbGreen = gtk.SpinButton(adjustment=adjGreen, climb_rate=1.0, digits=2)
        table.attach(self.spbGreen, 1, 2, 1, 2,yoptions=gtk.SHRINK,xoptions=gtk.SHRINK,ypadding=10) 

        lbRabbit = gtk.Label()
        lbRabbit.set_attributes(label_attributes)
        lbRabbit.set_text(_('Rabbits'))
        table.attach(lbRabbit, 0, 1, 2, 3,yoptions=gtk.SHRINK,xoptions=gtk.SHRINK,xpadding=10)

        adjRabbit = gtk.Adjustment(10, 1, 400, 1, 1, 0)
        self.spbRabbit = gtk.SpinButton(adjustment=adjRabbit, climb_rate=1.0, digits=2)
        table.attach(self.spbRabbit, 1, 2, 2, 3,yoptions=gtk.SHRINK,xoptions=gtk.SHRINK,ypadding=10)

        lbFox = gtk.Label()
        lbFox.set_attributes(label_attributes)
        lbFox.set_text(_('Foxs'))
        table.attach(lbFox, 0, 1, 3, 4,yoptions=gtk.SHRINK,xoptions=gtk.SHRINK,xpadding=10)
        
        adjFox = gtk.Adjustment(10, 1, 400, 1, 1, 0)
        self.spbFox = gtk.SpinButton(adjustment=adjFox, climb_rate=1.0, digits=2)
        table.attach(self.spbFox, 1, 2, 3, 4,yoptions=gtk.SHRINK,xoptions=gtk.SHRINK,ypadding=10)


        print "test resize"
        print "antes de initWorld"
        initWorld()
        print "antes de init Green"
        initGreen()
        print "antes de init Animals"
        initAnimals()

        hBox.resize_children()
        hBox.show_all()

        self.drawingarea1.connect('expose-event', self.onDrawingAreaExposed)


    def onDrawingAreaExposed(self,da, event):
        #print "drawingarea exposed"
        x, y, width, height = da.allocation
        ctx = da.window.cairo_create()
        drawStateWorld(ctx)        
        drawGrid(ctx)

    def onBtPlayClicked(self,widget):
        self.btStop.props.sensitive = True;
        self.btPlay.props.sensitive = False;
        world.playState = True
        source_id = gobject.timeout_add(2000, updateState,self.drawingarea1)    
        # http://www.pygtk.org/pygtk2tutorial-es/ch-TimeoutsIOAndIdleFunctions.html#sec-Timeouts

    def onBtStopClicked(self,widget):
        self.btStop.props.sensitive = False;
        self.btPlay.props.sensitive = True;
        world.playState = False

    def onBtNewClicked(self,widget):
        initWorld()
        world.initialGreen = self.spbGreen.get_value_as_int()
        world.initialRabbits = self.spbRabbit.get_value_as_int()
        world.initialFoxs = self.spbFox.get_value_as_int()
        initGreen()
        initAnimals()
        # Despues de esto hay que recargar la pantalla
        drawingarea1 = self.drawingarea1
        ctx = drawingarea1.window.cairo_create()
        drawStateWorld(ctx)        
        drawGrid(ctx)

