from collections import defaultdict
from Node import Node
from Graph import Graph
import os
import sys
global_time = -1


def normal_graph(program: list) -> Graph:  # program is a list of strings
    u_list = []  # an edge is in the format of (u,v): u -> v
    v_list = []
    init = True  # flag of the first run
    g = None  # our graph
    for string in program:
        string = str(string)
        ind = string.find(':-')
        if ind == -1:
            print("Wrong syntax.")
            exit()
        string = string.replace(" ", "")  # delete spaces
        string += ' '  # adding one space at the end
        temp = ''
        colon_flag = False
        for char in string:
            if char.isdigit():
                temp += char
            else:
                if not colon_flag and temp != '':
                    v_list.append(temp)
                elif colon_flag and temp != '':
                    u_list.append(temp)
                temp = ''
                if char == ':':
                    colon_flag = True
        if init:
            init = False
            g = Graph()  # initiating our graph with the first vertex
        if not u_list and len(v_list) == 1:  # rule with only one vertex in head
            g.add_edge(v_list[0], v_list[0])  # marked with edge(u,u)

        for u in u_list:
            for v in v_list:
                if u != v:
                    g.add_edge(u, v)

        u_list.clear()
        v_list.clear()
    return g


def super_graph(org_graph: Graph):
    super_g = []
    pointers = defaultdict(list)

    # DFS
    nodes = org_graph.get_nodes()
    nodes_keys = org_graph.get_nodes().keys()
    for key in nodes_keys:
        if nodes[key].get_color() == "white":
            dfs_visit(org_graph, key, False, [], nodes, 0, 0)  # 0 is initial global time, i is index

    # G_t
    g_t = Graph()
    for key in org_graph.get_adj().keys():
        neighbors_to_switch = org_graph.get_adj()[key]
        for to_switch in neighbors_to_switch:
            g_t.add_edge(to_switch, key)

    # DFS on G_t
    nodes = org_graph.get_nodes().values()
    rev_sorted_nodes = sorted(nodes, key=lambda x: getattr(x, 'exit_time'), reverse=True)
    exit_time_dict = defaultdict(Node)
    exit_key_dict = defaultdict(int)
    value_key_dict = defaultdict(int)

    for w in rev_sorted_nodes:
        time = w.get_exit_time()
        val = w.get_val()
        exit_time_dict[time].set_val(val)
        exit_key_dict[time] = val
        value_key_dict[val] = time

    temp_tree = []
    asci = 65  # 'A'
    offset_counter = 0
    for key in exit_time_dict.keys():
        if exit_time_dict[key].get_color() == "white":
            dfs_visit(g_t, key, True, temp_tree, exit_time_dict, exit_key_dict, value_key_dict)
            if asci == 91:
                offset_counter += 1
                asci = 65
            temp_scc = Graph()
            temp_scc.set_name(chr(asci) + str(offset_counter))
            asci += 1
            temp_scc.add_node(temp_tree[0])
            for u_key in temp_tree:
                neighbors = org_graph.get_adj()[u_key]
                for neigh in neighbors:
                    if neigh in temp_tree:
                        temp_scc.add_edge(u_key, neigh)
            super_g.append(temp_scc)
            temp_tree.clear()

    for gr1 in super_g:
        gr1_nodes = list(gr1.get_nodes().keys())
        name1 = gr1.get_name()
        for gr2 in super_g:
            if gr2.get_name() == gr1.get_name():
                continue
            name2 = gr2.get_name()
            if pointers.get(name1) is not None:
                if name2 in pointers[name1]:
                    continue
            gr2_nodes = list(gr2.get_nodes().keys())
            break_flag = False
            for u in gr1_nodes:
                if break_flag:
                    break
                for v in gr2_nodes:
                    if org_graph.is_edge(u, v):
                        pointers[name1].append(name2)
                        break_flag = True
                        break

    return super_g, pointers


def dfs_visit(graph: Graph, key: int, scc: bool, tree: list, exit_time_dict, exit_key_dict, value_key_dict):
    global global_time
    global_time += 1
    nodes = graph.get_nodes()
    neighbors = []
    if scc:
        tree.append(exit_key_dict[key])
        neighbors = graph.get_adj()[exit_key_dict[key]]
        exit_time_dict[key].set_color("grey")
    else:
        neighbors = graph.get_adj()[key]
        nodes[key].set_color("grey")
    for v in neighbors:
        if scc:
            if exit_time_dict[value_key_dict[v]].get_color() == "white":
                dfs_visit(graph, value_key_dict[v], scc, tree, exit_time_dict, exit_key_dict, value_key_dict)
        elif nodes[v].get_color() == "white":
            dfs_visit(graph, v, scc, tree, nodes, 0, 0)

    global_time += 1
    nodes[key].set_color("black")
    nodes[key].set_exit_time(global_time)


# MAIN
# args = sys.argv[1:]
args = ['program.txt', '0']
file_name = None
graph_type = None
f_return = None
if args:
    file_name = args[0]
    if len(args) != 2:
        print("input type arguments missing, 0 = normal graph, 1 = super graph")
        exit()
    input_type = args[1]
    if os.path.exists(file_name):
        if input_type.isdigit() and input_type is not None:
            st = 'normal graph'
            if input_type == '1':
                st = 'super graph'
            print("Creating {0} with {1}".format(st, file_name))
            graph_type = input_type
        else:
            print("input type arguments missing, 0 = normal graph, 1 = super graph")
            exit()
    else:
        print("Cannot find the file {0}".format(file_name))
        exit()
else:
    print("Not enough arguments. Please add file name and the graph type:\n"
          "If in windows cmd: python script_name.py input_file_name.text graph_type(0 = normal graph, 1 = super graph)")
    exit()

if file_name:
    f = open(file_name, "r")
    content = f.read()
    lis_t = content.splitlines()
    f_return = open("graph.txt", "w+")
    normal_g = normal_graph(lis_t)
    if graph_type == '0':
        f_return.write(normal_g.send_str())
        f_return.close()
        exit()

    super_gr, p = super_graph(normal_g)

    for gr in super_gr:
        temp_list = '{' + ', '.join(list(gr.get_nodes().keys())) + '}'
        group = '\n' + gr.get_name() + '=' + temp_list + '\n'
        f_return.write(group)
        edges = gr.send_str()
        if edges != '':
            s = gr.get_name() + ' edges:\n' + edges
            f_return.write(s)

    flag = False
    for scc_u in p.keys():
        if p[scc_u] and not flag:
            flag = True
            f_return.write("\nSCC edges:")
        for scc_v in p[scc_u]:
            f_return.write('\n')
            f_return.write('({0},{1})'.format(scc_u, scc_v))

    f_return.close()
    print("Saving to graph.txt")
