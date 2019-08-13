# Futoshiki Solver

On a bored August afternoon in 2019 I attempted the logic games in the Times, and became stuck on a particular Futoshiki puzzle. I decided that the task of a Futoshiki (namely to order the numbers 1-5 in each row and column fulfilling the logic present) would be a reasonably simple puzzle for a computer programme to solve, and that instead of figuring out the next step I should instead write a program to do the work for me. Three days, a couple of very late nights and ~500 lines of Python later I had solved the inital puzzle (both via the old-school & digital approaches), but not **every** conceivable puzzle, at least for 5 x 5 options. I then got distracted by discovering 7 x 7 Futoshikis :sweat_smile: which kept me occupied until re-opening my A&R Cambridge A60 for some repairs (another article to come soon on those).

I'm sure there are simpler ways to go about the task, both with neater code and a cleaner algorithm, however I attempted this with no references & purely for fun.

## Code Structure

### Puzzle Description

The first task was to setup a logic structure for the puzzles. I decided to split the logic and number sections into separate 2D arrays (lists), and wrote a function to print the two together. For logic I used the unicode characters: < > &#2227; &#2228;.

The raw logic input is done in an easily readable way, however to use it practically one wishes to know what the logic is surrounding each square. I wrote a function to return an array of the surrounding logic for each square,  `logic_matrix`.


### Validity Checker

A quick task, but a very important one, is to check that a solved Futoshiki is valid, that is that all squares fulfil the rules defined by the logic and only contain the numbers 1-5. My validity checker `valid(puzzle, logic)` runs a logic tester on each square, but only checks the values right and below each square since it sweeps through all squares so those are the only tests necessary in this case (the function could check all 4 neighbours but that would simply waste time).

We could use this to cycle through & brute force options, but I tried as much as possible to avoid this as it's far less fun.


## Algorithm Breakdown

Now onto actually solving the puzzles! Initially the solver assumes any of the numbers 1-5 can go into each square, then gradually reduces the options by running through a set of algorithms. When a consistent set is found, the values are returned so a human can see what the computer "thinks" should go where. This also showed where the computer was unsure (ie there was more than one option left for a square), which highlighted when a new algorithm was needed.

### Recursive Logic Strategies

One of the key things any keen Futoshiki solver (such as myself and my Dad) does when they see a puzzle is note down any places where there are multiple greater/less than signs in a row. If for example there's 3>\_>\_, then the only option is of course 3>2>1. A simple way of doing this is to ensure that "5" isn't an option in any location that is "less than" another, and that "1" isn't an option in any location "more than" another. My functions go a step further and examine the **possible** values in neighbouring squares, only allowing those that make logical sense. I'm particularly proud of the recursive nature of the function, which will check neighbouring squares if there's a change in the current square, but ideally it would ripple changes through & re-run itself. At the moment running the solver code multiple times is a quick fix for this.

### Only Possible Location

A simple thing to see when looking at the list of possible values for a line or column is that a single number is only able to go in one location. I wrote a row/column agnostic checking function and wrapped it so that it will check both when given a possible value matrix and a set of indices.

### Line Match

This is a slightlier trickier strategy to code and explain. If two positions in a line have the same two possible values, then this pair of options cannot feasibly be possible values for any other place in the line. The same can be said for three positions with three matching possible values and so on, but also if the same three possible values are shared across a 2, 3, 3 (number of possible values) configuration across three positions. This logic could be extended to 3, 3, 4, 4 setups but would involve more complex checks and likely not help with narrowing down options.

# ToDo
- [x] Puzzle Input
- [x] Validity Checker
- [x] Solve original target puzzle
- [ ] Solve all 5 x 5 Futoshikis
- [ ] Solve all higher order Futoshikis
- [ ] Character Recognition for scanning in puzzles
- [ ] Phone app
- [ ] ML Attempt at same problem ?
- [ ] Futoshiki problem creator ?
- [ ] Become Futoshiki God
