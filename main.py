from itertools import chain
from operator import itemgetter
import os
import psutil
from util import benchmark_time
from dataset import read_txt_dataset
from pwise.point_wise import PointWise as PointWiseGSkylineGroup
from uwise.unit_group_wise import UnitGroupWise as UnitGroupWiseGSkylineGroup
from topkgg.top_k_group_dominated_groups import TopKSkylineGroupsDominatedGroups
from topkgp.top_k_group_dominated_points import TopKSkylineGroupsDominatedPoints
from skyline_layers import SkylineLayer
from directed_skyline_graph import DirectedSkylineGraph


def get_user_input():
    try:
        dataset = str(
            input(
                "Input dataset name (default: hotel_2.txt): \n",
            )
            or "inde_3_100000.txt"
        )
        points = read_txt_dataset(f"data/{dataset}")
        print(f"Total Points: {len(points)}")
        points.sort(key=itemgetter(0))

        dimensional = len(points[0])
        top_k = 3

        group_size = int(input("Input size of a group (default: 2): \n") or 3)
        algo_name = str(
            input(
                "Choose Algorithm: (a)PWA = Point Wise Algorithm, (b)UWA = Unit Group Wise Algorithm, (c)TOPKGP = Top K Skyline Group Dominated Points, (d)TOPKGG = Top K Skyline Group Dominated Points: \n"
            )
            or "topkgg"
        )

        method_name = ""
        if algo_name.lower() == "topkgp" or algo_name.lower() == "topkgg":
            top_k = int(input("Input Top K data (default: 3): \n") or 3)

            if algo_name.lower() == "topkgg":
                method_name = str(
                    input(
                        "Choose Method For TopKGG: (a)PA = Pruning Algorithm (b) CA = Counting Algorithm: \n"
                        or "pa"
                    )
                )

        return points, dimensional, top_k, group_size, algo_name.lower(), method_name
    except KeyboardInterrupt:
        print("\nExit Program...")
        exit(0)


def run_unit_wise_algo(ugwa_skyline_groups, top_k, group_size):
    res = ugwa_skyline_groups.processing()
    skyline_groups = chain(ugwa_skyline_groups.skyline_groups, res)
    total = 0
    for group in skyline_groups:
        total += 1
        if total > top_k:
            continue
        print(group)
    print(f"\nTotal G-Skyline Group (size: {group_size}): {total}\n")


def run_point_wise_algo(pwa_skyline_groups, top_k, group_size):
    res = pwa_skyline_groups.processing()
    skyline_groups = chain(pwa_skyline_groups.skyline_groups, res)
    total = 0
    for group in skyline_groups:
        total += 1
        if total > top_k:
            continue
        print(group)
    print(f"\nTotal G-Skyline Group (size: {group_size}): {total}\n")


def processing(points, dimensional, top_k, group_size, algo_name, method_name):
    print("\n---- Skyline Layer ----")
    skyline_layer = SkylineLayer(points, dimensional, group_size)
    skyline_layer.processing()
    for x in skyline_layer.layers:
        print(f"layer {x}: Total Points {len(skyline_layer.layers[x])}")

    print("\n---- Skyline Graph ----")
    skyline_graph = DirectedSkylineGraph(
        skyline_layer.layers, len(skyline_layer.layers)
    )
    skyline_graph.processing()
    print(f"Length Directed Skyline Graph: {len(skyline_graph.graph)}")

    if algo_name == "pwa":
        print("\n---- Point Wise Algorithm ----")
        pwa_skyline_groups, _ = benchmark_time(
            PointWiseGSkylineGroup,
            "Preprocessing",
            skyline_graph.graph.copy(),
            group_size,
        )
        benchmark_time(
            run_point_wise_algo, "Processing", pwa_skyline_groups, top_k, group_size
        )
    elif algo_name == "uwa":
        print("\n---- Unit Group Wise Algorithm ----")
        ugwa_skyline_groups, _ = benchmark_time(
            UnitGroupWiseGSkylineGroup,
            "Preprocessing",
            skyline_graph.graph.copy(),
            group_size,
        )
        benchmark_time(
            run_unit_wise_algo, "Processing", ugwa_skyline_groups, top_k, group_size
        )
    elif algo_name == "topkgp":
        print("\n---- Top K Skyline Group Dominated Points ----")
        topkgp = TopKSkylineGroupsDominatedPoints(
            skyline_graph.graph, group_size, skyline_layer.layers, top_k
        )
        benchmark_time(topkgp.processing, "Processing")
        for group in topkgp.skyline_groups:
            print(list(group))
    elif algo_name == "topkgg":
        print("\n---- Top K Skyline Group Dominated Groups ----")
        topkgp = TopKSkylineGroupsDominatedGroups(
            skyline_graph.graph,
            group_size,
            skyline_layer.layers,
            top_k,
            method_name.upper(),
        )
        benchmark_time(topkgp.processing, "Processing")
        for group in topkgp.skyline_groups:
            print(list(group))

    print(
        "Memory usage: "
        + str(psutil.Process(os.getpid()).memory_info().rss // 1024**2)
        + " mb"
    )


if __name__ == "__main__":
    processing(get_user_input())
