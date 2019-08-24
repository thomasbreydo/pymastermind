#!/usr/bin/env python3

import mastermind

def main():
	game = mastermind.Game(5, 'a b c d e f g h i j k l'.split())
	while len(game.possibilities) > 1:
		print(f'\nMy guess is {game.guess}.')
		b = int(input('How many black pegs?\n> '))
		w = int(input('How many white pegs?\n> '))
		game.trim((b, w), 'rndm')
		print(f'DEBUG:root: remaining possibilities: {len(game.possibilities)}')

	ADD BACK FUNCTIONALITY

	print(f'Your code was {game.guess}')

if __name__ == '__main__':
	main()
