# mastermind
## Description
**mastermind** is a package designed to make it easy to emulate the [MasterMind Game](https://en.wikipedia.org/wiki/Mastermind_(board_game)) in Python code. It also includes a functioning, text-based implementation of MasterMind! This lets you play games against your computer or even have your computer play itself. 

## Installation
The source code for **mastermind** is hosted here, at https://github.com/thomasbreydo/mastermind. You can install matermind through PyPI, with pip:
```zsh
pip install mastermind
```
```zsh
# or, use the pip3 command if you need to use the python3 command to start Python 3.X
pip3 install mastermind
```
### Requirements
**mastermind** requires the following libraries:
- [pandas](https://github.com/pandas-dev/pandas), used by the _SelfGame_ object
- [tqdm](https://github.com/tqdm/tqdm), used to display progress bars when finding next guess. _Note: only some algorithms support progress bars. See "WHEREVER I DISCUSS ALGORITHMS"_

## Example Usage
### Play
Play a game against your computer, or have your computer play itself, by running ```mastermind.main()``` and following text-based instructions.
```python3
import mastermind as mm

mm.main()
```
### Using Definitions
Several useful classes are defined in the **mastermind** module
### Code objects
Code objects are list instances designed to store a MasterMind codes. You can compare two codes by using the ```.compare()``` method. [_What's comparing?_](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Gameplay_and_rules)
```python3
>>> import mastermind as mm
>>> secret_code = mm.Code(['a', 'b', 'c', 'd'])
>>> guess = mm.Code(['b', 'c', 'j', 'd'])
>>> len(secret_code) == len(guess)
True
>>> secret_code.compare(guess)
(1, 2)
```
_Note: code objects must be of the same length to comapre._
## License
[MIT](https://choosealicense.com/licenses/mit/)
