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

def run():
	sdl2ext.init()
	draw.pixels(500, 500)
	window = sdl2ext.Window("Pixel Access", size=(draw.xpix, draw.ypix))
	window.show()
	renderer = sdl2ext.Renderer(window)
	running = True
	while running:
		events = sdl2ext.get_events()
		for event in events:
			if event.type == SDL_QUIT:
				running = False
				break
			if event.type == SDL_MOUSEBUTTONDOWN:
				#DO WORK HERE
				pass
		with Timer() as t:
			draw.setFrames(1,100)
			draw.screen(-2, 2, -2, 2)
			draw.pixels(500,500)
			draw.vary("turn", 0, 360, 1, 100)
			draw.trans_matrix = draw.rotate_y("turn", draw.trans_matrix)
			draw.trans_matrix = draw.move(0, -.05, 0, draw.trans_matrix)
			draw.trans_matrix = draw.scale(.75, .75, .75, draw.trans_matrix)
			draw.trans_matrix = draw.rotate_x(30, draw.trans_matrix)
			draw.sphere_t(1.2, 1, 0.37, 0, 0, 0, 0, 0, 0)
			print draw.trans_matrix
			print draw.frames
			print draw.currentframe
			print draw.varys
			draw.render_parallel()
			grid = draw.end()
		print "=> elasped grid: %s s" % t.secs
		with Timer() as t:
			draw_pixels(renderer, draw.xpix, draw.ypix, grid)
		print "=> elasped render: %s s" % t.secs
		window.refresh()
	sdl2ext.quit()
	return 0

if __name__ == "__main__":
	run()