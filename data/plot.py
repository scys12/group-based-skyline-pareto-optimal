import pandas
import seaborn as sns
import matplotlib.pyplot as plt
from math import log10, floor


def format_func_x(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else floor(log10(abs(value)) / 3)
    print(num_thousands)
    print(value)
    return value


def format_func_y(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else floor(log10(abs(value)) / 3)
    value = round(value / 1000**num_thousands, 2)
    return f"{value:g}" + " KMBTPEZY"[num_thousands]


def plot(filename):
    pd = pandas.read_csv(filename, sep=" ", header=None)
    pd = pd.drop_duplicates()
    # pd.plot(x=0, y=1, kind="scatter")
    sns.pairplot(pd, plot_kws={"s": 3})
    plt.savefig(f"{filename}.png")


# plot("anti_2_1000.txt")


def draw_chart():
    fig, ax = plt.subplots()
    plt.plot(
        [
            1000,
            10000,
            100000,
            1000000,
            10000000,
        ],
        [
            0.000089,
            0.000105,
            0.000118,
            0.000121,
            0.000156,
        ],
    )
    # ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func_x))
    # ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func_y))
    plt.show()


draw_chart()
