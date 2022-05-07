from operator import itemgetter
from util import benchmark_time
from dataset import *
from point_wise import GSkylineGroup as PointWiseGSkylineGroup
from unit_group_wise import GSkylineGroup as UnitGroupWiseGSkylineGroup
from top_k_group_dominated_groups import TopKSkylineGroupsDominatedGroups
from top_k_group_dominated_points import TopKSkylineGroupsDominatedPoints
from skyline_layers import SkylineLayer
from directed_skyline_graph import DirectedSkylineGraph

if __name__ == "__main__":
    # points = read_nba_dataset('data/nba.csv')
    points = read_txt_dataset('data/corr_4.txt')
    points = sorted(points, key=itemgetter(0))
    group_size = 5
    top_k = 5
    dimensional = len(points[0])

    print("---- Skyline Layer ----")
    skyline_layer = SkylineLayer(points, dimensional, group_size)
    skyline_layer.processing()
    for x in skyline_layer.layers:
        print(f"layer {x}: {skyline_layer.layers[x]}")

    print("\n---- Skyline Graph ----")
    skyline_graph = DirectedSkylineGraph(
        skyline_layer.layers, len(skyline_layer.layers))
    skyline_graph.processing()
    for x in skyline_graph.graph:
        print(f"point {x}")
        print(f"graph {skyline_graph.graph[x]}")

    # print("\n---- Point Wise Algorithm ----")
    # pwa_skyline_groups = PointWiseGSkylineGroup(
    #     skyline_graph.graph.copy(), group_size)
    # benchmark_time(pwa_skyline_groups.processing)
    # print(
    #     f"Total G-Skyline Group: {len(pwa_skyline_groups.skyline_groups[group_size])}\n")
    # total = 0
    # for group in pwa_skyline_groups.skyline_groups[group_size]:
    #     print(group.points)
    #     total += 1
    #     if total == top_k:
    #         break

    # print("\n---- Unit Group Wise Algorithm ----")
    # ugwa_skyline_groups = UnitGroupWiseGSkylineGroup(
    #     skyline_graph.graph.copy(), group_size)
    # benchmark_time(ugwa_skyline_groups.processing)
    # print(
    #     f"Total G-Skyline Group: {len(pwa_skyline_groups.skyline_groups[group_size])}\n")
    # total = 0
    # for group in ugwa_skyline_groups.skyline_groups:
    #     print(group.points)
    #     total += 1
    #     if total == top_k:
    #         break

    # print("\n---- Top K Skyline Group Dominated Points ----")
    # topkgp = TopKSkylineGroupsDominatedPoints(
    #     skyline_graph.graph, group_size, skyline_layer.layers, top_k)
    # benchmark_time(topkgp.processing)
    # for group in topkgp.skyline_groups:
    #     print(list(group))

    topkgp = TopKSkylineGroupsDominatedGroups(
        skyline_graph.graph, group_size, skyline_layer.layers, top_k)
    print("\n---- Top K Skyline Group Dominated Groups ----")
    benchmark_time(topkgp.processing)
    for group in topkgp.skyline_groups:
        print(list(group))
