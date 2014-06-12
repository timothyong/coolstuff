import math
from math import sin, cos
import matrix


#*****UTILS*****
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def is_var(var):
	if var in varys:
		return varys[var]['current']
	else:
		return float(var)

def add_triangle(p1, p2, p3, l):
	l.append(p1[:])
	l.append(p2[:])
	l.append(p3[:])
	return l

def convert_points(matrix):
	global xmax, xmin, ymin, ymax
	global xpix, ypix
	for point in matrix:
		point[0] = int(round(xpix * (point[0] - xmin)/(abs(xmin) + abs(xmax))))
		point[1] = int(round(ypix * (ymax - point[1])/(abs(ymin) + abs(ymax))))
	return matrix

def vary(var, start, end, sframe, eframe):
	global varys
	v = var
	if not var in varys:
		varys[v] = {}
		varys[v]['current'] = start
		varys[v]['end'] = end
		varys[v]['sframe'] = sframe
		varys[v]['eframe'] = eframe
		varys[v]['rate'] = (end - start) / (eframe - sframe)
	else:
		if currentframe >= sframe and currentframe <= eframe:
				varys[v]['rate'] = (end - start) / (eframe - sframe)
				varys[v]['current'] += varys[v]['rate']

def save(name):
	global pushes, trans_matrix
	pushes[name] = trans_matrix

def restore(name):
	global pushes, trans_matrix
	trans_matrix = pushes[name]

def end():
	global triangle_matrix, trans_matrix, grid, varys, pushes
	triangle_matrix = []
	g = grid
	grid = []
	trans_matrix = matrix.create_identity_matrix()
	pushes = {}
	return g

def isvisible(ex, ey, ez, tmat):
	m = []
	for i in range(0, len(tmat), 3):
		p1 = tmat[i]
		p2 = tmat[i+1]
		p3 = tmat[i+2]
		t1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
		t2 = [p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]]
		s = [p1[0] - ex, p1[1] - ey, p1[2] - ez]
		d = dot_product(s, cross_product(t1, t2))
		if d < 0:
			m.append(tmat[i][:])
			m.append(tmat[i+1][:])
			m.append(tmat[i+2][:])
	return m

def isvisible_parallel(tmat):
	m = []
	for i in range(0, len(tmat), 3):
		p1 = tmat[i]
		p2 = tmat[i+1]
		p3 = tmat[i+2]
		t1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
		t2 = [p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]]
		d = cross_product(t1, t2)
		if d[2] >= 0:
			m.append(tmat[i][:])
			m.append(tmat[i+1][:])
			m.append(tmat[i+2][:])
	return m

#*****SETUP*****
def setFrames(start, end):
	global frames, currentframe, done
	if currentframe == -1:
		frames = end
		currentframe = start
	else:
		currentframe += 1
		if currentframe == frames:
			currentframe = 0

def screen(xmin1, xmax1, ymin1, ymax1):
	global xmin, ymin, xmax, ymax
	xmin = xmin1
	ymin = ymin1
	xmax = xmax1
	ymax = ymax1


def pixels(xpix1, ypix1):
	global xpix, ypix, grid
	xpix = xpix1
	ypix = ypix1
	grid = []

#*****DRAW LINE*****
def draw_triangle(x1, y1, x2, y2, x3, y3):
	draw_line(x1, y1, x2, y2)
	draw_line(x2, y2, x3, y3)
	draw_line(x1, y1, x3, y3)

def draw_line(x1, y1, x2, y2):
	global grid
	grid.append([x1,y1,x2,y2])

#*****TRANSFORM*****
def move(dx, dy, dz, m):
	dx = is_var(dx)
	dy = is_var(dy)
	dz = is_var(dz)
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][3] = dx
	new_matrix[1][3] = dy
	new_matrix[2][3] = dz
	return matrix.multiply_matrices(m, new_matrix)

def scale(sx, sy, sz, m):
	sx = is_var(sx)
	sy = is_var(sy)
	sz = is_var(sz)
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = sx
	new_matrix[1][1] = sy
	new_matrix[2][2] = sz
	return matrix.multiply_matrices(m, new_matrix)


