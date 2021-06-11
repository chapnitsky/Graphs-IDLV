import random
from collections import defaultdict
import sys
import numpy as np


def generate(num_of_rules: int, rule_len: int, num_of_vars: int, max: bool):
    if num_of_rules <= 0 or rule_len <= 1 or num_of_vars <= 1 or num_of_vars > rule_len*num_of_rules or num_of_vars < rule_len:
        print("Wrong arguments.")
        exit(1)

    options = 1
    tempr = rule_len
    tempv = num_of_vars
    while tempr > 0:
        options *= tempv
        tempv -= 1
        tempr -= 1

    if num_of_rules > options:
        print("Too long program with the calculating on rule length and number of vars.\n")
        exit(1)

    rules = []
    is_used = defaultdict(bool)
    variables = [x for x in range(1, num_of_vars + 1)]
    for var in variables:
        is_used[var] = False
    # prefix = ['-', 'not', '']
    prefix = ['not', '']
    k = 0
    all_used_flag = False
    first_all_used = True
    origin_rule_len = rule_len
    list_int = []
    while k < num_of_rules:
        cur_vars = rule_len = origin_rule_len
        if all_used_flag and max:
            cur_vars = rule_len = random.randint(1, origin_rule_len)
        head_pattern = ''
        arrow_options = [i for i in range(2, rule_len*3, 3)]
        arrow_options.append(0)
        arrow_ind = random.sample(arrow_options, 1).pop()
        if max:
            arrow_ind = 2 # With two indexes represent a number, choose specific arrow index.
        if arrow_ind != 0:
            for j in range(-1, arrow_ind, 4):
                head_pattern += '{}|'
                cur_vars -= 1
        head_pattern = head_pattern[:-1]
        if not head_pattern:
            head_pattern = ':- '
        else:
            head_pattern += ' :- '

        body_pattern = ''
        while cur_vars > 0:
            body_pattern += random.sample(prefix, 1).pop() + '{}, '
            cur_vars -= 1
        body_pattern = body_pattern[:-2]

        rule = head_pattern + body_pattern
        if all_used_flag:
            if first_all_used:  # just to skip this iteration for making a new rule pattern
                first_all_used = False
                continue
            list_int = random.choices(variables, k=rule_len)
        else:
            list_int.clear()
            temp = list(is_used.keys())
            to_add_counter = 0
            found_unused_flag = False
            for t in temp:
                if not is_used[t]:
                    list_int.append(t)
                    is_used[t] = True
                    found_unused_flag = True
                    to_add_counter += 1
                    if to_add_counter == rule_len:
                        break
            if not found_unused_flag:
                all_used_flag = True
                continue

        length = len(list_int)
        if length < rule_len and not (all_used_flag and max):
            to_add = rule_len - length
            while to_add > 0:
                check = list(random.sample(variables, 1))
                if check not in list_int:
                    list_int.extend(check)
                    to_add -= 1
        rule = rule.format(*list_int)
        if rule in rules:
            k -= 1  # Make again
        else:
            rules.append(rule)
        k += 1

    return rules


args = sys.argv[1:]
# args = ['20', '3', '30', 'max']
if len(args) < 3:
    print("Wrong usage. Need number of rules, rule length and num of variables")
    exit(1)

max_flag = False
if args[3] and args[3] == 'max':
    max_flag = True
program_list = generate(int(args[0]), int(args[1]), int(args[2]), max_flag)
f = open("program.txt", "w+")
if not program_list:
    print("Wrong arguments.")
    f.close()
    exit(1)
for r in program_list:
    f.write(r + '\n')
f.close()
print("Saving to program.txt")
