from collections import defaultdict
from Graph import Graph
import os
import sys
visited = defaultdict(bool)
no_path = []


def minimal_set(rules, scc_pointers, graph) -> tuple:
    q = []
    types = defaultdict(bool)
    # num_of_views = 3
    max_ind = len(rules)
    nodes = list(graph.keys())
    path_to_of = defaultdict(list)
    min_src_len = None
    for n in nodes:
        path_to_of[n] = find_all_paths_to(scc_pointers, graph, n)[1]
        if not path_to_of[n]:  # If there is no path to n = source
            _vert = list(graph[n].get_nodes().keys())
            weight = len(_vert)
            history = [False]*max_ind
            q.append([_vert, weight, 0, history])
            if not min_src_len:
                min_src_len = weight
            elif weight < min_src_len:
                min_src_len = weight

    if not q:
        return '1', None
    count = 0
    last = None
    while True:
        q = sorted(q, key=lambda triplet: triplet[1])
        cur = q.pop(0)
        cur_ver = list(cur[0])
        cur_w = int(cur[1])
        cur_ind = int(cur[2])
        cur_history = list(cur[3])
        changed = False
        while cur_ind < max_ind and not changed:
            if cur_history[cur_ind]:
                cur_ind += 1
                continue
            arrow_ind = rules[cur_ind].find(':-')
            temp1 = rules[cur_ind][:arrow_ind]
            temp2 = rules[cur_ind][(arrow_ind + 2):] + ' '
            head = []
            body = []
            num = ''
            for h in temp1:
                if h.isdigit():
                    num += h
                else:
                    head.append(num)
                    num = ''
            for b in temp2:
                if b.isdigit():
                    num += b
                elif num:
                    body.append(num)
                    num = ''

            index = 0
            is_in_head = False
            while not changed and index < len(head) and not is_in_head:
                if head[index] in cur_ver:
                    is_in_head = True
                    rule = head + body
                    forest = []
                    for y in rule:
                        add = path_to_of[y]
                        forest.append(y)
                        if add:
                            forest.extend(add)
                    before_len = len(cur_ver)
                    cur_ver.extend(forest)
                    cur_ver = list(dict.fromkeys(cur_ver).keys())
                    check = len(cur_ver) - before_len
                    cur_history[cur_ind] = True
                    if check != 0:
                        cur_w += check
                        changed = True

                else:
                    index += 1

            cur_ind += 1
            if changed:
                q.append([cur_ver, cur_w, 0, cur_history])

        if not changed and cur_ind == max_ind:  # FOUND
            leng = len(cur_ver)
            last = cur_ver
            # if leng > 1:
            return cur_ver, min_src_len
            # if not types[leng]:
            #     types[leng] = True
            #     count += 1
            #     if count == num_of_views:
            #         return cur_ver, min_src_len
        if not q:
            return last, min_src_len


def find_all_paths_to(scc_pointers, graph, dst) -> (list, list):
    to_return = []
    sc_names = []
    nodes = list(graph.keys())
    global visited
    global no_path

    for n in nodes:
        visited[n] = False

    visited[dst] = True
    for node in nodes:
        check = no_path
        if not visited[node] and node not in check:
            temp_dic = visited.fromkeys(visited, False)
            dfs(node, dst, temp_dic, scc_pointers, [], None)

    visited[dst] = False
    for temp in visited:
        if visited[temp]:
            to_return.extend(list(graph[temp].get_nodes().keys()))
            sc_names.append(temp)

    visited.clear()
    no_path.clear()
    return to_return, sc_names


def dfs(src, dst, visited_dic, neighbors, path, file):
    if src != dst:
        visited_dic[src] = True

    global no_path
    path.append(src)
    if src == dst:
        global visited
        size = len(path)
        for i, temp in enumerate(path):
            if not visited[temp] and i != (size - 1):
                visited[temp] = True
    else:
        for neighbor in neighbors[src]:
            if not visited_dic[neighbor] and neighbor not in no_path:
                dfs(neighbor, dst, visited_dic, neighbors, path, file)

    n_path = path.pop()
    if n_path != dst and not visited[n_path]:
        no_path.append(n_path)


