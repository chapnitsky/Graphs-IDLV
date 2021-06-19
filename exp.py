import os
import shutil
import math
import statistics as stat
import numpy as np
import sys

args = sys.argv[1:]
# args = ['idlv']
custom = False
ratio = np.arange(1.0, 10.1, 0.1)
if len(args) == 1 and args[0] == 'idlv':  # If you write in console: python exp.py idlv
    custom = True
    ratio = np.arange(0.1, 1, 0.1)
num_of_rules = None
num_of_vars = None
num_of_tests = 100
types = [50, 100, 150]
start = 3
end = 4
for i in range(start, end, 1):
    rule_len = i
    for g_type in types:
        g_t = f'//type{g_type}'
        path = os.getcwd() + '//to_Graph' + str(i)
        os.makedirs(path + g_t, exist_ok=True)
        for r in ratio:
            f = open("res.txt", "w+")
            path = os.getcwd() + '//to_Graph' + str(i)
            exp = path + g_t + '//experiment' + str(format(float(r), '.1f'))
            path = os.getcwd()
            num_of_rules = math.ceil(r * g_type)
            if not num_of_rules:
                print('Num_of_rules error')
                exit(1)
            count = []
            src = []
            start = 0
            for s in range(start, num_of_tests):
                if custom:
                    os.system(f'cmd /c python graph_gene.py {g_type} {r} && idlv 3col.txt graph_in.txt > '
                              f'ground.txt && python ground_actions.py')
                    os.system(f' python get_graph.py program.txt 1 &&'
                              f' python super_actions.py graph.txt set program.txt')
                else:
                    os.system(f'cmd /c python gene.py {num_of_rules} {rule_len} {g_type} &&'
                              f' python get_graph.py program.txt 1 &&'
                              f' python super_actions.py graph.txt set program.txt')
                temp = open("set.txt", "r")
                content = temp.read()
                check = content.find('|')
                temp_src = None
                if check != -1:
                    temp_src = int(content[check + 1:])
                    src.append(temp_src)
                    content = content[:check]
                min_set = content.split(',')
                temp.close()
                count.append(len(min_set))
                if check != -1:
                    f.write(str(len(min_set)) + ' | ' + ','.join(min_set) + ' | ' + str(temp_src) + '\n')
                else:
                    f.write(str(len(min_set)) + ' | ' + ','.join(min_set) + '\n')
                f.flush()
                os.makedirs(exp, exist_ok=True)
                os.makedirs(exp + '//test' + str(s), exist_ok=True)
                if custom:
                    shutil.move(path + '//graph_in.txt', exp + '//test' + str(s))
                    os.rename(exp + '//test' + str(s) + '//graph_in.txt',
                              exp + '//test' + str(s) + '//graph_in' + str(s) + '.txt')
                    shutil.move(path + '//ground.txt', exp + '//test' + str(s))
                    os.rename(exp + '//test' + str(s) + '//ground.txt',
                              exp + '//test' + str(s) + '//ground' + str(s) + '.txt')
                shutil.move(path + '//program.txt', exp + '//test' + str(s))
                os.rename(exp + '//test' + str(s) + '//program.txt',
                          exp + '//test' + str(s) + '//program' + str(s) + '.txt')
                shutil.move(path + '//graph.txt', exp + '//test' + str(s))
                os.rename(exp + '//test' + str(s) + '//graph.txt',
                          exp + '//test' + str(s) + '//graph' + str(s) + '.txt')
                shutil.move(path + '//set.txt', exp + '//test' + str(s))
                os.rename(exp + '//test' + str(s) + '//set.txt', exp + '//test' + str(s) + '//set' + str(s) + '.txt')
            f.write('\nMedian = {}'.format(format(float(stat.median(count)), '.2f')))
            f.write('\nAverage = {}'.format(format(float(sum(count) / len(count)), '.2f')))
            f.write('\nAverage Source = {}'.format(format(float(sum(src) / len(src)), '.2f')))
            f.close()
            shutil.move(path + '//res.txt', exp)
            os.rename(exp + '//res.txt', exp + '//res' + str(format(float(r), '.1f')) + '.txt')
