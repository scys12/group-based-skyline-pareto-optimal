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
from memory_profiler import memory_usage


def get_user_input():
    try:
        dataset = str(
            input(
                "Input dataset name (default: hotel_2.txt): \n",
            )
            or "hotel_2.txt"
        )
        points = read_txt_dataset(f"data/{dataset}")
        print(f"Total Points: {len(points)}")
        points.sort(key=itemgetter(0))

        dimensional = len(points[0])
        top_k = 3

        group_size = int(input("Input size of a group (default: 2): \n") or 2)
        algo_name = str(
            input(
                "Choose Algorithm: \n(a)PWA = Point Wise Algorithm, \n(b)UWA = Unit Group Wise Algorithm, \n(c)TOPKGP = Top K Skyline Group Dominated Points, \n(d)TOPKGG = Top K Skyline Group Dominated Points: \n"
            )
            or "pwa"
        )

        method_name = ""
        if algo_name.lower() == "topkgp" or algo_name.lower() == "topkgg":
            top_k = int(input("Input Top K data (default: 3): \n") or 3)

            if algo_name.lower() == "topkgg":
                method_name = str(
                    input(
                        "Choose Method For TopKGG: \n(a)PA = Pruning Algorithm \n(b) CA = Counting Algorithm: \n"
                        or "pa"
                    )
                )

        return points, dimensional, top_k, group_size, algo_name.lower(), method_name
    except KeyboardInterrupt:
        print("\nExit Program...")
        exit(0)


def run_unit_wise_algo(ugwa_skyline_groups, top_k):
    res = ugwa_skyline_groups.processing()
    skyline_groups = chain(ugwa_skyline_groups.skyline_groups, res)
    total = 0
    groups = []

    for group in skyline_groups:
        total += 1
        if total > top_k:
            continue
        groups.append(group)
    return groups, total


def run_point_wise_algo(pwa_skyline_groups, top_k):
    res = pwa_skyline_groups.processing()
    skyline_groups = chain(pwa_skyline_groups.skyline_groups, res)
    total = 0
    groups = []

    for group in skyline_groups:
        total += 1
        if total > top_k:
            continue
        groups.append(group)
    return groups, total


def processing(points, dimensional, top_k, group_size, algo_name, method_name):
    memory_initial = psutil.Process(os.getpid()).memory_info().rss / 1024**2
    print("\n---- Skyline Layer ----")
    skyline_layer = SkylineLayer(points, dimensional, group_size)
    _, skyline_layer_time = benchmark_time(skyline_layer.processing)
    print(f"Skyline Layer Time Elapsed: {skyline_layer_time:f} s\n")
    skyline_layer_memory = (
        psutil.Process(os.getpid()).memory_info().rss / 1024**2 - memory_initial
    )
    print(f"Total Memory : {skyline_layer_memory} MB\n")
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
        pwa_skyline_groups, pwa_preprocessing_time = benchmark_time(
            PointWiseGSkylineGroup,
            skyline_graph.graph.copy(),
            group_size,
        )
        print(f"Prepocessing Time Elapsed: {pwa_preprocessing_time:f} s\n")

        initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        point_group_wise_memory, (
            (groups, total_group),
            pwa_processing_time,
        ) = memory_usage(
            proc=(benchmark_time, (run_point_wise_algo, pwa_skyline_groups, top_k)),
            retval=True,
        )
        print(f"Processing Time Elapsed: {(pwa_processing_time):f} s\n")
        print(f"Total Memory : {max(point_group_wise_memory) - initial_memory} MB\n")
        print(f"Total G-Skyline Group (size: {group_size}): {total_group}\n")
        for group in groups:
            print(group)
    elif algo_name == "uwa":
        print("\n---- Unit Group Wise Algorithm ----")
        ugwa_skyline_groups, ugwa_preprocessing_time = benchmark_time(
            UnitGroupWiseGSkylineGroup,
            skyline_graph.graph.copy(),
            group_size,
        )
        print(f"Prepocessing Time Elapsed: {ugwa_preprocessing_time:f} s\n")

        initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        unit_group_wise_memory, (
            (groups, total_group),
            ugwa_processing_time,
        ) = memory_usage(
            proc=(benchmark_time, (run_unit_wise_algo, ugwa_skyline_groups, top_k)),
            retval=True,
        )

        print(f"Processing Time Elapsed: {(ugwa_processing_time):f} s\n")
        print(f"Total Memory : {max(unit_group_wise_memory)-initial_memory} MB\n")
        print(f"Total G-Skyline Group (size: {group_size}): {total_group}\n")
        for group in groups:
            print(group)
    elif algo_name == "topkgp":
        print("\n---- Top K Skyline Group Dominated Points ----")
        topkgp, topkgp_preprocessing_time = benchmark_time(
            TopKSkylineGroupsDominatedPoints,
            skyline_graph.graph,
            group_size,
            skyline_layer.layers,
            top_k,
        )
        print(f"Prepocessing Time Elapsed: {topkgp_preprocessing_time:f} s\n")

        initial_topkgp_memory = (
            psutil.Process(os.getpid()).memory_info().rss / 1024**2
        )
        _, topkgp_processing_time = benchmark_time(topkgp.processing)
        topkgp_memory = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        print(f"Processing Time Elapsed: {(topkgp_processing_time):f} s\n")
        print(f"Total Memory : {topkgp_memory-initial_topkgp_memory} MB\n")
        for group in topkgp.skyline_groups:
            print(list(group))

    elif algo_name == "topkgg":
        print("\n---- Top K Skyline Group Dominated Groups ----")
        topkgg, topkgg_preprocessing_time = benchmark_time(
            TopKSkylineGroupsDominatedGroups,
            skyline_graph.graph,
            group_size,
            skyline_layer.layers,
            top_k,
            method_name.upper(),
        )
        print(f"Prepocessing Time Elapsed: {topkgg_preprocessing_time:f} s\n")

        topkgg_memory = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        _, topkgg_processing_time = benchmark_time(topkgg.processing)
        topkgg_memory = (
            psutil.Process(os.getpid()).memory_info().rss / 1024**2 - topkgg_memory
        )
        print(f"Processing Time Elapsed: {(topkgg_processing_time):f} s\n")
        for group in topkgg.skyline_groups:
            print(list(group))
        print(f"Total Memory : {topkgg_memory} MB\n")


if __name__ == "__main__":
    processing(*get_user_input())
