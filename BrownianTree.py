import random


def vector_plus(p1, p2):
	l = []
	for i in range(len(p1)):
		l.append(p1[i]-p2[i])
	return l


class BrownianTree(object):

	def __init__(cls, width, height, seed_pos=[[0, 0]]):
		cls.map = [[0 for i in range(height)] for j in range(width)]
		cls.width, cls.height, cls.seed_pos = width, height, seed_pos
		for i in seed_pos:
			cls.map[i[0]][i[1]] = 1
		cls.walker_dir = [[i-1, j-1] for i in range(3) for j in range(3) if i-1 != 0 or j-1 != 0]


	def generate_tree(cls, particles, start_pos_list=[]):
		for i in range(particles):
			if start_pos_list != []:
				start_pos = start_pos_list[int(random.random()*len(start_pos_list))]
			else:
				start_pos = [int(random.random()*cls.width), int(random.random()*cls.height)]
			print 'walker start on %i, %i' % (start_pos[0], start_pos[1])
			cls.brownian_walker(start_pos)


	def particle_around(cls, cur_pos):
		'''
		'''
		for i in cls.walker_dir:
			tmp_around_pos = vector_plus(cur_pos, i)
			if cls.pos_in_field(tmp_around_pos) and cls.map[tmp_around_pos[0]][tmp_around_pos[1]] == 1:
				return True
		return False


	def pos_in_field(cls, pos):
		if pos[0] < 0 or pos[1] < 0 or pos[0] >= cls.height or pos[1] >= cls.width:
			return False
		return True


	def brownian_walker(cls, start_pos):
		'''
		'''
		if cls.map[start_pos[0]][start_pos[1]] == 1:
			return
		cnt = 0
		while not cls.particle_around(start_pos) and cnt < 50:
			cnt += 1
			tmp_pos = vector_plus(start_pos, cls.walker_dir[int(random.random()*len(cls.walker_dir))])
			if cls.pos_in_field(tmp_pos):
				start_pos = tmp_pos
		if cnt < 50:
			cls.map[start_pos[0]][start_pos[1]] = 1
		print 'particle set in %i, %i' % (start_pos[0], start_pos[1])
		return


	def print_map(cls):
		for i in cls.map:
			for j in i:
				if j == 0: print ' ',
				else: print '#',
			print ''



if __name__ == '__main__':
	width, height = 30, 30
	brownian_tree = BrownianTree(width, height, [[width/2, height/2], [10, 10], [20, 20]])
	border = [[i, 0] for i in range(width)]
	border.extend([[0, i] for i in range(height)])
	border.extend([[width-1, i] for i in range(height)])
	border.extend([[i, height-1] for i in range(width)])
	brownian_tree.generate_tree(300, border)
	brownian_tree.print_map()