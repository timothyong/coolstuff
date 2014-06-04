import sys
import draw
from timer import Timer

try:
	from sdl2 import *
	import sdl2.ext as sdl2ext
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

white = sdl2ext.Color(255, 255, 255)
black = sdl2ext.Color(0, 0, 0)

def draw_pixels(renderer, xpix, ypix, grid):
	renderer.clear()
	for line in grid:
		renderer.draw_line(line, white)
	renderer.present()

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
	renderer = sdl2ext.Renderer(window)
	running = True
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
			draw_pixels(renderer, xpix, ypix, grid)
		print "=> elasped render: %s s" % t.secs
		window.refresh()
	sdl2ext.quit()
	return 0

def main(lines):
	f = open(lines,'r')
	l = f.readlines()
	run(l)

if __name__ == "__main__":
	main(sys.argv[1])