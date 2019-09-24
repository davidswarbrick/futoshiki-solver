# Futoshiki Solver

On a bored August afternoon in 2019 I attempted a selection of logic games and became stuck on a particular Futoshiki puzzle. I decided that the task of a Futoshiki (namely to order the numbers 1-5 in each row and column fulfilling the logic present) would be a reasonably simple puzzle for a computer program to solve, and that instead of figuring out the next step I should instead write a program to do the work for me. Three days, a couple of very late nights and ~500 lines of Python later I had solved the initial puzzle (both via the old-school & digital approaches), but not _every_ conceivable puzzle, at least for 5 x 5 options. I then got distracted by discovering 7 x 7 Futoshikis :sweat_smile: which kept me occupied for a while, until returning to this code to solve those too.

I'm sure there are simpler ways to go about the task, both with neater code and a cleaner algorithm, however I attempted this with no references & purely for fun.

**EDIT**: Solving Futoshikis (or any Latin Square puzzle) has been categorized as NP-complete, thus the methods I detail here are strictly for futoshiki puzzles.

## Code Structure

### Puzzle Description

The first task was to setup a logic structure for the puzzles. I decided to split the logic and number sections into separate 2D arrays (lists), and wrote a function to print the two together. For logic I used the unicode characters: < > &#8743; &#8744;.

The raw logic input is done in an easily readable way, however to use it practically one wishes to know what the logic is surrounding each square. I wrote a function to return an array of the surrounding logic for each square,  `logic_matrix`.


### Validity Checker

A quick task, but a very important one, is to check that a solved Futoshiki is valid, that is that all squares fulfil the rules defined by the logic and only contain the numbers 1-5. My validity checker `valid(puzzle, logic)` runs a logic tester on each square, but only checks the values right and below each square since it sweeps through all squares so those are the only tests necessary in this case (the function could check all 4 neighbours but that would simply waste time).

We could use this to cycle through & brute force options, but the current brute force algorithm instead uses the solving code which is setup to only result in valid options.


## Algorithm Breakdown

Initially the solver assumes any of the numbers 1-5 can go into each square, then gradually reduces the options by running through a set of algorithms. When a consistent set is found, the values are returned so a human can see what the computer "thinks" should go where. This also showed where the computer was unsure (ie there was more than one option left for a square), which highlighted when a new algorithm was needed.

### Recursive Logic Strategies

One of the key things any keen Futoshiki solver does when they see a puzzle is note down any places where there are multiple greater/less than signs in a row. If for example there's 3>\_>\_, then the only option is of course 3>2>1. A simple way of doing this is to ensure that "5" isn't an option in any location that is "less than" another, and that "1" isn't an option in any location "more than" another. My functions go a step further and examine the _possible_ values in neighbouring squares, only allowing those that make logical sense. I'm particularly proud of the recursive nature of the function, which will check if there is logic restricting neighbouring squares and re-run itself so that changes are rippled through logic-linked cells.

### Only Possible Location

A simple thing to see when looking at the list of possible values for a line or column is that a single number is only able to go in one location. I wrote a row/column agnostic checking function and wrapped it so that it will check both when given a possible value matrix and a set of indices.

### Line Match

This is a slightlier trickier strategy to code and explain. If two positions in a line have the same two possible values, then this pair of options cannot feasibly be possible values for any other place in the line. The same can be said for three positions with three matching possible values and so on, but also if the same three possible values are shared across a 2, 3, 3 (number of possible values) configuration across three positions. This logic could be extended to 3, 3, 4, 4 setups but would involve more complex checks and likely not help with narrowing down options.


### Object-oriented setup
As a task in proper Python structuring, I decided to re-write my code to be object-oriented, and thus usable as a library more easily. This restructuring led to some algorithm re-factoring, most notably that I rethought my logic recursion to run from a top-down or bottom-up approach, leading to fewer iterations required through the puzzle for a completed solution to be found. This restructuring also helped with brute-forcing, as each puzzle can now keep track of the 'level' of brute forcing which it is currently at, and thus not recurse too deeply & waste time.

### Puzzle Generation
Having a Puzzle class allowed a simple addition to create a puzzle generator, which automatically generates a random set of logic & attempts to solve it. If the program can solve a puzzle using its algorithms it returns the puzzle for a user to try. If the program cannot, it generates a new set of logic and tries again. If we create more complex solution algorithms then the generated puzzles will in turn become more complex. Since the current algorithms are ones that I think are easily understandable, the generated puzzles are not too complex. One issue at the moment is that starting to brute force puzzles from the minimum possibility cells leads to 'solvable' puzzles where some of the logic has already been used and those numbers filled in.

A very useful improvement to the current program would be in the brute forcing algorithm. Currently the algorithm 'guesses' as few numbers as possible and uses its algorithms to try and solve after that. This means that possible values are always selected from a valid list, however occasionally it also results in situations where there are no possible values for a certain cell (raising a KeyError). An improved algorithm would handle these exceptions to infer whether the last attempted value for a cell can therefore be ignored as incorrect, however currently the next value is simply attempted. Running the solution algorithms on 9x9 grids or any complex puzzles each time a new value is guessed results in slow operation which must be able to be sped up. At one point I considered whether multithreading the application might be the solution (for example brute forcing different cells in different threads) but I think changing the algorithm itself will lead to the best solution.


# ToDo
- [x] Puzzle Input
- [x] Validity Checker
- [x] Solve original target puzzle
- [x] Solve all 5 x 5 Futoshikis
- [x] Solve all higher order Futoshikis (pending brute forcing improvements)
- [x] Futoshiki problem creator
- [ ] Character Recognition for scanning in puzzles
- [ ] Phone app
- [ ] ML Attempt at same problem ?
