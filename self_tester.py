#!/usr/bin/env python3

import mastermind
import datetime
import random
import pandas as pd

class SelfGame(mastermind.Game):
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
