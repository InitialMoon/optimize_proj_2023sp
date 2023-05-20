import numpy as np


def read_instance(path):
    """
    :param path: file formatted as the file teacher supported in "最优化方法大作业-2023-无等待置换流水车间调度-4道题目.txt"
    :return: a list saves all the context in the file
    """
    f = open(path, encoding='utf-8')
    txt = []
    for line in f:
        txt.append(line.strip())
    # print(txt)
    return txt


def switch_to_data(txt):
    """
    :param txt: list saves all the context in the file formatted as the file
    teacher supported in "最优化方法大作业-2023-无等待置换流水车间调度-4道题目.txt"
    :return: a 3D list, which stored all the data we need, the first dimension is
          every instance 2nd dimension store every workpiece, each third store
          step how long it need
          2D is a np
    """
    data = []
    flag = False
    for i in range(len(txt)):
        if txt[i][0] == 'i':
            flag = True
            continue
        if flag:
            flag = False
            workpiece_num_str, work_step_str = txt[i].split()
            # work_step = int(work_step_str) 这个数字我可以直接数出来，没有传输的意义
            workpiece_num = int(workpiece_num_str)
            instance = []
            for j in range(workpiece_num):
                workpiece = []
                line = txt[i + j + 1].split()
                skip = -1
                for d in line:
                    if skip > 0:
                        workpiece.append(int(d))
                    skip = -skip
                instance.append(workpiece)
            data.append(np.array(instance))

    return data
