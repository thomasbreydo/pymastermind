#!/usr/bin/env python3

import mastermind

def main():
    '''
    Ask if game should play itself.

    If yes --> guess user's code.
    If no --> play alone.
    '''
    slots = 4#int(input('How many slots? '))
    colors_input = 'a,b,c,d'#input('What are the colors (separate with commas)? ')
    colors = list(map(lambda x: x.strip(), colors_input.split(',')))
    algorithm = 'random'#input(f'Algorithm ({"/".join(mastermind.Game.ALGORITHMS)})? ')
    alone = True#input('Self game (y/n)? ').lower().startswith('y')

    if not alone:
        game = mastermind.Game(slots, colors)
        print('\nWelcome to Mastermind! Press enter to go back at any time.') # change later
        
        # main loop
        while len(game.possibilities) > 1:
            print(f'\nMy guess is {game.guess}.')
            try:
                b = int(input('How many black pegs?\n> '))
                w = int(input('How many white pegs?\n> '))
            except ValueError:
                print('\n\nGoing back . . .\n\n')
                game.back()
                continue # skip trimming and just go back
            game.new_guess((b, w), algorithm)

        print(f'\n\nYour code was {game.guess}')

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
