from Graph import Graph
from collections import defaultdict
import time
import os
import subprocess


def make_dlv_input(g: Graph):
    nodes = sorted(list(g.get_nodes().keys()))
    adj = g.get_adj()
    edges = []
    for u in list(adj.keys()):
        for v in adj[u]:
            edges.append(f'edge({u},{v})')

    _f_dlv = open('graph_dlv.txt', 'w')
    i = 0
    num_of_vars = len(nodes)
    lim_node = num_of_vars - 3
    if num_of_vars % 2 == 0:
        lim_node = num_of_vars
    while i < lim_node:
        _f_dlv.write(f'node({nodes[i]}).' + '\n')
        i += 1
    _f_dlv.write('\n')

    length = len(edges)
    i = 0

    while i < length:
        _f_dlv.write(edges[i] + '.' + '\n')
        i += 1
    _f_dlv.flush()
    _f_dlv.close()


def calc_dlv():
    gr = Graph()
    os.system(f'cmd /c python get_graph.py program.txt 0')  # Program rules: program.txt
    content = open('graph.txt', 'r').readlines()
    content = [eval(line) for line in content]  # making tuples
    for tup in content:
        gr.add_edge(tup(0), tup(1))
    make_dlv_input(gr)
    _calc_dlv = False
    while not _calc_dlv:
        output = subprocess.check_output("cmd /c dlv_updated graph_dlv.txt 3col.txt", shell=True)
        if output != b'DLV 2.1.0\r\n\r\n{}\r\n':
            _calc_dlv = True
            _f_calc = open('calc.txt', 'bw')  # saving DLV model calculation
            _f_calc.write(output)
            _f_calc.flush()
            _f_calc.close()


def get_matrix(data: list):
    _program = data
    matrix = []
    nots = defaultdict(list)
    positive = defaultdict(list)
    nodes = defaultdict(bool)
    for index, rule in enumerate(_program):
        u_list = []
        v_list = []
        string = str(rule)
        ind = string.find(':-')
        if ind == -1:
            print("Wrong syntax for rule, need to see ':-'")
            exit()
        string = string.replace(" ", "")  # delete spaces
        string += ' '  # adding one space at the end
        temp = ''
        not_flag = False
        colon_flag = False
        for i, char in enumerate(string):
            if char.isdigit():
                temp += char
            else:
                if char == 'n' and string[i:i + 3] == 'not':
                    not_flag = True

                if not_flag and temp != '':
                    nots[temp].append(index)  # remember which vertex has a NOT and in which index. (which rule)
                    temp = '-' + temp
                    not_flag = False
                elif not not_flag and temp != '':
                    positive[temp].append(index)

                if not colon_flag and temp != '':
                    v_list.append(temp)
                elif colon_flag and temp != '':
                    u_list.append(temp)

                if temp != '':
                    nodes[abs(int(temp))] = True
                temp = ''
                if char == ':':
                    colon_flag = True

        u_list.extend([None])
        u_list.extend(v_list)

        matrix.append(u_list)
    return matrix, nots, positive, list(nodes.keys())


end_time = None
os.system(f'cmd /c python gene.py 20 3 20 max')  # Program rules: program.txt
start_time = time.time()
model = []
_f_program = open('program.txt', 'r')
_program = _f_program.read().splitlines()
# calc_dlv(_program)
matrix, nots, positive, nodes = get_matrix(_program)
active_rules = defaultdict(bool)
break_while = False
inp = None
done = False
while not done:
    while not break_while:
        used_any_row = False
        for i, row in enumerate(matrix):
            u_list = []
            v_list = []
            to_model = []
            u_flag = True
            for vert in row:
                if vert is None:  # starting seeing V's
                    u_flag = False
                    continue
                if u_flag:
                    u_list.append(vert)
                else:
                    v_list.append(vert)

            v_list = [int(x) for x in v_list]
            u_list = [int(x) for x in u_list]
            if u_list:
                add_flag = True  # Active Body flag
                for u in u_list:
                    if u not in model:
                        add_flag = False
                        break
                if add_flag and [x for x in v_list if x not in model]:
                    model.extend(v_list)  # Adding head to model
                    used_any_row = True
                    active_rules[i] = True

            elif not u_list and [x for x in v_list if x not in model]:
                model.extend(v_list)
                used_any_row = True
                active_rules[i] = True

        if not used_any_row:
            model = list(dict.fromkeys(model))
            break_while = True  # Found all model

    print(str(nodes))
    print("current model: " + str(model))
    inp = input('If you would like to finish just press Enter.\n'
                'Enter a vertex (positive number):')
    if inp == '':
        done = True
        continue
    elif not inp.isdigit():
        print('Wrong input, need a number')
        exit(0)

    inp = int(inp)
    if inp not in nodes:
        model.append(inp)
        nodes.append(inp)
    elif inp in nodes:
        always_neg = inp not in positive
        pos_in_active = None

        if not always_neg:  # inp is positive somewhere
            inp_pos_rules = positive[inp]
            pos_in_active = False
            for index in inp_pos_rules:
                if index in active_rules:
                    pos_in_active = True
                    break

        neg_in_active = False
        inp_neg_rules = nots[inp]
        for index in inp_neg_rules:
            if index in active_rules:
                neg_in_active = True
                break

        if (always_neg or not pos_in_active) and not neg_in_active:  # variable in level 1
            model.append(inp)
            nodes.append(inp)

        elif pos_in_active and not neg_in_active:  # variable in level > 1
            pass


print(model)
print(list(active_rules.keys()))
print(nodes)
