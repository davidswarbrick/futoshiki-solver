from random import randint, randrange, random
from Futoshiki import FutoshikiPuzzle

rand_puzzle = FutoshikiPuzzle.empty_array_returner(5, 5, 'range')


class FutoshikiGenerator(FutoshikiPuzzle):
    @staticmethod
    def generate_logic(size, threshold=0.1):
        logic = []
        for j in range(2*size - 1):
            line = []
            # if j is odd then it's an up or down line
            if (j+1) % 2 == 0:  # j odd
                for i in range(size):
                    a = random()
                    if a >= threshold and a <= 1 - threshold:
                        line.append('')
                    elif a < threshold:
                        line.append(u"\u2228")
                    elif a > 1 - threshold:
                        line.append(u"\u2227")
            else:  # Even line
                for i in range(size - 1):
                    a = random()
                    if a >= threshold and a <= 1 - threshold:
                        line.append('')
                    elif a < threshold:
                        line.append('<')
                    elif a > 1 - threshold:
                        line.append('>')
            logic.append(line)
        return logic

<<<<<<< HEAD
    def generate_numbers(self, max_brute_force_level=2):
        try:
            self.solve()
        except KeyError:
            # Happens when there are zero possibilities for a square:
            self.generated_logic = self.generate_logic(self.size)
            self.generate_numbers()
        if self.solved:
            # Humans would be able to solve this without any pre-given numbers
            print("Humans can solve this puzzle without numbers:")
            print(self.puzzle_printer(self.solvable_puzzle_numbers, self.puzzle_logic))
        else:
            self.brute_force(max_brute_force_level)
            if self.solved:
                print("Found a set of numbers the computer could solve:")
                print(self.puzzle_printer(self.solvable_puzzle_numbers, self.puzzle_logic))
            else:
                # Not solved after 3 levels of brute force, just find a new puzzle, don't waste time
                self.generated_logic = self.generate_logic(self.size)
                self.generate_numbers()

    def __init__(self, size, threshold=None):
        self.size = size
        self.generated_logic = self.generate_logic(size)
        super().__init__(FutoshikiPuzzle.empty_array_returner(size, 1, 0), self.generated_logic)
=======
    def generate_numbers(self):
        for j in range(self.size):
            for i in range(self.size):
                self.puzzle = self.possible_values[j][i][randrange(
                    0, len(self.possible_values[j][i]))]
                self._solution_update()

    def __init__(self, size):
        self.size = size
        self.generated_logic = self.generate_logic(size)
        self.initial_puzzle = FutoshikiPuzzle.empty_array_returner(size, 1, 0)
        super().__init__(self.initial_puzzle, self.generated_logic)
>>>>>>> generator


# l = FutoshikiGenerator.generate_logic(5, 0.1)
# p = FutoshikiPuzzle.empty_array_returner(5, 1, 0)
# # FutoshikiPuzzle.puzzle_printer(p, l)
# fp = FutoshikiPuzzle(p, l)
fp = FutoshikiGenerator(5)
<<<<<<< HEAD
fp.generate_numbers(1)

# large_fp = FutoshikiGenerator(9, 0.5)
# large_fp.generate_numbers()
# all_solved = True
# while all_solved:
#     fp = FutoshikiGenerator(5)
#     fp.generate_numbers()
#     all_solved = fp.solved
# if not fp.solved:
#     print("Unable to solve puzzle:")
#     print(fp)
=======
# print(p)
fp.solve()
fp.brute_force()
>>>>>>> generator
