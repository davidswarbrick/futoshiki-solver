from copy import deepcopy
puzzle1 = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 3, 0],
           [0, 3, 0, 0, 0], ]
# '/\': u"\u2227"
# '\/': u"\u2228"
logic1 = [['>', '', '<', ''],
          ['', u"\u2228", '', '', ''],
          ['', '', '', ''],
          ['', '', '', u"\u2227", u"\u2227"],
          ['', '', '<', '<'],
          ['', '', '', '', ''],
          ['', '', '', ''],
          ['', '', '', '', ''],
          ['>', '', '', '']]


puzzle2 = [[5, 4, 3, 2, 1],
           [2, 5, 4, 1, 3],
           [3, 2, 1, 5, 4],
           [1, 3, 2, 4, 5],
           [4, 1, 5, 3, 2], ]

puzzle3 = [[5, 4, 3, 2, 1],
           [2, 5, 4, 1, 3],
           [3, 2, 1, 5, 4],
           [4, 3, 2, 4, 5],
           [1, 1, 5, 3, 2], ]
# '/\': u"\u2227"
# '\/': u"\u2228"
logic2 = [['', '', '', ''],
          ['', '', '', '', ''],
          ['', '>', '', '<'],
          [u"\u2227", '', '', '', u"\u2227"],
          ['', '', '', '>'],
          ['', '', '', '', ''],
          ['', '', '', ''],
          [u"\u2227", '', '', u"\u2228", ''],
          ['', '', '', '>']]
puzzle3 = [[0, 0, 0, 0, 0],
           [0, 3, 0, 0, 0],
           [0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0], ]

logic3 = [['', '>', '', ''],
          [u"\u2227", '', '', '', ''],
          ['<', '', '', ''],
          ['', u"\u2228", u"\u2228", '', ''],
          ['', '', '', ''],
          ['', '', '', '', u"\u2227"],
          ['>', '', '', '<'],
          [u"\u2227", '', '', '', ''],
          ['', '', '', '']]


