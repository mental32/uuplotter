##
# -*- coding: utf-8 -*-
##
from . import styles


class Box:
	@classmethod
	def estimate(cls, hostname) -> int:
		return len(hostname) + 4

	def __init__(self, name, connections=[], sorted_connections=True):
		self.raw_str = ['╔{0}╗', '{1} {2} {3}', '╚{4}╝']
		self.connections = (sorted(connections) if sorted_connections else connections)
		self.name = name

		self.left_connector = '║'
		self.right_connector = '║'
		
		self.top_connector = '═' * (len(self.name) + 2)
		self.bottom_connector = '═' * (len(self.name) + 2)

	def __repr__(self):
		return 'Box(name={0}, connections={1})'.format(self.name, len(self.connections))

	def pad_left(self, item):
		for i, c in enumerate(self.raw_str.copy()):
			self.raw_str[i] = item + c

	def attach(self, side, seq):
		if side == 'left':
			for s, rs in zip(seq, enumerate(self.raw_str.copy())):
				self.raw_str[rs[0]] = s + self.raw_str[rs[0]]
		elif side == 'right':
			for s, rs in zip(seq, enumerate(self.raw_str.copy())):
				self.raw_str[rs[0]] = self.raw_str[rs[0]] + s
		else:
			raise Exception

	def modify(self, **kwargs):
		for key, value in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, value)
		else:
			return self

	def string(self) -> str:
		return ('\n'.join(self.raw_str).format(self.top_connector, self.left_connector, self.name, self.right_connector, self.bottom_connector))


class Plotter:
	def __init__(self, datapoints):
		self.datapoints = datapoints

		# select middle datapoint as the target
		self.target = tuple(datapoints)[len(datapoints) // 2]

	def __repr__(self):
		return 'Plotter(datapoints={0})'.format(len(self.datapoints))

	def reinit(self, datapoints):
		self.datapoints = datapoints

		# select middle datapoint as the target
		self.target = tuple(datapoints)[len(datapoints) // 2]

	def center(self, key):
		try:
			index = tuple(self.datapoints).index(key)
		except ValueError:
			raise KeyError

		self.target = tuple(self.datapoints)[index]

	def format(self, style='linear_right_leaning'):
		return getattr(styles, style)(Box(self.target, self.datapoints[self.target]))

	def print(self, style='linear_right_leaning'):
		print(self.format(style=style))
