#!/usr/bin/env python3

import mastermind

ALL_ALLGORITHMS = mastermind.Game.ALGORITHMS

def main():
    '''
    Ask if game should play itself.

    If yes --> guess user's code.
    If no --> play alone.
    '''

    print(
'''
Welcome to MasterMind! 


-- Rules -- 

(Modified from https://en.wikipedia.org/wiki/Mastermind_(board_game))

I'm codebreaker, trying to guess your pattern, in both order and color. After 
each of my guesses, you'll be prompted to give my guess a number of black pegs  
and white pegs. 

The number of black pegs you give my guess represents the number of code pegs 
from my guess are correct in both color and position. 

The number of white pegs you give my guess represents the number of code pegs 
that are correct in color, but in the wrong position. 

If there are duplicate colors in my guess, they can't all be awarded a 
black/white peg unless they correspond to the same number of duplicate colors 
in your secret code. For example, if your hidden code is ('a', 'a', 'b', 'b') 
and I guess ('a', 'a', 'a', 'b'), you should respond with:
    * a black peg for the first 'a'
    * another black peg for the second 'a'
    * nothing for the third 'a', since there isn't a third 'a' in your code
    * another black peg for the last 'b' 
    * nothing to indicate your code has a second black


-- Copyright Info --

MIT License

Copyright (c) 2019 Thomas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

''')

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
            f'Algorithm ({"/".join(ALL_ALLGORITHMS)})? '
        )
        if algorithm in ALL_ALLGORITHMS:
            break
        else:
            print(f'The "{algorithm}"" algorithm is currently unsupported')
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

        game = mastermind.Game(slots, colors)
        turn = 0
        print(
'''

----------------

You've asked me guess your secret code. After each guess, I'll prompt you to
enter how many black and white pegs my guess got.

Press <enter> or <return> at any time to go back.
''')
        
        # main loop
        while len(game.possibilities) > 1:
            turn += 1
            print(f'\nMy guess is {game.guess}.')
            try:
                b = int(input('How many black pegs? '))
                w = int(input('How many white pegs? '))
            except ValueError: # non-int input, treated as <return/enter>
                print('\n\nGoing back . . .\n')
                game.back()
                turn -= 1
                continue # skip trimming and just go back
            try:
                if progress_bar:
                    print() # extra whitespace before progress bar
                game.new_guess((b, w), algorithm, progress_bar)
            except: # not enough possibilities
                print("\n\nSomething went wrong. Check your inputs. I'm "
                      "going back one move. To go back further, press <enter> "
                      "or <return> at any time.\n")
                turn -= 1
                game.back()
                continue

        print(f'\n\nDone! Your code was {game.guess}, and I guessed it in '
              f'{turn} moves.\n')

    else:
        gamecount = int(input('How many games? '))
        self_game = mastermind.SelfGame(slots, colors)
        df = self_game.play(gamecount, algorithm)

        # dislpay statistics
        print('\n\n-- General --')
        print(f'\nTotal games played:\n{len(df.index)}')
        print(f'\nAlgorithm used:\n{df["Algorithm"].iloc[0]}')
        print(f'\nAverage number of turns per game:\
{df.notna().sum(axis=1).mean() / 3}')
        for turn in df.columns.levels[0].drop(['Algorithm', 'Secret']):
            turndf = df[turn]
            eliminated = (turndf["Start Possibilities"] 
                        - turndf["End Possibilities"])
            print('\n')
            print('--', turn, '--')
            print(f'\nAverage time:\n{turndf["Time"].mean()}')
            print(f'\nAverage eliminated:\n{eliminated.mean()}')
            print(f'\nAverage percent eliminated:\
{100 * (eliminated / turndf["Start Possibilities"]).mean():.4}%')

if __name__ == '__main__':
    main()