def rotate_x(degrees, m):
	degrees = is_var(degrees)
	new_matrix = matrix.create_identity_matrix()
	new_matrix[1][1] = math.cos(math.radians(degrees))
	new_matrix[1][2] = 0 - math.sin(math.radians(degrees))
	new_matrix[2][1] = math.sin(math.radians(degrees))
	new_matrix[2][2] = math.cos(math.radians(degrees))
	return matrix.multiply_matrices(m, new_matrix)

def rotate_y(degrees, m):
	degrees = is_var(degrees)
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = math.cos(math.radians(degrees))
	new_matrix[0][2] = math.sin(math.radians(degrees))
	new_matrix[2][0] = 0 - math.sin(math.radians(degrees))
	new_matrix[2][2] = math.cos(math.radians(degrees))
	return matrix.multiply_matrices(m, new_matrix)

def rotate_z(degrees, m):
	degrees = is_var(degrees)
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = math.cos(math.radians(degrees))
	new_matrix[0][1] = 0 - math.sin(math.radians(degrees))
	new_matrix[1][0] = math.sin(math.radians(degrees))
	new_matrix[1][1] = math.cos(math.radians(degrees))
	return matrix.multiply_matrices(m, new_matrix)

def transform(trans_m, m):
	for i in range(len(m)):
		x = matrix.multiply_point_matrix(trans_m, m[i])
		m[i] = x
	return m

#******RENDER*****
def render_parallel():
	new_matrix = isvisible_parallel(triangle_matrix)
	new_matrix = convert_points(new_matrix)
	for i in range(0, len(new_matrix), 3):
		p1 = new_matrix[i]
		p2 = new_matrix[i+1]
		p3 = new_matrix[i+2]
		draw_triangle(p1[0],p1[1], p2[0], p2[1], p3[0], p3[1])

def render_perspective_cyclops(ex, ey, ez):
	new_matrix = isvisible(ex, ey, ez, triangle_matrix)
	for i in range(len(new_matrix)):
		new_matrix[i][0] = ex-(ez * (new_matrix[i][0] - ex) / (new_matrix[i][2] - ez))
		new_matrix[i][1] = ey-(ez * (new_matrix[i][1] - ey) / (new_matrix[i][2] - ez))
	new_matrix = convert_points(new_matrix)
	for i in range(0, len(new_matrix), 3):
		p1 = new_matrix[i]
		p2 = new_matrix[i+1]
		p3 = new_matrix[i+2]
		draw_triangle(p1[0],p1[1], p2[0], p2[1], p3[0], p3[1])

def render_perspective_stereo(ex1, ey1, ez1, ex2, ey2, ez2):
	global r, g, b
	g = 0
	b = 0
	render_perspective_cyclops(ex1, ey1, ez1)
	r = 0
	g = 127
	b = 127
	render_perspective_cyclops(ex2, ey2, ez2)

