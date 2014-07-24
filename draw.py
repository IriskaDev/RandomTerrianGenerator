from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ParticleSedimetary import ParticleSedimetary
import random

width = 80
length = 150

def rand():
	ret = random.gauss(0.5, 0.15)
	if ret < 0: ret = 0.0
	elif ret > 1.0: ret = .9
	return ret

def rand2():
	ret = .5
	return ret

p = ParticleSedimetary(width, length, 20)
p.search_radius = 2
p.altitude_threshold = 0.3
p.particle_height = 0.3
#p.field_walker(30000)
p.walker_start_pos = [int(width/2), int(length/2)]
p.walker(50000)
v = p.get_vertex_buffer()
idx = p.get_index_buffer()
color = p.get_color_buffer()
p.get_normal_buffer()
normal = p.normal_buffer

def init():
	glColor3f(.14, .66016, .8789)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	mat_specular = [1.0, 1.0, 1.0, 1.0]
	mat_shininess = [50.0]
	light_position = [0.0, 0.0, 40.0]
	white_light = [.14, .66016, .8789, 1.0]
	lmodel_ambient = [0.1, 0.1, 0.1, 1.0]
	glShadeModel(GL_SMOOTH)
	#glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
	glLightfv(GL_LIGHT0, GL_POSITION, light_position)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, white_light)
	#glLightfv(GL_LIGHT0, GL_SPECULAR, white_light)
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)



def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glColor3f(.14, .66016, .8789)
	#gluLookAt(50.0, 50.0, 130.0, 50.0, 50.0, 0.0, 0.0, 1.0, 0.0)
	gluLookAt(width/2.0, -75.0, 70.0, width/2.0, 50.0, 0.0, 0.0, 1.0, .0)
	#glEnableClientState(GL_COLOR_ARRAY)
	#glEnableClientState(GL_VERTEX_ARRAY)
	#glColorPointer(3, GL_FLOAT, 0, color)
	#glVertexPointer(3, GL_FLOAT, 0, v)
	#glDrawElements(GL_POINTS, len(idx), GL_UNSIGNED_BYTE, idx)
	for i in range(len(idx)/3):
		glBegin(GL_TRIANGLES)
		#gl begin
		glNormal3f(normal[idx[i*3]*3], normal[idx[i*3]*3+1], normal[idx[i*3]*3+2]) 
		glVertex3f(v[idx[i*3]*3], v[idx[i*3]*3+1], v[idx[i*3]*3+2]) 
		glNormal3f(normal[idx[i*3+1]*3], normal[idx[i*3+1]*3+1], normal[idx[i*3+1]*3+2]) 
		glVertex3f(v[idx[i*3+1]*3], v[idx[i*3+1]*3+1], v[idx[i*3+1]*3+2]) 
		glNormal3f(normal[idx[i*3+2]*3], normal[idx[i*3+2]*3+1], normal[idx[i*3+2]*3+2]) 
		glVertex3f(v[idx[i*3+2]*3], v[idx[i*3+2]*3+1], v[idx[i*3+2]*3+2]) 
		#gl end
		glEnd()
	glFlush()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w)/h, 1.5, 20000.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(800, 800)
	glutInitWindowPosition(100, 100)
	glutCreateWindow('hello')
	init();
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == '__main__':
	main()
