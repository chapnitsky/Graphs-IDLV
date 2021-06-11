import os
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt

ratio = np.arange(1, 10.1, 0.1)
ratio = [float(format(float(x), '.1f')) for x in ratio]
x = [int(c) for c in ratio if c.is_integer()]
avg = defaultdict(list)
median = defaultdict(list)
src = defaultdict(list)
y_steps = 5
points = list(tuple())
types = [50, 100, 150]
start = 3
end = 4
for i in range(start, end, 1):
    for g_type in types:
        avg[g_type] = []
        median[g_type] = []
        src[g_type] = []
        path = os.getcwd() + r'\to_Graph' + str(i) + r'\type' + str(g_type)
        for r in ratio:
            res = path + r'\experiment' + str(format(float(r), '.1f')) + r'\res' + str(format(float(r), '.1f')) + '.txt'
            if not os.path.exists(res):
                exit(1)
            f = open(res, 'r+')
            content = f.read().splitlines()
            for j, line in enumerate(content):
                if line.find("Median =") == 0:
                    MED = content[j][9:]
                    median[g_type].append(round(float(MED)))
                elif line.find("Average =") == 0:
                    AVG = content[j][9:]
                    avg[g_type].append(round(float(AVG)))
                elif line.find("Average Source =") == 0:
                    tmp_src = content[j][16:]
                    src[g_type].append(round(float(tmp_src)))
            f.close()

    path = os.getcwd() + r'\to_Graph' + str(i)
    mGraph = plt.figure(1)
    plt.xlabel("Rules / Variables  Ratio")
    plt.ylabel("Average")
    plt.title(f"AVG, rule len = {i}", fontsize=20)
    for t in types:
        plt.plot(ratio, avg[t], label=f"{str(t)} Variables")
    plt.legend(loc='best')
    plt.grid(axis='y', linestyle='-')
    #s = np.array(types)
    #plt.yticks(s)
    #plt.yticks(np.arange(min(s), max(s)+1, y_steps))
    plt.savefig(path + r'/AVG' + str(i) + '.png')
    # mGraph.show()

    aGraph = plt.figure(2)
    plt.xlabel("Rules / Variables  Ratio")
    plt.ylabel("Median")
    plt.title(f"MEDIAN, rule len = {i}", fontsize=20)
    for t in types:
        plt.plot(ratio, median[t], label=f"{str(t)} Variables")
    plt.legend(loc='best')
    plt.grid(axis='y', linestyle='-')
    #plt.yticks(s)
    #s = np.array(types)
    #plt.yticks([])
    #plt.yticks(np.arange(min(s), max(s)+1, y_steps))
    plt.savefig(path + r'/MED' + str(i) + '.png')
    # aGraph.show()
    plt.show()

