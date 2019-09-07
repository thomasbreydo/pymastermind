#!/usr/bin/env python3

'''MasterMind simulator and guesser.'''

import os
import collections
import itertools 
import random
import datetime
import pandas as pd
import tqdm.auto

ALGORITHMS = ['random', 'minmax']
DIVIDER = '\n\n----------------\n\n'
WELCOME_FILE_PATH = os.path.join(
            os.path.dirname(__file__),
            'welcome.txt'
        )


class Code(list):
    '''Store a MasterMind code.

    ### Initialization ###
    Required argument:
    code -- iterable containing the MasterMind code in raw format


    ### Methods ###
    compare(other) -- compare self to another Code object of equal length
        and return a tuple of (black_peg_count, white_peg_count)
    '''

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

        for i, peg in enumerate(self):
            if peg == other[i]:
                blacks_count += 1
            else:
                self_not_black.append(peg)
                other_not_black.append(other[i])
        
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
    random_new_guess() -- set self.guess to a random choice from
        self.possibilities
    minmax_get_score(guess) -- return a score for a guess; used by 
        minmax_new_guess().
    minmax_new_guess(progress_bar) -- set self.guess to the highest 
    min-max-scoring guess
    new_guess(response, algorithm, progress_bar) -- do the following:
        1. self.trim()
        2. self.save()
        3. if only one possibility remains in self.possibilities, set 
            self.guess to that possibilities. 
            a. throw error if 0 possibilities remain
        4. run the respective algorithm for a new guess
    '''
    
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
        first_guess = ()
        try:
            for i in range(slots):
                first_guess += (colors[i // 2],)
        except: # fill empty slots with the last element in first_guess
            first_guess += (first_guess[-1],)* (slots - len(first_guess)) 
        # 5 slots; 'a', 'b' colors; first_guess == ['a', 'a', 'b', 'b', 'b']
        self.guess = Code(first_guess) 
        self.states = []

    def save(self):
        self.states.append((self.possibilities, self.guess))

    def back(self):
        '''Recover previous values for possibilities & guess.'''
        self.possibilities, self.guess = self.states.pop()

    def trim(self, response):
        '''Remove possibilities from self.possibilities that don't match
        the response given.'''

        self.possibilities = [
                possibility 
                for possibility in self.possibilities
                if self.guess.compare(possibility) == response
            ]

    def random_new_guess(self):
        '''Set self.guess to a random choice from
        self.possibilities.'''

        return random.choice(self.possibilities)

    def minmax_get_score(self, guess):
        '''Return the fewest number of possibilities that the guess passed 
        into minmax_get_score() could eliminate. This takes all responses in 
        self.response into account.'''

        return min([
            sum(1 for possibility in self.possibilities 
            if guess.compare(possibility) != r) 
            for r in self.responses
        ])

    def minmax_new_guess(self, progress_bar=True): 
        '''Set self.guess to the guess from self.combinations that has the
        highest min-max score. This score is calculated using the 
        minmax_get_score(guess) method.'''

        best = (
                self.combinations[0], 
                self.minmax_get_score(self.combinations[0])
            )

        if progress_bar:
            for guess in tqdm.auto.tqdm(self.combinations[1:], 
                                        desc='Searching for best guess'):
                best = max(
                    best, 
                    (guess, self.minmax_get_score(guess)),
                    key=lambda x: x[1], # compare the scores (found at idx 1)
                    )

        else: # no progress bar, so no tqdm
            for guess in self.combinations[1:]:
                best = max(
                    best, 
                    (guess, self.minmax_get_score(guess)),
                    key=lambda x: x[1], # compare the scores (found at idx 1)
                    )

        return best[0]

    def new_guess(self, response, algorithm='random', progress_bar=True):
        '''Do the following:
            1. self.trim()
            2. self.save()
            3. if only one possibility remains in self.possibilities, set 
                self.guess to that possibilities. 
                a. throw error if 0 possibilities remain
            4. run the respective algorithm for a new guess
        '''

        self.save()
        self.trim(response)
        # <=, not == to throw error if < 1 i.e. 0, which is caught in main
        if len(self.possibilities) <= 1: 
            self.guess = self.possibilities[0]
        elif algorithm == 'random':
            self.guess = self.random_new_guess()
        elif algorithm == 'minmax':
            self.guess = self.minmax_new_guess(progress_bar)


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
                self.new_guess(secret.compare(start_guess), algorithm, 
                    progress_bar=False)
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
            df.loc[:, (turn, 'Time')] = pd.to_timedelta(
                df.loc[:, (turn, 'Time')]
            )
            
        # populate the dataframe
        for game_i, game in enumerate(games):
            for turn_i, turn in enumerate(game[0]): # game == (turns, secret)
                df.loc[f'Game {game_i}', f'Turn {turn_i}'] = turn
        df['Algorithm'] = algorithm
        
        return df


def main():
    '''
    Ask if game should play itself.

    If yes --> guess user's code.
    If no --> play alone.
    '''

    with open(WELCOME_FILE_PATH) as f:
        print(DIVIDER)
        print(f.read())
        print(DIVIDER)

    while True:
        try:
            slots = int(input('How many slots? '))
            break
        except:
            print('The number of slots must be an integer')
    colors_input = input('What are the colors (separate with commas)? ')
    colors = list(map(lambda x: x.strip(), colors_input.split(',')))
    while True:
        algorithm = input(
            f'Algorithm ({"/".join(ALGORITHMS)})? '
        )
        if algorithm in ALGORITHMS:
            break
        else:
            print(f'The "{algorithm} algorithm is currently unsupported')
    while True:
        alone_input = input('Self game (y/n)? ').lower()
        if alone_input == 'y':
            alone = True
            break
        elif alone_input == 'n':
            alone = False
            break

    if not alone:
        if algorithm == 'minmax': # Only for algorithms that support p-bars!
            while True:
                pbar_input = input('Progress bars (y/n)? ').lower()
                if pbar_input == 'y':
                    progress_bar = True
                    break
                elif pbar_input == 'n':
                    progress_bar = False
                    break
        else: # p-bar is not supported for chosen algorithm
            progress_bar = False

        game = Game(slots, colors)
        turn = 0
        print(DIVIDER)
        print("You've asked me guess your secret code. After each guess, "
              "I'll prompt you to enter how many black and white pegs my "
              "guess got.\n")
        print('Press <enter> or <return> at any time to go back.')
        
        # main loop
        while len(game.possibilities) > 1:
            print(f'\nMy guess is {game.guess}.')
            try:
                b = int(input('How many black pegs? '))
                w = int(input('How many white pegs? '))
            except ValueError: # non-int input, treated as <return/enter>
                try:
                    game.back()
                except IndexError: # catch error when no previous state
                    print("\n\nYou can't go back farther.\n")
                else: # no error
                    print('\n\nGoing back . . .\n')
                    turn -= 1
                continue # skip trimming and just go back
            if progress_bar:
                    print() # extra whitespace before progress bar
            try:
                game.new_guess((b, w), algorithm, progress_bar)
            except: # not enough possibilities
                print("\n\nSomething went wrong. Check your inputs. I'll try "
                      "to go back one move. To go back further, press "
                      "<enter> or <return> at any time.\n")
                try:
                    game.back()
                except IndexError:
                    pass
                continue
            turn += 1

        print(DIVIDER)
        print(f'Done! Your code was {game.guess}, and I got it after {turn} '
             f"guess{'es' if turn != 1 else ''}.")
        print(DIVIDER)

    else:
        gamecount = int(input('How many games? '))
        self_game = SelfGame(slots, colors)
        df = self_game.play(gamecount, algorithm)

        # dislpay statistics
        print(DIVIDER)
        print('-- General --')
        print(f'\nTotal games played:\n{len(df.index)}')
        print(f'\nAlgorithm used:\n{df["Algorithm"].iloc[0]}')
        print(f'\nAverage number of turns per game:\
{df.notna().sum(axis=1).mean() / 3}')
        for turn in df.columns.levels[0].drop(['Algorithm']):
            turndf = df[turn]
            eliminated = (turndf["Start Possibilities"] 
                        - turndf["End Possibilities"])
            print('\n')
            print('--', turn, '--')
            print(f'\nAverage time:\n{turndf["Time"].mean()}')
            print(f'\nAverage eliminated:\n{eliminated.mean()}')
            print(f'\nAverage percent eliminated\n:\
{100 * (eliminated / turndf["Start Possibilities"]).mean():.4}%')

if __name__ == '__main__':
    main()
