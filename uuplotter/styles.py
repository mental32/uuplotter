##
# -*- coding: utf-8 -*-
##
import itertools
from collections import deque

from .plotter import Box

_topleft = '╔'
_topright = '╗'
_bottomleft = '╚'
_bottomright = '╝'
_horizontal = '═'
_vertical = '║'
_vertical_right = '╠'
_vertical_left = '╣'
_horizontal_down = '╦'
_horizontal_up = '╩'


def splice_strings(*strings):
	return '\n'.join(''.join(pair) for pair in zip(*[s.split('\n') for s in strings]))


def linear_right_leaning(datapoint) -> str:
	def make_top(hostname) -> str:
		est = Box.estimate(hostname)
		lst = list(_horizontal * (est - 2))
		lst[len(lst)//2] = _horizontal_up
		return ''.join(lst)

	center = Box(datapoint.name, datapoint.connections)
	if center.connections:
		center.right_connector = _vertical_right
		connections = [Box(conn).modify(top_connector=make_top(conn)).string() for conn in center.connections]
		last_index = len(center.connections) - 1
		for index, connection in enumerate(center.connections):
			lst = list(_horizontal * Box.estimate(connection))
			if index == last_index:
				lst[len(lst) // 2] = _topright
				lst = lst[:lst.index(_topright) + 1]
			else:
				lst[len(lst) // 2] = _horizontal_down

			center.raw_str[1] += ''.join(lst)
			center.raw_str[2] += ''.join(''.join(lst).replace('═', ' ').replace('╦', '║').replace('╗', '║'))

	displacement = ' ' * (Box.estimate(datapoint.name))
	connections[0] = '\n'.join(displacement + line for line in connections[0].split('\n'))
	center.raw_str.append(splice_strings(*connections))
	return center.string()

def linear_left_leaning(center) -> str:
	def make_line(d, cs):
		lst = list(_horizontal * d)
		total = 0
		for i, c in enumerate(cs):
			if i == 0:
				lst[Box.estimate(c) // 2] = _topleft
			else:
				lst[total + (Box.estimate(c) // 2)] = _horizontal_down
			total += Box.estimate(c)

		lst[:lst.index(_topleft)] = ' ' * lst.index(_topleft)

		return ''.join(lst)

	def make_top(hostname) -> str:
		est = Box.estimate(hostname)
		lst = list(_horizontal * (est - 2))
		lst[len(lst)//2] = _horizontal_up
		return ''.join(lst)

	center.modify(left_connector=_vertical_left)

	if center.connections:
		displacement = sum([Box.estimate(c) for c in center.connections])
		q = ' ' * displacement
		center.attach(side='left', seq=[q, make_line(displacement, center.connections), make_line(displacement, center.connections).replace(_horizontal, ' ').replace(_topleft, _vertical).replace(_horizontal_down, _vertical)])

		center.raw_str.append(splice_strings(*(Box(c).modify(top_connector=make_top(c)).string() for c in center.connections)))

	return center.string()

def linear_trail(datapoint) -> str:
	def right_if_middle(nt, nntt) -> str:
		n, t = nt
		nn, tt = nntt

		if int(nn) == int(tt) - 1:
			if int(n) == t // 2:
				return _bottomleft
			elif int(n) != t - 1:
				return _vertical
			else:
				return ' '
		else:
			if int(n) == t // 2:
				return _vertical_right
			else:
				return _vertical

	center = Box(datapoint.name, datapoint.connections)
	if center.connections:
		connections = [Box(conn).modify(left_connector=_vertical_left).string() for conn in center.connections]
		for n, conn in enumerate(connections.copy()):
			connections[n] = '\n'.join(' ' * (Box.estimate(datapoint.name) + 1) + right_if_middle((index, len(conn.split('\n'))), (n, len(connections))) + string for index, string in enumerate(conn.split('\n')))

		center.right_connector = _vertical_right
		center.raw_str[1] += _horizontal + _topright
		center.raw_str[2] += ' ' + _vertical
		center.raw_str += connections

	return center.string()

def spider(datapoint) -> str:
	def add_left(item, container):
		return '{0}{1}'.format(item, container)

	def even_array(one, two, appendright=False):
		four = [one, two]
		if len(one) != len(two):
			_three = deque(min((one, two), key=len))
			_three.appendleft(' ') if not appendright else _three.append(' ')
			four[four.index(min((one, two), key=len))] = list(_three)
		return four

	center = Box(datapoint.name, datapoint.connections).modify(left_connector='╣', right_connector='╠')
	if center.connections:
		if len(center.connections) < 4:
			if len(center.connections) <= 2:
				center.modify(right_connector='║')

			if len(center.connections) == 1:
				return splice_strings(center.modify(right_connector='╠', left_connector='║').string(), Box(center.connections[0]).modify(left_connector='╣').string())

			base_displacement = max([Box.estimate(n) for n in [c for c in center.connections]])

			center.raw_str[0] = add_left(' ' * base_displacement + ' ║ ', center.raw_str[0])
			center.raw_str[1] = add_left(' ' * base_displacement + ' ╠═', center.raw_str[1]) + ('═╗' if len(center.connections) == 3 else '')
			center.raw_str[2] = add_left(' ' * base_displacement + ' ║ ', center.raw_str[2]) + (' ║' if len(center.connections) == 3 else '')

			branches = [[], [], [], []]
			fixed_indexes = [0, 1, 3]
			for i, c in enumerate(center.connections):
				branches[fixed_indexes[i]] = [c]
		else:
			base_displacement = max([Box.estimate(n) for n in [c for c in center.connections[::2]]])

			center.raw_str[0] = add_left(' ' * base_displacement + ' ║ ', center.raw_str[0]) + ' ║'
			center.raw_str[1] = add_left(' ' * base_displacement + ' ╠═', center.raw_str[1]) + '═╣'
			center.raw_str[2] = add_left(' ' * base_displacement + ' ║ ', center.raw_str[2]) + ' ║'

			l, r = [c for c in center.connections[::2]], [c for c in center.connections[1::2]]
			branches = [l[:len(l) // 2], l[len(l) // 2:], r[:len(r) // 2], r[len(r) // 2:]]

		center_displacement = Box.estimate(datapoint.name) + 2

		rc = lambda i: (_vertical_left if i in (2, 3) else _vertical)
		lc = lambda i: (_vertical_right if i in (0, 1) else _vertical)
		max_q = len(max(center.connections, key=len))
		for index, branch in enumerate(branches.copy()):
			for number, connection in enumerate(branch):
				_element = Box(connection).modify(left_connector=rc(index), right_connector=lc(index))
				if index in (2, 3):
					space = ' ' * center_displacement

					if index == 2:
						pipe = add_left(space + ('╔═' if connection == branch[-1] else '╠═'), _element.raw_str[1])
						end = add_left(space + ('  ' if connection == branch[-1] else '║ '), _element.raw_str[0])
					else:
						pipe = add_left(space + ('╚═' if connection == branch[-1] else '╠═'), _element.raw_str[1])
						end = add_left(space + ('  ' if connection == branch[-1] else '║ '), _element.raw_str[2])

					addons = ([add_left(space + '║ ', _element.raw_str[0]), pipe, end] if index == 3 else [end, pipe, add_left(space + '║ ', _element.raw_str[2])])
				else:
					end = ('  ' if connection == branch[-1] else ' ║')
					sexpand = ' ' * (max_q - len(connection)) 
					expand = _horizontal * (max_q - len(connection) + 1) 
					pipe = ((expand+'╗' if connection == branch[-1] else expand+'╣') if index in (0, 2) else (expand+'╝' if connection == branch[-1] else expand+'╣'))
					addons = ([sexpand + end, pipe, sexpand + ' ║'] if index in (0, 2) else [sexpand + ' ║', pipe, end + sexpand])

				for n, i in enumerate(addons):
					if index in (2, 3):
						_element.raw_str[n] = i
					else:
						_element.raw_str[n] += i
				else:
					branches[index][number] = _element.string()
		else:
			top = []
			bottom = []

			branches[0], branches[2] = even_array(list(reversed(branches[0])), list(reversed(branches[2])))
			branches[1], branches[3] = even_array(branches[1], branches[3], appendright=True)

			for left, right in itertools.zip_longest((branches[0]), (branches[2]), fillvalue=' '):
				if ' ' not in (left, right):
					top.append(splice_strings(left, right))
				else:
					_tmp = [left, right]
					_tmp[_tmp.index(' ')] = _vertical
					top.append(_tmp[0])

			for left, right in itertools.zip_longest(branches[1], branches[3], fillvalue=' '):
				if ' ' not in (left, right):
					bottom.append(splice_strings(left, right))
				else:
					_tmp = [left, right]
					_tmp.remove(' ')
					bottom.append(_tmp[0])
			else:
				center.raw_str = top + center.raw_str + bottom
	else:
		center.modify(left_connector=_vertical, right_connector=_vertical)

	return center.string()