#*****SHAPES*****
def box_t(sx, sy, sz, rx, ry, rz, mx, my, mz):
	global triangle_matrix
	sx = is_var(sx)
	sy = is_var(sy)
	sz = is_var(sz)
	rx = is_var(rx)
	ry = is_var(ry)
	rz = is_var(rz)
	mx = is_var(mx)
	my = is_var(my)
	mz = is_var(mz)
	p0 = [.5, .5, .5, 1]
	p1 = [.5, -.5, .5, 1]
	p2 = [-.5, -.5, .5, 1]
	p3 = [-.5, .5, .5, 1]
	p4 = [.5, .5, -.5, 1]
	p5 = [.5, -.5, -.5, 1]
	p6 = [-.5, -.5, -.5, 1]
	p7 = [-.5, .5,  -.5, 1]
	box_triangles = []
	box_triangles = add_triangle(p0, p2, p1, box_triangles)
	box_triangles = add_triangle(p3, p2, p0, box_triangles)
	box_triangles = add_triangle(p7, p6, p2, box_triangles)
	box_triangles = add_triangle(p7, p2, p3, box_triangles)
	box_triangles = add_triangle(p0, p1, p5, box_triangles)
	box_triangles = add_triangle(p0, p5, p4, box_triangles)
	box_triangles = add_triangle(p7, p5, p6, box_triangles)
	box_triangles = add_triangle(p4, p5, p7, box_triangles)
	box_triangles = add_triangle(p4, p7, p3, box_triangles)
	box_triangles = add_triangle(p3, p0, p4, box_triangles)
	box_triangles = add_triangle(p2, p6, p5, box_triangles)
	box_triangles = add_triangle(p1, p2, p5, box_triangles)
	box_triangles = transform(scale(sx, sy, sz, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(rotate_x(rx, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(rotate_y(ry, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(rotate_z(rz, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(move(mx, my, mz, matrix.create_identity_matrix()), box_triangles)
	#box_triangles = transform(trans_matrix, box_triangles)
	return box_triangles
	#triangle_matrix = triangle_matrix + box_triangles

def sphere_t(sx, sy, sz, rx, ry, rz, mx, my, mz):
	global triangle_matrix
	sx = is_var(sx)
	sy = is_var(sy)
	sz = is_var(sz)
	rx = is_var(rx)
	ry = is_var(ry)
	rz = is_var(rz)
	mx = is_var(mx)
	my = is_var(my)
	mz = is_var(mz)
	sphere_matrix = []
	theta = 0
	phi = 0
	while theta < 2*math.pi:
		phi = 0
		while phi < math.pi:
			t1 = theta
			p1 = phi
			t2 = theta + 2*math.pi / CIRCLELINES
			p2 = phi + math.pi / CIRCLELINES

			x1 = sin(p1) * cos(t1)
			y1 = sin(p1) * sin(t1)
			z1 = cos(p1)
			x2 = sin(p1) * cos(t2)
			y2 = sin(p1) * sin(t2)
			z2 = cos(p1)
			x3 = sin(p2) * cos(t2)
			y3 = sin(p2) * sin(t2)
			z3 = cos(p2)
			sphere_matrix = add_triangle([x3, y3, z3, 1], [x2, y2, z2, 1], [x1, y1, z1, 1], sphere_matrix) 
			x1 = sin(p1) * cos(t1)
			y1 = sin(p1) * sin(t1)
			z1 = cos(p1)
			x2 = sin(p2) * cos(t2)
			y2 = sin(p2) * sin(t2)
			z2 = cos(p2)
			x3 = sin(p2) * cos(t1)
			y3 = sin(p2) * sin(t1)
			z3 = cos(p2)
			sphere_matrix = add_triangle([x3, y3, z3, 1], [x2, y2, z2, 1], [x1, y1, z1, 1], sphere_matrix) 
			phi += math.pi / CIRCLELINES
		theta += 2*math.pi / CIRCLELINES
	sphere_matrix = transform(scale(sx, sy, sz, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(rotate_x(rx, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(rotate_y(ry, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(rotate_z(rz, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(move(mx, my, mz, matrix.create_identity_matrix()), sphere_matrix)
	#sphere_matrix = transform(trans_matrix, sphere_matrix)
	triangle_matrix = triangle_matrix + sphere_matrix

#*****MATRIXES*****
def dot_product(l1, l2):
	ans = 0
	for i in range(len(l1)):
		ans += l1[i]*l2[i]
	return ans

def cross_product(l1, l2):
	return_matrix = []
	return_matrix.append(l1[1]*l2[2] - l1[2]*l2[1])
	return_matrix.append(l1[2]*l2[0] - l1[0]*l2[2])
	return_matrix.append(l1[0]*l2[1] - l1[1]*l2[0])
	return return_matrix

######

CIRCLELINES = 20

######

r = 255
g = 255
b = 255
filename = "default"
trans_matrix = matrix.create_identity_matrix()
triangle_matrix = []
xmax = 0
xmin = 0
ymax = 0
ymin = 0
grid = 0
xpix = 0
ypix = 0
frames = 0
currentframe = -1
varys = {}
done = False
pushes = {}
