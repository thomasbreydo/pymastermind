#!/usr/bin/env python3

from collections import Counter


class Code():
	'''ADD A DOCSTRING!'''
	def __init__(self, *colors):
		self.code = [c for c in colors]

	def __repr__(self):
		return str(self.code)

	def __len__(self):
		return len(self.code)

	def compare(self, other):
		'''Compares self to another code. Returns (black, white)'''

		# get blacks, then whites
		
		blacks_count = 0
		whites_count = 0
		self_not_black = []
		other_not_black = []

		for i in range(len(self)):
			if self.code[i] == other.code[i]:
				blacks_count += 1
			else:
				self_not_black.append(self.code[i])
				other_not_black.append(other.code[i])
		
		self_not_black_counter = Counter(self_not_black)
		other_not_black_counter = Counter(other_not_black)

		for color, count in self_not_black_counter.items():
			# if color missing, counter[missing_color] == 0, no KeyError
			whites_count += min(count, other_not_black_counter[color])

		return blacks_count, whites_count

			# sum(1 for )
