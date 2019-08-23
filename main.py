#!/usr/bin/env python3

import mastermind

def main():
	secret_code = mastermind.Code(*'b a c c'.split())
	guess = mastermind.Code(*'a b c b'.split())

	print(secret_code.compare(guess))


if __name__ == '__main__':
	main()