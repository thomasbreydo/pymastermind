#!/usr/bin/env python3

'''MasterMind simulator and guesser.

Code() -- class, stores MasterMind code
Game() -- class, MasterMind in Python with a computer guesser. 
'''

import collections
import itertools 
import random
import datetime
import pandas as pd


class Code():
    '''Store a MasterMind code.

    ### Initialization ###
    Required argument:
    code -- iterable containing the MasterMind code in raw format


    ### Methods ###
    compare(other) -- compare self to another Code object of equal length
        and return a tuple of (black_peg_count, white_peg_count)
    '''

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return str(self.code)

    def __repr__(self):
        return f'mastermind.Code({self})'

    def compare(self, other):
        '''Compare self to another Code object of equal length and return 
        a tuple of (black_peg_count, white_peg_count).
        
        -- Examples --
        >>> c = Code(['a', 'b', 'c', 'd'])
        >>> c.compare(Code(['a', 'b', 'd', 'e'])) # 2 black, 1 white
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
    '''MasterMind in Python with a computer guesser.

    ### Initialization ###
    Keyword arguments:
    slots -- number of slots in the secret code (default 4)
    colors -- list of available colors for the secret code (default ['a', 
        'b', 'c', 'd', 'e', 'f'])

    ### Variables ###
    Class variables:
    ALGORITHMS -- list of available new_guess() algorithms

    Instance variables:
    self.slots -- number of slots in the secret code
    self.colors -- list of available colors for the secret code
    self.combinations -- list of Code objects, which contains all 
        possible secret codes
    self.responses -- list of all possible response tuples (also a list
        of all possible return values of Code().compare(Code()))
    self.possibilities -- list of all remaining possibilities for the 
        secret code
    self.guess -- Code object containing the current guess
    self.states -- list of tuples containing past values of 
        self.possibilities and self.guess

    ### Methods ###
    Instance methods:
    save() -- append (self.possibilities, self.guess) to self.states
    back() -- reset self.possibilities, self.guess, and self.states to
        previous values
    trim(response) -- remove possibilities from self.possibilties that
        don't match the response passed into trim()
    random_new_guess(response) -- set self.guess to a random choice from
        self.possibilities
    minmax_get_score()
    '''

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
        '''Remove possibilities from self.possibilities that don't match
        the response given.
        '''
        self.possibilities = [
                possibility 
                for possibility in self.possibilities
                if self.guess.compare(possibility) == response
            ]

    def random_new_guess(self, response):
        self.save()
        self.trim(response)
        return random.choice(self.possibilities)

    def _minmax_get_score(self, guess):
        '''Return score for a guess--used by minmax_new_guess(response).'''
        return min([
            sum(1 for possibility in self.possibilities 
            if guess.compare(possibility) != r) 
            for r in self.responses
        ])

    def minmax_new_guess(self, response): 
        '''Set self.guess to highest min-max-scoring guess.'''
        self.save()
        self.trim(response)
        best = (
                self.combinations[0], 
                self._minmax_get_score(self.combinations[0])
            )
        for guess in self.combinations[1:]:
            best = max(
                best, 
                (guess, self._minmax_get_score(guess)),
                key=lambda x: x[1], # compare the scores
            )

        return best[0]

    def new_guess(self, response, algorithm='random'):
        if algorithm == 'random':
            self.guess = self.random_new_guess(response)

        elif algorithm == 'minmax':
            self.guess = self.minmax_new_guess(response)

        # <=, not == to throw error if < 1, which is caught in main
        if len(self.possibilities) <= 1: 
            self.guess = self.possibilities[0]


class SelfGame(Game):
    '''Game subclass--play self and return info about games played.

    ### Game vs. SelfGame ###
    Similarities: 
        - Initialization
        - All variables and methods
    Differences:
        - Added play() method

    ### New Method ###
    play(gamecount, algorithm) -- play {gamecount} games using the
        {algorithm} algorithm and return a pandas DataFrame with game info.
    '''

    def play(self, gamecount=10, algorithm='random'):
        '''Play a specified number of MasterMind games with a specified
        algorithm and return a pandas DataFrame with info about: guess
        time, remaining possibilities before/after the guess.

        ### Calling the method ###
        Keyword arguments:
        gamecount -- play this many games (default 10).
        algorithm -- use this algorithm to find new guesses (default 
            'random'). Possibile values stored in class variable 
            ALGORITHMS SelfGame inherits from Game.

        ### Examples ###
        >>> # random secret code chosen for the second game
        >>> SelfGame().play().loc['Game 2', 'Secret']
        Code(['a', 'b', 'f', 'e']) 
        '''
        games = []
        longest_game_len = -1
        for i in range(gamecount):
            secret = random.choice(self.combinations)
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
            games.append((turns, secret))
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
            for turn_i, turn in enumerate(game[0]): # game == (turns, secret)
                df.loc[f'Game {game_i}', f'Turn {turn_i}'] = turn
            df.loc[f'Game {game_i}', 'Secret'] = game[1]
        df['Algorithm'] = algorithm
        
        return df

