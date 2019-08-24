#!/usr/bin/env python3

import mastermind
import timeit

def main():
	game = mastermind.Game()
	while len(game.possibilities) > 1:
		print(f'\nMy guess is {game.guess}.')
		b = int(input('How many black pegs?\n> '))
		w = int(input('How many white pegs?\n> '))
		game.trim((b, w))
		game.new_guess('minmax')

	print(f'\n\nYour code was {game.guess}')

if __name__ == '__main__':
	main()
