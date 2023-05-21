import math
import read_instacne
import numpy as np
from numpy import random
import util


def load_data(path):
    """
    load in 2D workTime table data
    :param path: file path
    :return: a np 3D array, which store all the data we need
    """
    instances_data = read_instacne.read_instance(path)
    instances = read_instacne.switch_to_data(instances_data)  # 获取到了二维的工件时间加工表
    # print(instances)
    return instances


def random_initial(length):
    """
    随机生成一个排列作为初值
    :param length: 排列的长度
    :return: 一个排列
    """
    origin_list = []
    for i in range(length):
        origin_list.append(i)
    arr = np.array(origin_list)
    random_arr = random.permutation(arr)
    # print(random_arr)
    return random_arr


def gen_initial_val(length, data):
    """
    generate a permutation, which is initial value of SA
    :param data: workTime table
    :param length: workpiece num
    :return: a permutation, which is the index of workpiece
    """
    # return neh_initial(length, data)
    return random_initial(length)


def cal_timeline_wait(time_table, per):
    """
    根据给定的时间表和对应的加工次序返回一个2D的列表，
    这个列表里存放了与所需时间表位置对应的每一个工件在对应的机器上加工开始的时间
    :param time_table: 原始数据中的所需时间表
    :param per: 排序方式
    :return: 根据给定的时间表和对应的加工次序返回一个2D的列表，这个列表里存放了与所需时间表位置对应的每一个工件在对应的机器上加工开始的时间
    """
    starts = []
    ii = len(time_table)
    jj = len(time_table[0])
    for i in range(ii):
        starts.append([])
        for j in range(jj):
            starts[i].append(0)

    per_time_table = []
    for i in per:
        per_time_table.append(list(time_table[i]))

    time_table = per_time_table

    for i in range(len(per)):
        for j in range(jj):
            if i > 0:
                if j > 0:
                    if starts[i][j - 1] + time_table[i][j - 1] > starts[i - 1][j] + time_table[i - 1][j]:
                        starts[i][j] = starts[i][j - 1] + time_table[i][j - 1]
                    else:
                        starts[i][j] = starts[i - 1][j] + time_table[i - 1][j]
                else:
                    starts[i][j] = starts[i - 1][j] + time_table[i - 1][j]
            else:
                if j > 0:
                    starts[i][j] = time_table[i][j - 1] + starts[i][j - 1]
                else:
                    starts[i][j] = 0
    # print(starts)
    duration = starts[ii - 1][jj - 1] + time_table[ii - 1][jj - 1]
    return time_table, starts, duration


def cal_timeline_no_wait(time_table, per):
    """
    根据给定的时间表和对应的加工次序返回一个2D的列表，
    这个列表里存放了与所需时间表位置对应的每一个工件在对应的机器上加工开始的时间
    :param time_table: 原始数据中的所需时间表
    :param per: 排序方式
    :return: 根据给定的时间表和对应的加工次序返回一个2D的列表，这个列表里存放了与所需时间表位置对应的每一个工件在对应的机器上加工开始的时间
    """
    starts = []
    ii = len(time_table)
    jj = len(time_table[0])
    for i in range(ii):
        starts.append([])
        for j in range(jj):
            starts[i].append(0)

    per_time_table = []
    for i in per:
        per_time_table.append(list(time_table[i]))

    time_table = per_time_table

    for i in range(len(per)):
        for j in range(jj):
            if i > 0:
                if j > 0:
                    if starts[i][j - 1] + time_table[i][j - 1] > starts[i - 1][j] + time_table[i - 1][j]:
                        starts[i][j] = starts[i][j - 1] + time_table[i][j - 1]
                    else:
                        d = -(starts[i][j - 1] + time_table[i][j - 1]) + starts[i - 1][j] + time_table[i - 1][j]
                        for k in range(j):
                            starts[i][k] += d
                        starts[i][j] = starts[i - 1][j] + time_table[i - 1][j]
                else:
                    starts[i][j] = starts[i - 1][j] + time_table[i - 1][j]
            else:
                if j > 0:
                    starts[i][j] = time_table[i][j - 1] + starts[i][j - 1]
                else:
                    starts[i][j] = 0
    duration = starts[ii - 1][jj - 1] + time_table[ii - 1][jj - 1]
    return time_table, starts, duration


def swap_twice(x_cur):
    """
    二交换
    :param x_cur: 当前解排列
    :return: 二交换生成的一个邻域解
    """
    fir = random.randint(0, len(x_cur))
    sec = random.randint(0, len(x_cur))
    pfir = min(fir, sec)
    psec = max(fir, sec)
    if psec == len(x_cur):
        psec = len(x_cur) - 1
    s1 = list(x_cur[0: pfir])
    s2 = list(x_cur[pfir: psec + 1])
    s3 = list(x_cur[psec + 1:])
    s2.reverse()
    return s1 + s2 + s3


def swap_third(x_cur):
    """
    三交换
    :param x_cur: 当前解排列
    :return: 三交换生成的一个邻域解
    """
    fir = random.randint(0, len(x_cur))
    sec = random.randint(0, len(x_cur))
    thi = random.randint(0, len(x_cur))
    a = [fir, sec, thi]
    a.sort()
    pfir = a[0]
    psec = a[1]
    pthi = a[2]

    if pthi == len(x_cur):
        pthi = len(x_cur) - 1
    if psec == len(x_cur):
        psec = len(x_cur) - 1
    s1 = list(x_cur[0: pfir])
    s2 = list(x_cur[pfir: psec + 1])
    s3 = list(x_cur[psec + 1: pthi + 1])
    s4 = list(x_cur[pthi + 1:])
    return s1 + s3 + s2 + s4