# MAIN
# args = sys.argv[1:]
args = ['graph.txt', 'set', 'program.txt']
file_name = None
f_return = None
action = None
info = None
if args:
    if len(args) != 3:
        print("Wrong arguments. Please add arguments:\n"
              "If in windows cmd: python script_name.py graph_file_name.text tree/set scc_name/program.txt\n"
                  "Respectively")
        exit()
    file_name = args[0]
    if args[1] == 'tree':
        action = 'tree'
        info = args[2]
    elif args[1] == 'set':
        action = 'set'
        info = args[2]
    else:
        print("Wrong arguments. Please add arguments:\n"
              "If in windows cmd: python script_name.py graph_file_name.text tree/set scc_name/program.txt\n"
              "Respectively")

    if os.path.exists(file_name):
        if info is not None:
            if action == 'set':
                if os.path.exists(info):
                    f_return = open("set.txt", "w+")
                    print("Calculating minimal set with {0} and {1}".format(file_name, info))
                else:
                    print("Cannot find the file {0}".format(info))
            elif action == 'tree':
                f_return = open("has_path_to_{}.txt".format(info), "w+")
                print("Calculating path to {0} with {1}".format(info, file_name))
        else:
            print("Wrong arguments. Please add arguments:\n"
              "If in windows cmd: python script_name.py graph_file_name.text tree/set scc_name/program.txt\n"
              "Respectively")
            exit()
    else:
        print("Cannot find the file {0}".format(file_name))
        exit()
else:
    print("Wrong arguments. Please add arguments:\n"
          "If in windows cmd: python script_name.py graph_file_name.text tree/set scc_name/program.txt\n"
          "Respectively")
    exit()


f = open(file_name, "r")
content = f.read()
f.close()
lis_t = content.splitlines()
lis_t = [i for i in lis_t if i]
recreated_super = defaultdict(Graph)
pointers = defaultdict(list)
SCC = False
# Reverse engineering, creating the super graph
for line in lis_t:
    length = len(line)
    if not SCC:
        vertexes = []
        name = None
        ind = 0
        while ind < length:
            if line.find('(') != -1:    # normal graph edges
                break
            if line[ind].isupper():
                if line.find("SCC") != -1:
                    SCC = True
                    break
                equal_ind = line.find('=')
                if equal_ind == -1:
                    break
                name = line[ind:equal_ind]
                ind = equal_ind + 1
                continue
            elif line[ind].isdigit():
                cur_vertex = ''
                while line[ind] != ',' and line[ind] != '}':
                    cur_vertex += line[ind]
                    ind += 1
                if cur_vertex != '':
                    vertexes.append(cur_vertex)
                    cur_vertex = ''
            if line[ind] == '}':
                if name:
                    g = Graph()
                    g.set_name(name)
                    for ver in vertexes:
                        g.add_node(ver)
                    recreated_super[name] = g
            ind += 1

    elif SCC:   # SCC edges
        comma_ind = line.find(',')
        u = line[1:comma_ind]
        v = line[comma_ind + 1:length - 1]
        pointers[u].append(v)

# if not SCC:
#     print("(Clique COMPONENT)")

if action == 'set':
    f_program = open(info, "r")
    content = f_program.read()
    f_program.close()
    program = content.splitlines()
    program = [i for i in program if i]
    ans, src = minimal_set(program, pointers, recreated_super)
    f_return.write(','.join(ans) + ' | ' + str(src))
    f_return.flush()
    f_return.close()
    print('Saving results to {0}'.format(f_return.name))


else:
    vert, names = find_all_paths_to(pointers, recreated_super, info)
    f_return.write(','.join(vert))
    f_return.flush()
    f_return.close()
    print('Saving results to {0}'.format(f_return.name))