def puzzle_printer(puzzle, logic):
    for i, l_line in enumerate(logic):
        if (i+1) % 2:  # number lines
            print('{n[0]}{l[0]:1}{n[1]}{l[1]:1}{n[2]}{l[2]:1}{n[3]}{l[3]:1}{n[4]}'.format(
                n=puzzle[i//2], l=l_line))
        else:  # logic lines
            print('{l[0]:1} {l[1]:1} {l[2]:1} {l[3]:1} {l[4]:1}'.format(l=l_line))


def single_cell_tester(cell_number, neighbours, nearby_logic, only_check_two=False):
    # "Only check two" allows for the fact that checking only right and down for all squares will be equally valid and quicker.
    result = True
    if nearby_logic[0] == '>' and neighbours[0] is not None:
        result = result & (cell_number > neighbours[0])
    if nearby_logic[1] == u"\u2228" and neighbours[1] is not None:
        result = result & (cell_number > neighbours[1])
    if nearby_logic[2] == '<' and neighbours[2] is not None and not only_check_two:
        result = result & (cell_number > neighbours[2])
    if nearby_logic[3] == u"\u2227"and neighbours[3] is not None and not only_check_two:
        result = result & (cell_number > neighbours[3])

    if nearby_logic[0] == '<'and neighbours[0] is not None and neighbours[0] != 0:
        result = result & (cell_number < neighbours[0])
    if nearby_logic[1] == u"\u2227" and neighbours[1] is not None and neighbours[1] != 0:
        result = result & (cell_number < neighbours[1])
    if nearby_logic[2] == '>' and neighbours[2] is not None and neighbours[2] != 0 and not only_check_two:
        result = result & (cell_number < neighbours[2])
    if nearby_logic[3] == u"\u2228" and neighbours[3] is not None and neighbours[3] != 0 and not only_check_two:
        result = result & (cell_number < neighbours[3])

    return result


def logic_finder(logic):
    # logic_matrix = [[[None]*4] * 5]*5
    logic_matrix = [[[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]],
                    [[None, None, None, None], [None, None, None, None], [None, None, None, None],
                     [None, None, None, None], [None, None, None, None]],
                    [[None, None, None, None], [None, None, None, None], [None, None, None, None],
                     [None, None, None, None], [None, None, None, None]],
                    [[None, None, None, None], [None, None, None, None], [None, None, None, None],
                     [None, None, None, None], [None, None, None, None]],
                    [[None, None, None, None], [None, None, None, None], [None, None,
                                                                          None, None], [None, None, None, None], [None, None, None, None]]
                    ]

    for j in range(5):
        for i in range(5):
            # Finding logic to test this cell against
            try:
                # right
                logic_matrix[j][i][0] = logic[j*2][i]
            except IndexError:
                logic_matrix[j][i][0] = None
            try:
                # below
                logic_matrix[j][i][1] = logic[(j*2)+1][i]
            except IndexError:
                logic_matrix[j][i][1] = None

            try:
                # left
                if i-1 < 0:
                    logic_matrix[j][i][2] = None
                else:
                    logic_matrix[j][i][2] = logic[j*2][i-1]
            except IndexError:
                logic_matrix[j][i][2] = None
            try:
                # above
                if (j*2)-1 < 0:
                    logic_matrix[j][i][3] = None
                else:
                    logic_matrix[j][i][3] = logic[(j*2)-1][i]
            except IndexError:
                logic_matrix[j][i][3] = None
    return logic_matrix


def get_neighbours(puzzle, j, i):
    neighbours = [None]*4
    try:
        neighbours[0] = puzzle[j][i+1]
    except IndexError:
        pass
    try:
        neighbours[1] = puzzle[j+1][i]
    except IndexError:
        pass
    try:
        neighbours[2] = puzzle[j][i-1]
    except IndexError:
        pass
    try:
        neighbours[3] = puzzle[j-1][i]
    except IndexError:
        pass

    return neighbours


def get_possible_neighbours(p, j, i, index=0):
    neighbours = [None]*4
    try:
        neighbours[0] = p[j][i+1][index]
    except IndexError:
        pass
    try:
        neighbours[1] = p[j+1][i][index]
    except IndexError:
        pass
    try:
        neighbours[2] = p[j][i-1][index]
    except IndexError:
        pass
    try:
        neighbours[3] = p[j-1][i][index]
    except IndexError:
        pass

    return neighbours


def valid(puzzle, logic):
    tests_to_be_performed = logic_finder(logic)
    all_cells_valid = True
    zero_flag = False
    all_lines_filled = True
    logic_failures = []
    for j, line in enumerate(puzzle):
        for i, n in enumerate(line):
            if n == 0:
                # any zeroes mean not completed puzzle
                print('Not Complete (Zeroes Present) Checking Logic')
                zero_flag = True
            else:
                # Applying the tests to the cell
                cell_valid = single_cell_tester(
                    cell_number=puzzle[j][i], neighbours=get_neighbours(puzzle, j, i), nearby_logic=tests_to_be_performed[j][i], only_check_two=True)
            if not cell_valid:
                print('Logic Failure caused by cell: {},{} (line, index)'.format(j, i))
                logic_failures.append((j, i))
                all_cells_valid = False
        l = line.copy()
        l.sort()
        if l != [1, 2, 3, 4, 5]:
            print(
                "The line {} does not have solely the numbers 1-5 (inclusive), therefore is invalid".format(
                    puzzle.index(line)))
            all_lines_filled = False

    return (all_cells_valid, all_lines_filled, zero_flag), logic_failures

#
# def valid_for_all_possible_neighbours(logic_matrix, p, j, i):
#     # Check each value in current square that it could exist with combinations nearby
#     not_valid_numbers = []
#     for value in p[j][i]:
#         ok = True
#         # Check that this value is compatible with the possible neighbours
#         for index in range(5):
#             neighbours = get_possible_neighbours(p=p, j=j, i=i, index=index)
#             ok = ok & single_cell_tester(value, neighbours=neighbours,
#                                          nearby_logic=logic_matrix[j][i])
#         if not ok:
#             not_valid_numbers.append(value)
#
#     for number in not_valid_numbers:
#         p[j][i].remove(number)
#     return p
    # p[j][i] = [x for x in p[j][i] if ]
    # if nearby_logic[0] == '>':
    #     recursive_more_than(logic_matrix, p, j, i+1)
    # elif nearby_logic[1] == u"\u2228":
    #     recursive_more_than(logic_matrix, p, j+1, i)
    # elif nearby_logic[2] == '<':
    #     recursive_more_than(logic_matrix, p, j, i-1)
    # elif nearby_logic[3] == u"\u2227":
    #     recursive_more_than(logic_matrix, p, j-1, i)
    # except ValueError:
    #     pass


def recursive_more_than(logic_matrix, p, j, i):
    nearby_logic = logic_matrix[j][i]
    # print("Currently in {},{}".format(j, i))
    # CHECK WHETHER RECURSION COULD BE MOVED UP
    # next cell is less than current cell
    if nearby_logic[0] == '>':
        try:
            p[j][i] = [x for x in p[j][i] if x > min(p[j][i+1])]
        except ValueError:
            pass
        recursive_more_than(logic_matrix, p, j, i+1)

    if nearby_logic[1] == u"\u2228":
        try:
            # p[j][i].remove((min(p[j+1][i])))
            p[j][i] = [x for x in p[j][i] if x > min(p[j+1][i])]
        except ValueError:
            pass
        recursive_more_than(logic_matrix, p, j+1, i)
    if nearby_logic[2] == '<':
        try:
            # p[j][i].remove((min(p[j][i-1])))
            p[j][i] = [x for x in p[j][i] if x > min(p[j][i-1])]
        except ValueError:
            pass
        recursive_more_than(logic_matrix, p, j, i-1)
    if nearby_logic[3] == u"\u2227":
        try:
            # p[j][i].remove((min(p[j-1][i])))
            p[j][i] = [x for x in p[j][i] if x > min(p[j-1][i])]
        except ValueError:
            pass
        recursive_more_than(logic_matrix, p, j-1, i)
    return p


def recursive_less_than(logic_matrix, p, j, i):
    nearby_logic = logic_matrix[j][i]
    # print("Currently in {},{}".format(j, i))
    # next cell is greater than current cell
    if nearby_logic[0] == '<':
        try:
            p[j][i] = [x for x in p[j][i] if x < max(p[j][i+1])]
        except ValueError:
            pass
        recursive_less_than(logic_matrix, p, j, i+1)

    if nearby_logic[1] == u"\u2227":
        try:
            p[j][i] = [x for x in p[j][i] if x < max(p[j+1][i])]
        except ValueError:
            pass
        recursive_less_than(logic_matrix, p, j+1, i)
    if nearby_logic[2] == '>':
        try:
            p[j][i] = [x for x in p[j][i] if x < max(p[j][i-1])]
        except ValueError:
            pass
        recursive_less_than(logic_matrix, p, j, i-1)
    if nearby_logic[3] == u"\u2228":
        try:
            p[j][i] = [x for x in p[j][i] if x < max(p[j-1][i])]
        except ValueError:
            pass
        recursive_less_than(logic_matrix, p, j-1, i)
    return p


def line_match(row, match_list):
    row_matches = [index for index, val in enumerate(row) if val == match_list]
    if len(row_matches) == len(match_list):
        non_matched_row_indices = [x for x in range(5) if x not in row_matches]
        for index in non_matched_row_indices:
            try:
                for num in match_list:
                    row[index].remove(num)
            except ValueError:
                continue

    # Now all exact matches are removed, look for partial matches:
    if len(match_list) == 2 and len(row_matches) == 1:
        # print("Partial matching: match_list {} and \n row:{} ".format(match_list, row))
        rest_of_row = list(filter(lambda a: a != match_list, deepcopy(row)))
        third_values_attempted = []
        for item in rest_of_row:
            if len(item) == 3 and all(x in item for x in match_list):  # all of the match list is contained

                ic = [x for x in deepcopy(item) if x not in match_list]
                # ic.remove(match_list[0])
                # ic.remove(match_list[1])
                # print("Checking {}, Third value in item = {}".format(item, ic[0]))
                if ic[0] in third_values_attempted:
                    pass
                else:
                    third_values_attempted.append(ic[0])
                    new_match_value = deepcopy(match_list)
                    new_match_value.append(ic[0])
                    new_match_value.sort()

                    new_row_matches = [index for index,
                                       val in enumerate(row) if (val == new_match_value) or (val == match_list)]

                    if len(new_row_matches) == 3:
                        # print("Partial matching match_list: {} extended to: {} for \nrow: {}".format(
                            # match_list, new_match_value, row))

                        # print("Found {} matches, removing {} from row ".format(
                            # len(new_row_matches), new_match_value))
                        non_matched_row_indices = [x for x in range(5) if x not in new_row_matches]
                        for index in non_matched_row_indices:
                            for num in new_match_value:
                                try:
                                    row[index].remove(num)
                                except ValueError:
                                    continue
                        # print("New row: {}".format(row))

    return row


def only_possible_location(line, index):
    other_indices = [0, 1, 2, 3, 4]
    other_indices.remove(index)

    poss_values = line[index]

    for val in poss_values:
        other_occurences = 0
        for i in other_indices:
            if val in line[i]:
                # Count up if there is another possible location
                other_occurences += 1
        if other_occurences == 0:
            # If none then this place is the only one you can put this value
            line[index] = [val]
    return line


def poss_locations(pc, j, i):
    row = pc[j].copy()
    row = only_possible_location(row, i)
    pc[j] = row
    col = [x[i] for x in pc.copy()]
    col = only_possible_location(col, j)
    for m in range(5):
        pc[m][i] = col[m]
    return pc


def find_matches(pc, j, i):
    match_list = pc[j][i]
    # Match the row first
    row = pc[j].copy()
    row = line_match(row, match_list)
    # Match the column next
    col = [x[i] for x in pc.copy()]
    col = line_match(col, match_list)
    # As shallow copies have been used, the possibility matrix will have been altered
    return pc


def possible_values(puzzle, logic, p):
    logic_layout = logic_finder(logic)
    pc = deepcopy(p)
    for j, line in enumerate(puzzle):
        for i, number in enumerate(line):
            if number != 0 or len(pc[j][i]) == 1:
                if number == 0:
                    no = pc[j][i][0]
                else:
                    no = number
                # print('Removing {} from column and line due to appearance at {}, {}'.format(number, j, i))
                other_line = [0, 1, 2, 3, 4]
                other_line.remove(i)

                for k in other_line:
                    try:
                        # print('{},{}'.format(l, i))
                        pc[j][k].remove(no)
                    except (ValueError, IndexError):
                        pass
                other_column = [0, 1, 2, 3, 4]
                other_column.remove(j)
                for l in other_column:
                    try:
                        pc[l][i].remove(no)
                    except (ValueError, IndexError):
                        pass
                pc[j][i] = [no]
            else:
                # Removing the maxima from neighbours in 'less than' locations, and minima from 'more than' locations
                pc = recursive_more_than(logic_layout, pc, j, i)
                # current cell is less than the next cell along
                pc = recursive_less_than(logic_layout, pc, j, i)
                if len(pc[j][i]) == 2 or len(pc[j][i]) == 3:
                    pc = find_matches(pc, j, i)
                pc = poss_locations(pc, j, i)

    return pc


# puzzle_printer(puzzle2, logic2)

# p = [[[1, 2, 3, 4, 5]] * 5] * 5 # List comprehension causes issues with deletion (most likely due to implied copies)


# p_orig = possible_values(puzzle1, logic1, p)
# possible_values(puzzle1, logic1, p)


def consistent_past_values(puzzle, logic):
    p = [[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]
    p_prev = None
    t = 0

    while p != p_prev and t < 15:
        p_prev = p
        p = possible_values(puzzle, logic, p_prev)
        t += 1

    print("Found a consistent set of possible values after {} iterations".format(t))
    return p


# print(p[0])


a = [[[3, 4, 5], [2, 4], [1, 2, 3, 4], [2, 4, 5], [1, 2, 3, 4, 5]],
     [[3, 4, 5], [1, 2], [3, 4, 5], [1, 2], [3, 4]],
     [[1, 2, 3, 4, 5], [1, 2, 4, 5], [1, 2, 3], [2, 4], [4, 5]],
     [[1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5], [3], [1, 2, 4, 5]],
     [[4, 5], [3], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5]]]

b = [[[3, 4, 5], [2, 4], [1, 2, 3, 4], [2, 4, 5], [1, 2, 3, 4, 5]],
     [[3, 4, 5], [1, 2], [3, 4, 5], [1, 2], [3, 4]],
     [[1, 2, 3, 4, 5], [1, 2, 4, 5], [1, 2, 3], [2, 4], [4, 5]],
     [[1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5], [3], [1, 2, 4, 5]],
     [[4, 5], [3], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5]]]

c = [[[3, 4, 5], [2, 4], [1, 2, 3, 4], [2, 4, 5], [1, 2, 3, 4, 5]],
     [[3, 4, 5], [1, 2], [3, 4, 5], [1, 2], [3, 4]],
     [[1, 2], [1, 2, 4, 5], [1, 2, 3], [2, 4], [4, 5]],
     [[1, 2], [1, 2, 4, 5], [1, 2, 4, 5], [3], [1, 2, 4, 5]],
     [[4, 5], [3], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5]]]

d = [[[3, 4, 5], [2, 4], [1, 2, 3, 4], [2, 4, 5], [1, 2, 3, 4, 5]],
     [[3, 4, 5], [1, 2], [3, 4, 5], [1, 2], [3, 4]],
     [[1, 2], [1, 2, 4, 5], [3], [4], [5]],
     [[1, 2], [1, 2, 4, 5], [1, 2, 4, 5], [3], [1, 2, 4, 5]],
     [[4, 5], [3], [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 4, 5]]]

e = [[[5], [4], [1], [2], [3]],
     [[3], [2], [5], [1], [4]],
     [[2], [1], [3], [4], [5]],
     [[1], [5], [4], [3], [2]],
     [[4], [3], [2], [5], [1]]]


def sol_print(p):
    for line in p:
        print(line)
        # print("{:4d} {:4d} {:4d} {:4d} {:4d}".format(line[0], line[1], line[2], line[3], line[4]))

        # print("{},{} : Checking values: {}".format(j, i, p[j][i]))
# print(valid(puzzle2, logic2))
# puzzle_printer(puzzle1, logic1)
#
# p = consistent_past_values(puzzle1, logic1)


# print("Is this the same as previous best guess? {}".format(d == p))
# sol_print(p)
puzzle_printer(puzzle1, logic1)
sol_print(consistent_past_values(puzzle1, logic1))
puzzle_printer(puzzle3, logic3)
sol_print(consistent_past_values(puzzle3, logic3))

# print(recursive_less_than(logic_finder(logic3), p2, 2, 2))
# t = 0
# pz = deepcopy(puzzle1)
# poss = consistent_past_values(pz, logic1)
# solution_found, problem_location = valid(pz, logic1)
# prev_locations = []
# prob_loc = (0, 0)
#
# last_tried_values = [[[], [], [], [], []],
#                      [[], [], [], [], []],
#                      [[], [], [], [], []],
#                      [[], [], [], [], []],
#                      [[], [], [], [], []]]
#
# print(valid(puzzle1, logic1))

# #
# while t < 1000 and not solution_found:
#     poss = consistent_past_values(pz, logic1)
#     solution_found, prob_loc = valid(pz, logic1)
#     for j in range(5):
#         for i in range(5):
#             if len(poss[j][i]) == 1:
#                 pz[j][i] = poss[j][i][0]
#             elif len(poss[j][i]) == 2:
#                 for x in poss[j][i]:
#                     if x not in last_tried_values[j][i]:
#                         pz[j][i] = x
#                         last_tried_values[j][i].append(x)
#                         prev_locations.append((j, i))
#                         break
#                     elif x in last_tried_values[j][i] and x!= poss[j][i][-1]: # has been tried and is not the last value:
#                         pass
#
#     if prob_loc[1] == 0:
#         print("Previous error was due to line being filled improperly. {} {}".format(
#             prob_loc[0], prob_loc[1]))
#         continue
#     elif prob_loc == attempted_solutions[-1]:
#         print("Last adjustment caused problem, jumping there.")
#         j = prob_loc[0]
#         i = prob_loc[1]
#         poss_for_cell = p[j][i]
#         for poss in poss_for_cell:
#             if poss not in last_tried_values[j][i]:
#                 pz[j][i] = poss
#                 last_tried_values[j][i].append(poss)
#                 solution_found, prob_loc = valid(pz, logic1)
#                 attempted_solutions.append((j, i))
#                 break

#     for j in range(5):
#         for i in range(5):
#             poss_for_cell = p[j][i]
#             if len(poss_for_cell) == 1:
#                 pz[j][i] = p[j][i][0]
#                 print("Found single value {} for cell {},{}".format(p[j][i], j, i))
#                 prev_locations.append((j, i))
#             else:  # len(poss_for_cell) < 4:
#                 # print("Found {} values for cell {},{}".format(len(p[j][i]), j, i))
#                 # print("Setting random value from possible values")
#                 for poss in poss_for_cell:
#                     if poss not in last_tried_values[j][i]:
#                         print('Trying new value')
#                         pz[j][i] = poss
#                         last_tried_values[j][i].append(poss)
#                         solution_found, prob_loc = valid(pz, logic1)
#                         attempted_solutions.append((j, i))
