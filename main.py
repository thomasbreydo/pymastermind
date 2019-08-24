#!/usr/bin/env python3

import mastermind

def main():
	game = mastermind.Game()
	print('Welcome to Mastermind! Press enter to go back at any time.') # change later
	
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
		game.new_guess((b, w), 'minmax')

	print(f'\n\nYour code was {game.guess}')

if __name__ == '__main__':
	main()
