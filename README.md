# pymastermind
## Description
**pymastermind** is a package designed to make it easy to emulate the [MasterMind Game](https://en.wikipedia.org/wiki/Mastermind_(board_game)) in Python code. It also includes a functioning, text-based implementation of MasterMind! This lets you play games against your computer or even have your computer play itself. 

## Installation
The source code for **pymastermind** is hosted here, at https://github.com/thomasbreydo/pymastermind. You can install matermind through PyPI, with pip:
```zsh
pip install pymastermind
```
```zsh
# or, use the pip3 command if you need to use the python3 command to start Python 3.X
pip3 install pymastermind
```
### Requirements
**pymastermind** requires the following libraries:
- [pandas](https://github.com/pandas-dev/pandas), used by the _SelfGame_ object
- [tqdm](https://github.com/tqdm/tqdm), used to display progress bars when finding next guess. _Note: only some algorithms support progress bars. See "WHEREVER I DISCUSS ALGORITHMS"_

## Example Usage
### Play
Play a game against your computer, or have your computer play itself, by running ```pymastermind.main()``` and following text-based instructions.
```python3
import pymastermind as pmm

pmm.main()
```
### Using Definitions
Several useful classes are defined in the **pymastermind** module.
#### Code
Code objects are list instances designed to store a MasterMind codes. You can compare two codes by using the ```.compare()``` method. [_What's comparing?_](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Gameplay_and_rules)
```python3
>>> import pymastermind as pmm
>>> secret_code = pmm.Code(['a', 'b', 'c', 'd'])
>>> guess = pmm.Code(['b', 'c', 'j', 'd'])
>>> len(secret_code) == len(guess)
True
>>> secret_code.compare(guess)
(1, 2)
```
_Note: code objects must be of the same length to comapre._
#### Game
Game objects are used to immitate gameplay.
```python3
>>> import pymastermind as pmm
>>> my_game = pmm.Game() # default: slots == 4, colors == ['a', 'b', 'c', 'd', 'e', 'f']
>>> secret_code = pmm.Code(['e', 'a', 'f', 'f'])
>>> my_game.guess # always the same for given setup; see Wikipedia article
['a', 'a', 'b', 'b']
>>> blacks_and_whites = secret_code.compare(my_game.guess)
>>> blacks_and_whites
(1, 0)
>>> my_game.new_guess(response, algorithm='minmax')
>>> my_game.guess
['a', 'c', 'c', 'd'] # CONTINUE FROM HERE
>>> my_game.back()
```
Read the documentation for an in-depth look at all the attributes and methods of a ```pymastermind.Game```.
## License
[MIT](https://choosealicense.com/licenses/mit/)
