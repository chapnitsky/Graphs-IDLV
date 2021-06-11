f = open('ground.txt', 'r')
p = open('program.txt', 'w+')
content = f.read().splitlines()
f.close()
vertex = []
node_flag = False
edge_flag = False
edge_ind = None
for i, line in enumerate(content):
    if line.find('node') != -1:
        node_flag = True
    elif node_flag:
        ind = line.find('node')
        if ind == -1:
            vertex = [x for x in range(3, int(line[:line.find(' ')]))]
            node_flag = False
    elif edge_flag:
        ind = line.find('edge')
        if ind == -1:
            if len(line) == 1:
                vertex.extend([x for x in range(edge_ind, int(content[i - 1][:content[i - 1].find(' ')]) + 1)])
            else:
                vertex.extend([x for x in range(edge_ind, int(line[:line.find(' ')]))])
            break
    elif line.find('edge') != -1:
        edge_flag = True
        edge_ind = int(line[:line.find(' ')])


for ver in vertex:
    p.write(f'{ver}:-\n')
for line in content:
    rule = ''
    lang = [int(x) for x in line.split(' ') if x.isdigit()]
    if len(lang) == 1:
        if lang[0] == 0:
            break
    num = lang[0]
    if num == 8:  # in head
        iterations = lang[1]
        lang = lang[2:]
        no_need = False
        for j in range(0, iterations):
            if lang[j] in vertex:
                no_need = True
                break
            if lang[j] != 0:
                rule += str(lang[j]) + '|'
        if no_need:
            continue
        rule = rule[:-1] + ' :-\n'
    elif num == 1:  # normal rule
        rule = f'{lang[1]} :- '
        # negatives = lang[3]
        iterations = lang[2]
        lang = lang[4:]
        for j in range(0, iterations):
            if lang[j] != 0:
                rule += str(lang[j]) + ', '
        rule = rule[:-2] + '\n'
    else:
        continue
    p.write(rule)
p.flush()
p.close()
print('Saving to program.txt')
