Module pymastermind
===================
MasterMind simulator and guesser.

Code() -- class, stores MasterMind code
Game() -- class, MasterMind in Python with a computer guesser.

Functions
---------

    
`main()`
:   Ask if game should play itself.
    
    If yes --> guess user's code.
    If no --> play alone.

Classes
-------

`Code(*args, **kwargs)`
:   Store a MasterMind code.
    
    ### Initialization ###
    Required argument:
    code -- iterable containing the MasterMind code in raw format
    
    
    ### Methods ###
    compare(other) -- compare self to another Code object of equal length
        and return a tuple of (black_peg_count, white_peg_count)

    ### Ancestors (in MRO)

    * builtins.list

    ### Methods

    `compare(self, other)`
    :   Compare self to another Code object of equal length and return 
        a tuple of (black_peg_count, white_peg_count).
        
        -- Examples --
        >>> c = Code(['a', 'b', 'c', 'd'])
        >>> c.compare(Code(['a', 'b', 'd', 'e'])) # 2 black, 1 white
        (2, 1)

`Game(slots=4, colors=['a', 'b', 'c', 'd', 'e', 'f'])`
:   MasterMind in Python with a computer guesser.
    
    ### Initialization ###
    Keyword arguments:
    slots -- number of slots in the secret code (default 4)
    colors -- list of available colors for the secret code (default ['a', 
        'b', 'c', 'd', 'e', 'f'])
    
    ### Variables ###
    Class variables:
    ALGORITHMS -- list of available new_guess() algorithms
    
    Instance variables:
    self.slots -- number of slots in the secret code
    self.colors -- list of available colors for the secret code
    self.combinations -- list of Code objects, which contains all 
        possible secret codes
    self.responses -- list of all possible response tuples (also a list
        of all possible return values of Code().compare(Code()))
    self.possibilities -- list of all remaining possibilities for the 
        secret code
    self.guess -- Code object containing the current guess
    self.states -- list of tuples containing past values of 
        self.possibilities and self.guess
    
    ### Methods ###
    Instance methods:
    save() -- append (self.possibilities, self.guess) to self.states
    back() -- reset self.possibilities, self.guess, and self.states to
        previous values
    trim(response) -- remove possibilities from self.possibilties that
        don't match the response passed into trim()
    random_new_guess() -- set self.guess to a random choice from
        self.possibilities
    minmax_get_score(guess) -- return a score for a guess; used by 
        minmax_new_guess().
    minmax_new_guess(progress_bar) -- set self.guess to the highest 
    min-max-scoring guess
    new_guess(response, algorithm, progress_bar) -- do the following:
        1. self.trim()
        2. self.save()
        3. if only one possibility remains in self.possibilities, set 
            self.guess to that possibilities. 
            a. throw error if 0 possibilities remain
        4. run the respective algorithm for a new guess

    ### Descendants

    * pymastermind.SelfGame

    ### Methods

    `back(self)`
    :   Recover previous values for possibilities & guess.

    `minmax_get_score(self, guess)`
    :   Return the fewest number of possibilities that the guess passed 
        into minmax_get_score() could eliminate. This takes all responses in 
        self.response into account.

    `minmax_new_guess(self, progress_bar=True)`
    :   Set self.guess to the guess from self.combinations that has the
        highest min-max score. This score is calculated using the 
        minmax_get_score(guess) method.

    `new_guess(self, response, algorithm='random', progress_bar=True)`
    :   Do the following:
        1. self.trim()
        2. self.save()
        3. if only one possibility remains in self.possibilities, set 
            self.guess to that possibilities. 
            a. throw error if 0 possibilities remain
        4. run the respective algorithm for a new guess

    `random_new_guess(self)`
    :   Set self.guess to a random choice from
        self.possibilities.

    `save(self)`
    :

    `trim(self, response)`
    :   Remove possibilities from self.possibilities that don't match
        the response given.

`SelfGame(slots=4, colors=['a', 'b', 'c', 'd', 'e', 'f'])`
:   Game subclass--play self and return info about games played.
    
    ### Game vs. SelfGame ###
    Similarities: 
        - Initialization
        - All variables and methods
    Differences:
        - Added play() method
    
    ### New Method ###
    play(gamecount, algorithm) -- play {gamecount} games using the
        {algorithm} algorithm and return a pandas DataFrame with game info.

    ### Ancestors (in MRO)

    * pymastermind.Game

    ### Methods

    `play(self, gamecount=10, algorithm='random')`
    :   Play a specified number of MasterMind games with a specified
        algorithm and return a pandas DataFrame with info about: guess
        time, remaining possibilities before/after the guess.
        
        ### Calling the method ###
        Keyword arguments:
        gamecount -- play this many games (default 10).
        algorithm -- use this algorithm to find new guesses (default 
            'random'). Possibile values stored in class variable 
            ALGORITHMS SelfGame inherits from Game.
        
        ### Examples ###
        >>> # random secret code chosen for the second game
        >>> SelfGame().play().loc['Game 2', 'Secret']
        Code(['a', 'b', 'f', 'e'])
