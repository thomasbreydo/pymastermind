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

		for i, peg in enumerate(self.code):
			if peg == other.code[i]:
				blacks_count += 1
			else:
				self_not_black.append(peg)
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
		self.responses = [
			r for r in itertools.product(list(range(slots + 1)), list(range(slots + 1))) if sum(r) <= slots
		]
		self.possibilities = [
			Code(combo) for combo in itertools.product(colors, repeat=slots)
		]
		self.guess = Code(tuple(colors[i // 2] for i in range(slots)))
		# LATER: PLAY W/ DIFF STARTING VALUES FOR SELF.GUESS
		self.states = []

	def save(self):
		self.states.append((self.possibilities, self.guess))

	def back(self):
		'''Recover previous values for possibilities & guess.'''
		try:
			self.possibilities, self.guess = self.states.pop()
		except IndexError:
			pass # catch no previous state

	def trim(self, response):
		self.possibilities = [
				possibility 
				for possibility in self.possibilities
				if self.guess.compare(possibility) == response
			]

	def rndm_new_guess(self, response):
		self.save()
		self.trim(response)
		return random.choice(self.possibilities)

	def minmax_get_score(self, guess):
		return min([
			sum(1 for possibility in self.possibilities if guess.compare(possibility) != r) 
			for r in self.responses
		])

	def minmax_new_guess(self, response): 
		self.save()
		self.trim(response)
		best = (
				self.combinations[0], 
				self.minmax_get_score(self.combinations[0])
			)
		for guess in self.combinations[1:]:
			best = max(
				best, 
				(guess, self.minmax_get_score(guess)),
				key=lambda x: x[1], # compare the scores
			)

		return best[0]

	def new_guess(self, response, algorithm='rndm'):
		if algorithm == 'rndm':
			self.guess = self.rndm_new_guess(response)

		if algorithm == 'minmax':
			self.guess = self.minmax_new_guess(response)

		if len(self.possibilities) == 1:
			self.guess = self.possibilities[0]
