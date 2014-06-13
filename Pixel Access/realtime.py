"""Direct pixel access examples."""
import sys
import draw
from timer import Timer

# Try to import SDL2. The import might fail, if the SDL2 DLL could not be
# loaded. In that case, just print the error and exit with a proper
# error code.
try:
	from sdl2 import *
	import sdl2.ext as sdl2ext
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

white = sdl2ext.Color(255, 255, 255)
black = sdl2ext.Color(0, 0, 0)

def draw_pixels(surface, xpix, ypix, grid):
	pixelview = sdl2ext.PixelView(surface)
	for y in range(ypix):
		for x in range(xpix):
			pixelview[y][x] = sdl2ext.Color(grid[y][x][0],grid[y][x][1],grid[y][x][2])   
			#if grid[y][x][0] == 255:
			#	pixelview[x][y] = white   
			#else:
			#	pixelview[x][y] = black
	del pixelview

def run(linefile):
	sdl2ext.init()
	for line in linefile:
		l = line.split()
		if len(l) == 0:
			pass
		elif l[0] == "pixels":
			xpix = int(l[1])
			ypix = int(l[2])
	window = sdl2ext.Window("Pixel Access", size=(xpix, ypix))
	window.show()
	windowsurface = window.get_surface()
	running = True
	while running:
		events = sdl2ext.get_events()
		for event in events:
			if event.type == SDL_QUIT:
				running = False
				break
		grid = draw.dofile(linefile)
		draw_pixels(windowsurface, xpix, ypix, grid)
		window.refresh()
	sdl2ext.quit()
	return 0
	'''		
	while running:
		events = sdl2ext.get_events()
		for event in events:
			if event.type == SDL_QUIT:
				running = False
				break
		with Timer() as t:
			grid = draw.dofile(linefile)
		print "=> elasped grid: %s s" % t.secs
		with Timer() as t:
			draw_pixels(windowsurface, xpix, ypix, grid)
		print "=> elasped render: %s s" % t.secs
		window.refresh()
	sdl2ext.quit()
	return 0
'''
def main(lines):
	f = open(lines,'r')
	l = f.readlines()
	run(l)

if __name__ == "__main__":
	main(sys.argv[1])
