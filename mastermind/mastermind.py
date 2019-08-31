#!/usr/bin/env python3

import collections
import itertools 
import random
import datetime
import pandas as pd


class Code():
	''''''

	def __init__(self, colors):
		self.code = colors

	def __str__(self):
		return str(self.code)

	def __repr__(self):
		return f'mastermind.Code({self})'

	def compare(self, other):
		'''Compare self to another code of equal length and return a 
		tuple

		Examples:
		>>> c = Code(['a', 'b', 'c', 'd'])
		>>> c.compare(Code(['a', 'b', 'd', 'e']))
		(2, 1)
		'''
		
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

	ALGORITHMS = ['random', 'minmax']

	def __init__(self, slots=4, colors=['a', 'b', 'c', 'd', 'e', 'f']):
		self.slots = slots
		self.colors = colors
		self.combinations = [
			Code(combo) for combo in itertools.product(colors, repeat=slots)
		]
		self.responses = [
			r for r in itertools.product(
				list(range(slots + 1)),
				list(range(slots + 1)),
			)
			if sum(r) <= slots
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

	def random_new_guess(self, response):
		self.save()
		self.trim(response)
		return random.choice(self.possibilities)

	def minmax_get_score(self, guess):
		return min([
			sum(1 for possibility in self.possibilities 
			if guess.compare(possibility) != r) 
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

	def new_guess(self, response, algorithm='random'):
		if algorithm == 'random':
			self.guess = self.random_new_guess(response)

		if algorithm == 'minmax':
			self.guess = self.minmax_new_guess(response)

		if len(self.possibilities) == 1:
			self.guess = self.possibilities[0]

class SelfGame(Game):
    """docstring for SelfGame"""

    def play(self, gamecount=10, algorithm='rndm'):
        '''Returns time, turns'''
        games = []
        longest_game_len = -1
        for i in range(gamecount):
            secret = random.choice(self.combinations)
            # info.loc[f'Game {i}', 'Secret'] = secret
            turns = []
            turn = 0
            while len(self.possibilities) > 1:
                start_guess = self.guess
                start_pos = self.possibilities[:]
                start_time = datetime.datetime.now()
                self.new_guess(secret.compare(start_guess), algorithm)
                end_time = datetime.datetime.now()
                end_pos = self.possibilities[:]
                turns.append([
                    end_time - start_time, # turn time
                    len(start_pos), # possibilities at turn start
                    len(end_pos), # possibilities at turn end
                ])
                turn += 1
            # reset 
            longest_game_len = max(turn, longest_game_len)
            games.append(turns)
            self.possibilities, self.guess = self.states[0] 

        # create the dataframe
        index = list(map(lambda x: f'Game {x}', range(gamecount)))
        turns = list(map(lambda x: f'Turn {x}', range(longest_game_len)))
        values = [
            'Time',
            'Start Possibilities',
            'End Possibilities',
        ]
        columns = pd.MultiIndex.from_product([turns, values])
        df = pd.DataFrame(index=index, columns=columns)
        
        # ensure timedelta missing values are NaT, not NaN
        for turn in turns:
            df.loc[:, (turn, 'Time')] = pd.to_timedelta(df.loc[:, (turn, 'Time')])
            
        # populate the dataframe
        for game_i, game in enumerate(games):
            for turn_i, turn in enumerate(game): # game is a list of turns
                df.loc[f'Game {game_i}', f'Turn {turn_i}'] = game[turn_i]
        df['Algorithm'] = algorithm
        
        return df
