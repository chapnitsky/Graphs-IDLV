import os
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt

ratio = np.arange(1, 10.1, 0.1)
ratio = [float(format(float(x), '.1f')) for x in ratio]
types = [50, 100, 150]
start = 3
end = 4
for i in range(start, end, 1):
    data = defaultdict(list)
    data_src = defaultdict(list)
    for g_type in types:
        data[g_type] = [0]*(g_type + 1)
        data_src[g_type] = [0] * (len(ratio))
        path = os.getcwd() + r'\to_Graph' + str(i) + r'\type' + str(g_type)
        index = -1
        for r in ratio:
            index += 1
            res = path + r'\experiment' + str(format(float(r), '.1f')) + r'\res' + str(format(float(r), '.1f')) + '.txt'
            if not os.path.exists(res):
                exit(1)
            f = open(res, 'r+')
            content = f.read().splitlines()
            for line in content:
                if not line:
                    continue
                ind = line.find('|')
                src_ind = line.find('Average Source =')
                if ind != -1:
                    num = line[:ind]
                    num = int(num)
                    data[g_type][num] += 1
                elif src_ind != -1:
                    data_src[g_type][index] = float(line[16:].format('{0.0f}'))
            f.close()

    path = os.getcwd() + r'\to_Graph' + str(i)
    width = 0.25
    ax0 = plt.figure(0, figsize=(15, 15))
    # plt.figure(figsize=(15, 50))

    plt.ylim(0, 150)
    plt.title(f"Statistics, rule len = {i}", fontsize=20)
    w1 = -width
    for t in types:
        data[t] = data[t][1:]
        for j, num in enumerate(data[t]):
            if num > 150:
                data[t][j] = 150
        x1 = np.arange(1, t + 1, 1)
        x1 = x1 + w1
        w1 = w1 + width
        plt.bar(x1, data[t], width=width, label=f"{str(t)} Variables")
        # index = -1
        # src_offset = w1 - width
        # for r in ratio:
        #     index += 1
        #     src = data_src[t][index]
        #     if src != 0:
        #         ax.annotate(src, xy=(r + src_offset, data[t][index]),
        #                     xytext=(0, 3),
        #                     ha='center',
        #                     va='bottom')
    x = np.arange(10, max(types) + 1, 10)
    x = np.append(x, 1)
    plt.xticks(x, x)
    # plt.xticks(x)
    plt.xlabel("Set length", fontsize=20)
    plt.ylabel("Number of occurrences", fontsize=20)
    plt.legend(loc='best', fontsize=20)
    plt.grid(axis='y', linestyle='-', linewidth=2)
    fig = plt.gcf()
    fig.set_size_inches((20, 11), forward=False)
    plt.savefig(path + r'/Stat' + str(i) + '.png', dpi=500)


    ax1 = plt.figure(1, figsize=(15, 15))
    plt.ylim(0, max(types) + 10)
    for t in types:
        plt.plot(ratio, data_src[t], label=f"{str(t)} Variables")
    plt.title(f"Minimal Source, rule len = {i}")
    plt.xticks(np.arange(1, 11, 1))
    # plt.xticks(ratio)
    plt.xlabel("Rules / Variables  Ratio", fontsize=20)
    plt.ylabel("Source size", fontsize=20)
    plt.legend(loc='best', fontsize=20)
    plt.grid(axis='y', linestyle='-', linewidth=2)
    fig = plt.gcf()
    fig.set_size_inches((20, 11), forward=False)
    plt.savefig(path + r'/Src' + str(i) + '.png', dpi=500)
    plt.show()

