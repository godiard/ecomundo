### By Gonzalo Odiard, 2006 godiard at gmail.com
### GPL License - http://www.gnu.org/copyleft/gpl.html

import gobject, gtk , cairo, os
import World

print "Init Green"
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"images")

print "Despues de ver el path"
image1 = cairo.ImageSurface.create_from_png (os.path.join(path,"green1.png"))
image2 = cairo.ImageSurface.create_from_png (os.path.join(path,"green2.png"))
image3 = cairo.ImageSurface.create_from_png (os.path.join(path,"green3.png"))
image4 = cairo.ImageSurface.create_from_png (os.path.join(path,"green4.png"))

def getImagesGreen(world,ctx,n,p):
	state = world.state[n][p].STATE
	x1 = World.MARGEN+(World.SIZE_TILE*n)
	y1 = World.MARGEN +(World.SIZE_TILE*p)
	ctx.move_to(x1,y1)
	ctx.translate(x1,y1)
	ctx.rectangle(0,0,World.SIZE_TILE,World.SIZE_TILE);
	ctx.set_source_rgb(146.0/256.0,98.0/256.0,46.0/256.0)	
	if state ==1:
		ctx.set_source_surface(image1,1,1)
	elif state ==2:
		ctx.set_source_surface(image2,1,1)
	elif state ==3:
		ctx.set_source_surface(image3,1,1)
	elif state ==4:
		ctx.set_source_surface(image4,1,1)
	ctx.fill()

# MARRON RGB 146,98,46
# VERDE1 166,202,128
# VERDE2 127,175,76
# VERDE3 102,160,40
# VERDE4 78,143,8

def getColorTile(world,ctx,n,p):
	state = world.state[n][p].STATE
	#print state
	x1 = World.MARGEN+(World.SIZE_TILE*n)
	y1 = World.MARGEN +(World.SIZE_TILE*p)
	ctx.move_to(x1,y1)
	ctx.rectangle(x1,y1,World.SIZE_TILE,World.SIZE_TILE);

	if state == 0:
		ctx.set_source_rgb(146.0/256.0,98.0/256.0,46.0/256.0)
	elif state ==1:
		ctx.set_source_rgb(166.0/256.0,202.0/256.0,128.0/256.0)
	elif state ==2:
		ctx.set_source_rgb(127.0/256.0,175.0/256.0,76.0/256.0)
	elif state ==3:
		ctx.set_source_rgb(102.0/256.0,160.0/256.0,40.0/256.0)
	elif state ==4:
		ctx.set_source_rgb(78.0/256.0,143.0/256.0,8.0/256.0)
	ctx.fill()


def grow(world):
	for n in range(0,World.CANT_TILES-1):
		for p in range(0,World.CANT_TILES-1):
			if ((world.state[n][p].STATE != 0) and 
				(world.state[n][p].STATE < 4)):
				world.state[n][p].STATE = world.state[n][p].STATE + 1
				x1 = World.MARGEN+(World.SIZE_TILE*n)
				y1 = World.MARGEN +(World.SIZE_TILE*p)
				#drawingarea.queue_draw_area(x1, y1, World.SIZE_TILE, World.SIZE_TILE)
			level = 0
			if (world.state[n][p].STATE == 0):
				if (n != 0) and (world.state[n-1][p].STATE > 1):
					level = level + world.state[n-1][p].STATE
				if ((n != 0) and (p != 0) and 
					(world.state[n-1][p-1].STATE > 1)):
					level = level + world.state[n-1][p-1].STATE
				if ((n != 0) and (p < World.CANT_TILES) and 
					(world.state[n-1][p+1].STATE > 1)):
					level = level + world.state[n-1][p+1].STATE
				if (p != 0) and (world.state[n][p-1].STATE > 1):
					level = level + world.state[n][p-1].STATE
				if (p < World.CANT_TILES) and (world.state[n][p+1].STATE > 1):
					level = level + world.state[n][p+1].STATE
				if (n < World.CANT_TILES) and (world.state[n+1][p].STATE > 1):
					level = level + world.state[n+1][p].STATE
				if ((n < World.CANT_TILES) and (p != 0) and 
					(world.state[n+1][p-1].STATE > 1)):
					level = level + world.state[n+1][p-1].STATE
				if ((n < World.CANT_TILES) and (p < World.CANT_TILES) and 
					(world.state[n+1][p+1].STATE > 1 )):
					level = level + world.state[n+1][p+1].STATE
				if (level > 3):
					world.state[n][p].STATE = 1
					x1 = World.MARGEN+(World.SIZE_TILE*n)
					y1 = World.MARGEN +(World.SIZE_TILE*p)
					#drawingarea.queue_draw_area(x1, y1, World.SIZE_TILE, World.SIZE_TILE)
