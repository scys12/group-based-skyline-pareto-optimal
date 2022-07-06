from operator import itemgetter
from time import sleep
from dataset import read_txt_dataset
from main_without_preprocessing import processing
import sys


def test(dataset, group_size, top_k, algo_name, method_name):
    points = read_txt_dataset(f"data/{dataset}")
    points.sort(key=itemgetter(0))
    print(f"Total Points: {len(points)}")
    dimensional = len(points[0])
    processing(points, dimensional, top_k, group_size, algo_name, method_name)
    print("--------------------------------------------------")


if __name__ == "__main__":
    try:
        [_, dataset, group_size, top_k, algo_name, method_name] = sys.argv
    except:
        [_, dataset, group_size, top_k, algo_name] = sys.argv
        method_name = ""
    test(dataset, int(group_size), int(top_k), algo_name, method_name)
