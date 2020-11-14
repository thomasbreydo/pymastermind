# pymastermind
## Description
A Python package designed to **play**, **develop** strategies/algorithms, and **implement** the classic [MasterMind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) board game. It even includes a functioning, text-based implementation of MasterMind!

## Installation
The source code for **pymastermind** is hosted on [GitHub](https://github.com/thomasbreydo/pymastermind). You can install mastermind through PyPI, with pip:
```zsh
pip install pymastermind
```
### Requirements
**pymastermind** requires the following libraries:

- [pandas](https://github.com/pandas-dev/pandas), used by the _SelfGame_ object
- [tqdm](https://github.com/tqdm/tqdm), used to display progress bars when finding next guess. _Note: only some algorithms support progress bars. See "Algorithms" below._

## Documentation
Read the full documentation for **pymastermind** [here](https://pymastermind.readthedocs.io).

## Example Usage
### Play
Play a game against your computer, or have your computer play itself, by running `main()` and following text-based instructions.
```python3
>>> main() # initiate the game; print instructions & wait for inputs
```
### Classes
Several useful classes are defined in the **pymastermind** module.
#### Code
Code objects are list instances designed to store a MasterMind codes. You can compare two codes by using the `.compare()` method. [_What's comparing?_](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Gameplay_and_rules)
```python3
>>> secret_code = Code(['a', 'b', 'c', 'd'])
>>> guess = Code(['b', 'c', 'j', 'd'])
>>> len(secret_code) == len(guess)
True
>>> secret_code.compare(guess)
(1, 2)
```
_Note: code objects must be of the same length to comapre._
#### Game
Game objects are used to immitate gameplay.
```python3
>>> my_game = Game() # default: slots == 4, colors == ['a', 'b', 'c', 'd', 'e', 'f']
>>> secret_code = Code(['e', 'a', 'f', 'f'])
>>> my_game.guess # always the same for given setup; see Wikipedia article
['a', 'a', 'b', 'b']
>>> blacks_and_whites = secret_code.compare(my_game.guess)
>>> blacks_and_whites
(1, 0)
>>> my_game.new_guess(response, algorithm='minmax') # new guess using minmax algorithm (see below)
>>> my_game.guess
['a', 'c', 'c', 'd']
>>> my_game.back() # go back one turn
>>> my_game.guess
['a', 'a', 'b', 'b']
```
Read the [documentation](https://pymastermind.readthedocs.io/documentation) for an in-depth look at all the attributes and methods of a `Game`.
##### Algorithms
A new guess can be generated using several different algorithms. Currently, **pymastermind** has two algorithms implemented:

- _random (default algorithm)_
    - Set the guess to a random secret code possibility
    - No progress bar support yet
- _minmax_
    - Set the guess to the guess that has the highest min-max score of _all_ guesses. Read more [here](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm).
    - Supports progress bars

See the full documentation for a more detailed description of the algorithms.
#### SelfGame
SelfGame is a subclass of Game that is used to "play" games with specified algorithms and obtain a pandas [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) full of information about the games played.
```python3
>>> my_self_game = SelfGame() # same defaults, so slots == 4, colors == ['a', 'b', 'c', 'd', 'e', 'f']
>>> df = my_self_game.play() # default: games == 10, algorithm == 'random'
>>> type(df)
<class 'pandas.core.frame.DataFrame'>
>>> df.loc['Game 3', 'Turn 2'] # example query
Time                   0 days 00:00:00.000610
Start Possibilities                        23
End Possibilities                           4
Name: Game 3, dtype: object
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
