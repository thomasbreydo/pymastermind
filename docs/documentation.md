# pymastermind
A Python package designed to **play**, **develop** strategies/algorithms, and **implement** the classic [MasterMind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) board game. It even includes a functioning, text-based implementation of MasterMind!

## Functions
### Main: `main()`
Play MasterMind from your console.

## Classes

### Code: `Code(*args, **kwargs)`
A subclass of the Python `list`, used to store a MasterMind code.
##### Ancestors (in MRO)

- builtins.list
    - Changes:
        - None
  - Additions:
      - `compare(self, other)`
##### Initialization
Initialize a `Code` object like a Python `list`.
```python3
>>> c = Code(['red', 'red', 'blue'])
```
##### New Methods
###### New Instance Methods

**`compare(self, other)`** -- Compare `self` to another `Code` object of equal length and return a tuple of `(n_blacks, n_whites)`.

##### Example Usage
```python3
>>> my_code = Code(['a', 'b', 'c', 'd'])
>>> my_code[3]
'd'
>>> my_code.compare(Code(['a', 'b', 'd', 'e'])) # 2 black, 1 white
(2, 1)  
```
### Game: `Game(slots=4, colors=['a', 'b', 'c', 'd', 'e', 'f'])`
MasterMind in Python with algorithms to guess the secret code.
    
##### Initialization 
```python3
>>> g = Game(3, ['red', 'yellow', 'blue', 'white'])
>>> g.slots
3
>>> g.colors
['red', 'yellow', 'blue', 'white']
```
###### Keyword arguments
**`slots`** -- Number of slots in the secret code (default: `4`).

**`colors`** -- List of available colors for the secret code (default: `['a', 'b', 'c', 'd', 'e', 'f']`).

##### Variables
###### Class variables
**`ALGORITHMS`** -- List of available algorithms for `new_guess()`.
###### Instance variables
**`self.slots`** -- Number of slots in the secret code.

**`self.colors`** -- List of available colors for the secret code.

**`self.combinations`** -- List of `Code` objects, which contains all possible secret codes.

**`self.responses`** -- List containing all valid response tuples, `(n_blacks, n_whites)`.

**`self.possibilities`** -- List of all remaining possibilities for the secret code.

**`self.guess`** -- `Code` object containing the current guess.

**`self.states`** -- List of tuples containing past values of `self.possibilities` and `self.guess`.


##### Methods 
###### Instance methods
**`save(self)`** -- Append `(self.possibilities, self.guess)` to `self.states`.

**`back(self)`** -- Reset `self.possibilities`, `self.guess`, and `self.states` to previous values.

**`trim(self, response)`** -- Remove possibilities from `self.possibilties` that don't match the tuple `response`, which contains the number of black and white pegs the current `self.guess` got.

**`random_new_guess(self)`** -- Set `self.guess` to a random choice from `self.possibilities`.

**`minmax_get_score(self, guess)`** -- Return the [min-max score](https://en.wikipedia.org/wiki/Mastermind_%28board_game%29#Five-guess_algorithm) for the `Code` object `guess`.

**`minmax_new_guess(self, progress_bar=True)`** -- Set `self.guess` to the highest min-max-scoring guess. If `progress_bar` is set to `True`, `minmax_new_guess` displays a progress bar as it iterates through all possible guesses. 

**`new_guess(self, response, algorithm='random', progress_bar=True)`** -- Run `self.trim(reponse)`, `self.save()`, then:

- If only one possibility for the secret code remains, assign it to `self.guess`.
- Otherwise, run the correct guess algorithm (default: `'random'`).

##### Descendants

* `pymastermind.SelfGame`

### Self Game: `SelfGame(slots=4, colors=['a', 'b', 'c', 'd', 'e', 'f'])`
Play MasterMind without player input and return info about the games played.
##### Ancestors (in MRO)

- `pymastermind.Game`
    - Changes: 
        - None
    - Additions:
         - `play(self)`
##### Initialization
Treat a `SelfGame` object like a `Game`.
```python3
>>> self_game = SelfGame(3, ['red', 'yellow', 'blue', 'white'])
>>> self_game.slots
3
>>> self_game.colors
['red', 'yellow', 'blue', 'white']
```
##### New Methods
###### New Instance Methods
**`play(self, gamecount=10, algorithm='random')`** -- Play a `gamecount` number of MasterMind games with the `algorithm` algorithm and return a pandas DataFrame with info about: guess time and remaining possibilities before/after the guess.
##### Example Usage
```python3
>>> self_game = SelfGame()
>>> df = self_game.play()
>>> type(df)
<class 'pandas.core.frame.DataFrame'>
>>> df.loc['Game 2', 'Turn 1']
Time                   0 days 00:00:00.000610
Start Possibilities                        23
End Possibilities                           4
>>> df.loc['Game 5', 'Turn 3'] # Game 5 ended before Turn 3, but another didn't
Time                   NaT
Start Possibilities    NaN
End Possibilities      NaN
```

## Algorithms
**pymastermind** currently supports two algorithms to use for generating a new guess, **random** and **min-max**. 

_Note: all algorithms can be accessed using the `new_guess` method, which automatically trims and saves._
```python3
>>> g.new_guess(response, algorithm_code) # preferred over g.minmax_new_guess(reponse)
```
### Random: `random_new_guess(self, response)`
The **random** algorithm sets `self.guess` to a random choice from `self.possibilities`. 
##### Algorithm Code
The algorithm code for the **random** algorithm is `'random'`.

### Min-Max: `minmax_new_guess(self, response, progress_bar=True)`
The **min-max** algorithm consists of two steps:

1. Assign a score to each combination from `self.combinations` by counting how many possibilities that combination, if used as the next guess, would _always_ eliminate, no matter which response it gets.
2. Set `self.guess` to the highest-scoring combination from step 1.

##### Algorithm Code
The algorithm code for the **min-max** algorithm is `'minmax'`.

### All Algorithm Codes
Below is a list of supported algorithms and their algorithm code. The algorithm code is needed to run `new_guess` with a specific algorithm.

- Random: `'random'`
- Min-Max: `'minmax'`