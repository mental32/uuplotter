##
# -*- coding: utf-8 -*-
##
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
