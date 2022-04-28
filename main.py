from operator import itemgetter
from point_wise import GSkylineGroup as PointWiseGSkylineGroup
from unit_group_wise import GSkylineGroup as UnitGroupWiseGSkylineGroup
from top_k_group_dominated_groups import TopKSkylineGroupsDominatedGroups
from top_k_group_dominated_points import TopKSkylineGroupsDominatedPoints
from skyline_layers import SkylineLayer
from directed_skyline_graph import DirectedSkylineGraph

points = [
    [4, 400],
    [24, 380],
    [14, 340],
    [36, 300],
    [26, 280],
    [8, 260],
    [40, 200],
    [20, 180],
    [34, 140],
    [28, 120],
    [16, 60],
]

if __name__ == "__main__":
    points = sorted(points, key=itemgetter(0))
    skyline_layer = SkylineLayer(points)
    skyline_layer.processing()
    print("---- Skyline Layer ----")
    for x in skyline_layer.points:
        print(x)
    print(skyline_layer.layers)

    print("\n---- Skyline Graph ----")
    skyline_graph = DirectedSkylineGraph(
        skyline_layer.layers, skyline_layer.max_layer)
    skyline_graph.processing()
    for x in skyline_graph.graph:
        print(f"key {x}")
        print(f"val {skyline_graph.graph[x]}")

    print("\n---- Point Wise Algorithm ----")
    pwa_skyline_groups = PointWiseGSkylineGroup(skyline_graph.graph.copy(), 4)
    pwa_skyline_groups.processing()
    for groups_level in pwa_skyline_groups.skyline_groups:
        for group in groups_level:
            print(group)

    print("\n---- Unit Group Wise Algorithm ----")
    ugwa_skyline_groups = UnitGroupWiseGSkylineGroup(
        skyline_graph.graph.copy(), 4)
    ugwa_skyline_groups.processing()
    for group in ugwa_skyline_groups.skyline_groups:
        print(group)

    print("\n---- Top K Skyline Group Dominated Points ----")
    topkgp = TopKSkylineGroupsDominatedPoints(
        skyline_graph.graph, 6, skyline_layer.layers, 10)
    topkgp.processing()
    for group in topkgp.skyline_groups:
        print(list(group))

    print("\n---- Top K Skyline Group Dominated Groups ----")
    topkgp = TopKSkylineGroupsDominatedGroups(
        skyline_graph.graph, 3, skyline_layer.layers, 5)
    topkgp.processing()
    for group in topkgp.skyline_groups:
        print(list(group))