def swap_point(x_cur):
    """
    点交换
    :param x_cur: 当前解排列
    :return: 点交换后的结果
    """
    fir = random.randint(0, len(x_cur))
    sec = random.randint(0, len(x_cur))
    temp = x_cur[fir]
    x_cur[fir] = x_cur[sec]
    x_cur[sec] = temp
    return x_cur


def get_neighbor(x_cur):
    """
    以等概率选择三种随机获取邻域解
    :param x_cur: 当前解排列
    :return: 随机生成的一个邻域解
    """
    dice = random.random()
    if dice > 0.67:
        return swap_point(x_cur)
    if dice > 0.33:
        return swap_third(x_cur)
    return swap_twice(x_cur)


def sa(time_table, cal_func):
    """
    一个完整的模拟退火主逻辑
    负责返回一个计算出的最佳的解序列,和对应的总时长
    :param time_table:
    :return:
    """
    # 模拟退火的超参
    T0 = 100000
    T = T0
    alpha = 0.99
    t_num = 10

    x_cur = gen_initial_val(time_table.shape[0], time_table)  # 生成一个初解
    time_table_cur, start_time_cur, dur_cur = cal_func(time_table, x_cur)  # 当前初解的相关参数的计算

    # 声明一组用作记录历史最小值的变量
    x_min = x_cur  # 赋一个最小值的初值，用作声明
    min_dur = dur_cur  # 设置一个最大
    time_table_min = time_table_cur
    start_time_min = start_time_cur

    same_num = 0
    k = 0

    while T > 1e-5:
        # 用作并行搜索邻域解
        time_table_neighbor, start_time_neighbor, dur_neighbor = time_table_cur, start_time_cur, dur_cur
        x_neighbor = x_cur
        # 并行搜索多个邻域解,取最小的那个作为候选邻域
        for t in range(t_num):
            x_neighbor_temp = get_neighbor(x_cur)
            time_table_neighbor_temp, start_time_neighbor_temp, dur_neighbor_temp = \
                cal_func(time_table, x_neighbor_temp)
            if t != 0:
                if dur_neighbor > dur_neighbor_temp:
                    x_neighbor = x_neighbor_temp
                    time_table_neighbor, start_time_neighbor, dur_neighbor = \
                        time_table_neighbor_temp, start_time_neighbor_temp, dur_neighbor_temp
            else:
                x_neighbor = x_neighbor_temp
                time_table_neighbor, start_time_neighbor, dur_cur_neighbor = \
                    time_table_neighbor_temp, start_time_neighbor_temp, dur_neighbor_temp

        delta_e = dur_cur - dur_neighbor
        if min_dur > dur_neighbor:
            min_dur = dur_neighbor
            x_min = x_neighbor
            time_table_min = time_table_neighbor
            start_time_min = start_time_neighbor
            continue

        if delta_e < 0:
            same_num = 0
            dur_cur = dur_neighbor
            time_table_cur = time_table_neighbor
            start_time_cur = start_time_neighbor
        else:
            dice = random.random()
            if pow(math.e, delta_e / T) > dice:
                dur_cur = dur_neighbor
                time_table_cur = time_table_neighbor
                start_time_cur = start_time_neighbor
            else:
                same_num += 1
        if same_num == 30:
            break

        T = T * alpha
        k += 1
    print("after {} epochs, T = {}, min duration = {}".format(k, T, min_dur))
    return x_min, min_dur, time_table_min, start_time_min


def mian_logic(in_path, out_path, cal_func):
    """
    等待和无等待实验的相同逻辑部分
    :param in_path: 数据来源路径
    :param out_path: 输出路径中间名
    :param cal_func: 是调用无等待计算方式还是调用等待计算方式
    """
    all_tests = load_data(in_path)
    repeat_num = 10  # 每组数据重复实验的次数
    instance = 0
    out = open("../out/" + out_path + "/data/sequence_duration.txt", "w")
    for test in all_tests:
        print("instance" + str(instance) + "\n")
        out.write("instance " + str(instance) + "\n")
        x, y, ttm, stm = sa(test, cal_func)
        out.write(str(x))
        out.write('\t')
        out.write(str(y))
        out.write('\n')

        for i in range(repeat_num - 1):
            xi, yi, ttmi, stmi = sa(test, cal_func)
            out.write(str(xi))
            out.write('\t')
            out.write(str(yi))
            out.write('\n')
            if yi < y:
                x = xi
                y = yi
                ttm = ttmi
                stm = stmi
        out.write("min result\n")
        out.write(str(x))
        out.write('\t')
        out.write(str(y))
        out.write('\n')
        out.write('\n')
        util.draw_result(ttm, stm, "../out/" + out_path + "/img/" + str(instance) + ".png")
        instance += 1


def run_no_wait():
    """
    进行无等待算法的运行实验
    """
    print("no wait")
    mian_logic("../no_wait.txt", "no_wait", cal_timeline_no_wait)


def run_wait():
    """
    进行等待算法的运行实验
    """
    print("wait")
    mian_logic("../wait.txt", "wait", cal_timeline_wait)


if __name__ == "__main__":
    # run_wait()
    run_no_wait()
