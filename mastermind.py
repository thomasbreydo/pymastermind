#!/usr/bin/env python3

import collections
import itertools 
import random


class Code():
	'''ADD A DOCSTRING!'''
	def __init__(self, colors):
		self.code = colors

	def __str__(self):
		return str(self.code)

	def __repr__(self):
		return f'mastermind.Code({self})'

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
		
		self_not_black_counter = collections.Counter(self_not_black)
		other_not_black_counter = collections.Counter(other_not_black)

		for color, count in self_not_black_counter.items():
			# if color missing, counter[missing_color] == 0, no KeyError
			whites_count += min(count, other_not_black_counter[color])

		return blacks_count, whites_count


class Game:
	'''ADD A DOCSTRING!'''
	def __init__(self, slots=4, colors=['a', 'b', 'c', 'd', 'e', 'f']):
		self.slots = slots
		self.colors = colors
		self.combinations = [
			Code(combo) for combo in itertools.product(colors, repeat=slots)
		]
		self.possibilities = [
			Code(combo) for combo in itertools.product(colors, repeat=slots)
		]
		self.guess = Code([colors[i // 2] for i in range(slots)])
		# LATER: PLAY W/ DIFF STARTING VALUES FOR SELF.GUESS
		self.states = []

	def save(self, possibilities, guess):
		self.states.append((self.possibilities, self.guess))
		self.possibilities = possibilities
		self.guess = guess

	def back(self):
		'''Recover previous values for possibilities & guess.'''
		try:
			self.possibilities, self.guess = self.states.pop()
		except IndexError:
			pass # catch no previous state
			
	# def minmax_trim(self): 
	# 	return new_possibilities, new_guess

	def rndm_trim(self, response):
		new_possibilities = [
				self.possibilities[i] 
				for i in range(len(self.possibilities)) 
				if self.guess.compare(self.possibilities[i]) == response
			]
		new_guess = random.choice(new_possibilities)
		return new_possibilities, new_guess

	def trim(self, response, algorithm='rndm'):
		'''
		ADD DOCSTRING.

		(LONG)
		'''
		if algorithm == 'rndm':
			new_possibilities, new_guess = self.rndm_trim(response)

		if algorithm == 'minmax':
			new_possibilities, new_guess = self.minmax_trim(response)

		self.save(new_possibilities, new_guess)
