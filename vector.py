import math


def cross_mutiplie3D(p1, p2):
	return [p1[1]*p2[2]-p1[2]*p2[1], p1[2]*p2[0]-p1[0]*p2[2], p1[0]*p2[1]-p1[1]*p2[0]]

def dot_mutiplie(p1, p2):
	ret = 0
	if len(p1) != len(p2):
		raise Exception('the dimension of two input vecotr is not equal')
	for i in range(len(p1)):
		ret += p1[i]*p2[i]
	return ret

def vector_plus(p1, p2):
	l = []
	if len(p1) != len(p2):
		raise Exception('the dimension of two input vecotr is not equal')
	for i in range(len(p1)):
		l.append(p1[i]+p2[i])
	return l

def vector_rev(p1):
	return [-i for i in p1]

def vector_divide(p1, div):
	if div == 0:
		raise Exception('the division element is 0!')
	return [i/div for i in p1]

def vector_mutiplie(p1, mut):
	return [i*mut for i in p1]

def vector_normalize(p1):
	v_len = math.sqrt(sum([i**2 for i in p1]))
	return [i/v_len for i in p1]

def vector_len(p1):
	return math.sqrt(sum([i**2 for i in p1]))

def vector_distance_of(p1, p2):
	if len(p1) != len(p2):
		raise Exception('the dimension of two input vector is not equal')
	return math.sqrt(sum([i**2 for i in vector_plus(p1, vector_rev(p2))]))

def vector_distance_pow_2(p1, p2):
	if len(p1) != len (p2):
		raise Exception('the dimension of two input vector is not equal')
	return sum([i**2 for i in vector_plus(p1, vector_rev(p2))])

def vector_mutilp_plus():
	pass
