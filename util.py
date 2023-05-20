import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# CopyRight 知乎 我就要吃米饭 https://zhuanlan.zhihu.com/p/106787569
def draw_result(add, left, out_path):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    m = range(len(add))
    n = range(len(add[0]))
    color = ['b', 'g', 'r', 'y', 'c', 'm', 'k', 'pink', 'royalblue', 'lime', 'gold', 'lightseagreen', 'darkred', 'orangered', 'sandybrown']

    # 画布设置，大小与分辨率
    plt.figure(figsize=(20, 8), dpi=80)
    # barh-柱状图换向，循坏迭代-层叠效果
    for i in m:
        for j in n:
            plt.barh(m[i] + 1, add[i][j], left=left[i][j], color=color[j])
    plt.title("流水加工甘特图")
    labels = [''] * len(add[0])
    for f in n:
        labels[f] = "工序%d" % (f + 1)
    # 图例绘制
    patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(add[0]))]
    plt.legend(handles=patches, loc=4)
    # XY轴标签
    plt.xlabel("加工时间单位")
    plt.ylabel("工件加工优先级")
    plt.savefig(out_path)


if __name__ == "__main__":
    # dur是每一个工件在不同的工序上加工所需要的时间,这里是3个工件
    dur = [[14, 6, 23], [18, 7, 35], [10, 30, 21], [18, 5, 30], [10, 25, 20], [12, 35, 20], [10, 32, 17], [10, 20, 16]]
    # start是每一个工件开始再第i个工序上开始加工的时间
    start = [[0, 14, 20], [14, 32, 43], [32, 42, 78], [42, 72, 99], [60, 77, 129], [70, 102, 149], [82, 137, 169], [92, 169, 189]]
    draw_result(dur, start)
