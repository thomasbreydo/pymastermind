#!/usr/bin/env python3

import mastermind

def main():
	game = mastermind.Game()
	while len(game.possibilities) > 1:
		print(f'\nMy guess is {game.guess}.')
		b = int(input('How many black pegs?\n> '))
		w = int(input('How many white pegs?\n> '))
		game.trim((b, w), 'rndm')

	print(f'Your code was {game.guess}')

if __name__ == '__main__':
	main()
