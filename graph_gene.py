import random
import numpy as np
import sys


def generate(num_of_vars: int, chance: float):
    if chance <= 0 or num_of_vars <= 1:
        print("Wrong arguments.")
        exit(1)

    g = open("graph_in.txt", "w+")

    variables = np.arange(1, num_of_vars + 1)
    i = 0
    lim_node = num_of_vars - 3
    if num_of_vars % 2 == 0:
        lim_node = num_of_vars
    while i < lim_node:
        g.write(f'node({variables[i]}) | node({variables[i + 1]}).' + '\n')
        i += 2
    if num_of_vars % 2 != 0:
        g.write(f'node({variables[num_of_vars - 3]}) | node({variables[num_of_vars - 2]}) | node({variables[num_of_vars - 1]}).' + '\n')
    g.write('\n')
    # prefix = ['-', 'not', '']
    prefix = ['']
    edges = []
    for u in variables:
        for v in variables:
            rand = random.random()
            if rand <= chance and u != v:
                edges.append(f'edge({u}, {v})')
    length = len(edges)
    i = 0
    lim_edge = length - 3
    if length % 2 == 0:
        lim_edge = length
    while i < lim_edge:
        g.write(edges[i] + ' | ' + edges[i + 1] + '.' + '\n')
        i += 2
    if (length % 2 != 0 and length > 2) or length == 3:
        g.write(f'{edges[length - 3]} | {edges[length - 2]} | {edges[length - 1]}.' + '\n')
    elif length == 1:
        g.write(edges[0] + ' .')
    g.flush()
    g.close()
    print("Saving to graph_in.txt")


args = sys.argv[1:]
# args = ['20', '0.5']
if len(args) != 2:
    print("Wrong usage. Need number of vars and edge chance.")
    exit(1)
generate(int(args[0]), float(args[1]))
