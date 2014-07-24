import math
import random
import vector


class ParticleSedimetary:

	def __init__(self, width, length, height):
		self.width = width
		self.length = length
		self.height = height
		self.point_matrix = []
		self.search_radius = 1 
		self.altitude_field = []
		self.altitude_threshold = 1
		self.particle_height = 1
		self.vertex_buffer = []
		self.index_buffer = []
		self.normal_buffer = []
		self.color_buffer = []
		self.face_normal = []
		self.walker_direction = [[i-1, j-1] for i in range(3) for j in range(3) if i-1 != 0 or j-1 != 0]
		self.walker_start_pos = [0, 0]
		for i in range(width):
			self.point_matrix.append([])
			for j in range(length):
				self.point_matrix[i].append([float(i), float(j), 0.0])

	
	def walker(self, steps):
		'''
			walk throught the field and drop particles.
		'''
		cur_pos = list(self.walker_start_pos)
		sr_pow_2 = self.search_radius ** 2
		for i in range(steps):
			dir_idx = int(random.random() * 8)
			#drop_num = 1 + int(random.random() * 50)
			drop_num = 1 + int(random.random()*0)
			tmp_pos = vector.vector_plus(cur_pos, self.walker_direction[dir_idx])
			if tmp_pos[0] < self.width and tmp_pos[0] >= 0 \
				and tmp_pos[1] < self.length and tmp_pos[1] >= 0:
				cur_pos = tmp_pos
				center = list(self.point_matrix[cur_pos[0]][cur_pos[1]])
				for j in range(drop_num):
					drop_position = self.search_ava_position(center, sr_pow_2)
					self.point_matrix[drop_position[0]][drop_position[1]][2] += self.particle_height



	def search_ava_position(self, center, sr_pow_2=0):
		'''
			search apposite for particle
		'''
		sr = self.search_radius
		if sr_pow_2 == 0:
			sr_pow_2 = sr ** 2
		center = [int(center[0]), int(center[1]), center[2]]
		center_cpy = list(center)
		dir_arr = [[0, -1], [1, 0], [0, 1], [-1,0]]
		cur_dir = int(random.random()*4)
		dir_change_mark = 0
		step_length = 0
		cur_p = [center[0], center[1]]
		center_altitude = center[2]
		min_x, max_x = center[0] - sr, center[0] + sr
		min_y, max_y = center[1] - sr, center[1] + sr
		while step_length <= self.search_radius*2:
			#direction have to change every time
			cur_dir = (cur_dir + 1) % 4
			if dir_change_mark % 2 == 0:
				step_length += 1
			for i in range(step_length):
				cur_p = vector.vector_plus(cur_p, dir_arr[cur_dir])
				if cur_p[0] < 0 or cur_p[0] >= self.width:
					continue
				if cur_p[1] < 0 or cur_p[1] >= self.length:
					continue
				if vector.vector_distance_pow_2(cur_p, [center[0], center[1]]) >= sr_pow_2:
					continue
				if self.point_matrix[cur_p[0]][cur_p[1]][2] <= center[2] - self.altitude_threshold:
					center = list(self.point_matrix[cur_p[0]][cur_p[1]])
					break

			dir_change_mark += 1
		if sum([abs(center_cpy[i] - center[i]) for i in range(3)]) < 0.003:
			return center
		else:
			center = self.search_ava_position(center)
			return center


	def ret_altitude_field(self):
		l = []
		for i in range(self.width):
			l.append([])
			for j in range(self.length):
				l[i].append(self.point_matrix[i][j][2])
		return l


	def get_vertex_buffer(self):
		l = []
		for i in range(self.width):
			for j in range(self.length):
				[l.append(k) for k in self.point_matrix[i][j]]
		self.vertex_buffer = l
		return l


	def get_index_buffer(self):
		l = []
		for i in range(self.width-1):
			for j in range(self.length-1):
				l.append(j+self.length*i)
				l.append(j+1+self.length*(i+1))
				l.append(j+self.length*(i+1))
				l.append(j+self.length*i)
				l.append(j+1+self.length*i)
				l.append(j+1+self.length*(i+1))
		self.index_buffer = l
		return l


	def get_color_buffer(self):
		max_altitude = 0
		for i in range(len(self.vertex_buffer)/3):
			if self.vertex_buffer[i * 3 + 2] > max_altitude:
				max_altitude = self.vertex_buffer[i * 3 + 2]

		for i in range(len(self.vertex_buffer)/3):
			altitude = self.vertex_buffer[i * 3 + 2]
			r = altitude / float(max_altitude) * 1.0
			b = 0.5
			g = (1 - altitude / float(max_altitude)) * 1.0
			self.color_buffer.append(r)
			self.color_buffer.append(g)
			self.color_buffer.append(b)
		return self.color_buffer


	def get_normal_buffer(self):
		'''
			calculate normal buffer
		'''
		if len(self.vertex_buffer) == 0:
			raise Exception('can only be called after get_vertex_buffer() is called')

		for i in range(self.width):
			for j in range(self.length):
				cur_p = self.point_matrix[i][j]
				p_list = []
				if i == 0 and j == 0:
					#left-bottom corner
					p_list = [
						self.point_matrix[i+1][j],
						self.point_matrix[i+1][j+1],
						self.point_matrix[i][j+1]
					]
				elif i == 0 and j == self.length - 1:
					#left-top corner
					p_list = [
						self.point_matrix[i][j-1],
						self.point_matrix[i+1][j]
					]
				elif i == self.width - 1 and j == self.length - 1:
					#right-top corner
					p_list = [
						self.point_matrix[i-1][j],
						self.point_matrix[i-1][j-1],
						self.point_matrix[i][j-1]
					]
				elif i == self.width - 1 and j == 0:
					#right-bottom corner
					p_list = [
						self.point_matrix[i][j+1],
						self.point_matrix[i-1][j]
					]
				elif i == 0:
					#left edge
					p_list = [
						self.point_matrix[i][j-1],
						self.point_matrix[i+1][j],
						self.point_matrix[i+1][j+1],
						self.point_matrix[i][j+1]
					]
				elif i == self.width - 1:
					#right edge
					p_list = [
						self.point_matrix[i][j+1],
						self.point_matrix[i-1][j],
						self.point_matrix[i-1][j-1],
						self.point_matrix[i][j-1]
					]
				elif j == 0:
					#bottom edge
					p_list = [
						self.point_matrix[i+1][j],
						self.point_matrix[i+1][j+1],
						self.point_matrix[i][j+1],
						self.point_matrix[i-1][j]
					]
				elif j == self.length - 1:
					#top edge
					p_list = [
						self.point_matrix[i-1][j],
						self.point_matrix[i-1][j-1],
						self.point_matrix[i][j-1],
						self.point_matrix[i+1][j]
					]
				else:
					#inner point
					p_list = [
						self.point_matrix[i-1][j-1],
						self.point_matrix[i][j-1],
						self.point_matrix[i+1][j],
						self.point_matrix[i+1][j+1],
						self.point_matrix[i][j+1],
						self.point_matrix[i-1][j]
					]
				#endif

				tmp_v = [vector.vector_plus(i1, vector.vector_rev(cur_p)) \
						for i1 in p_list]
				tmp_norm = [vector.cross_mutiplie3D(tmp_v[i2], tmp_v[i2+1]) \
						for i2 in range(len(tmp_v)-1)]
				normal = [0 for i3 in range(3)]
				for i4 in tmp_norm:
					normal = vector.vector_plus(normal, i4)
				normal = vector.vector_normalize(normal)
				[self.normal_buffer.append(k) for k in normal]
				#endfor
			#endfor
		#enddef

	def cal_face_normal(self):
		if len(self.index_buffer) == 0 or len(self.vertex_buffer) == 0:
			raise Exception('can only be called after get_vertex_buffer() and \
							get_index_buffer() is called')
		for i in range(len(self.index_buffer)/3):
			p1, p2, p3 = [], [], []
			vertex_offset = self.index_buffer[i*3]*3
			[p1.append(self.vertex_buffer[vertex_offset+j]) for j in range(3)]
			vertex_offset = self.index_buffer[i*3+1]*3
			[p2.append(self.vertex_buffer[vertex_offset+j]) for j in range(3)]
			vertex_offset = self.index_buffer[i*3+2]*3
			[p3.append(self.vertex_buffer[vertex_offset+j]) for j in range(3)]
			v1 = vector.vector_plus(p2, vector.vector_rev(p1))
			v2 = vector.vector_plus(p3, vector.vector_rev(p2))
			f_normal = vector.cross_mutiplie3D(v2, v1)
			self.face_normal.append(vector.vector_normalize(f_normal))


	def gen_file(self, path, obj_name):
		if path[-1] != '/':
			path += '/'
		file_handler = open(path+obj_name+'.js', 'w')
		file_handler.write('var '+obj_name+'= {\n')
		file_handler.write('vertex: [')
		[file_handler.write(str(self.vertex_buffer[i])+', ') \
			for i in range(len(self.vertex_buffer)-1)]
		file_handler.write(str(self.vertex_buffer[-1]))
		file_handler.write('],\n')
		file_handler.write('index: [')
		[file_handler.write(str(self.index_buffer[i])+', ') \
			for i in range(len(self.index_buffer)-1)]
		file_handler.write(str(self.index_buffer[-1]))
		file_handler.write('],\n')
		file_handler.write('normal: [')
		[file_handler.write(str(self.normal_buffer[i])+', ') \
			for i in range(len(self.normal_buffer)-1)]
		file_handler.write(str(self.normal_buffer[-1]))
		file_handler.write(']\n')
		file_handler.write('}')
		file_handler.close()

