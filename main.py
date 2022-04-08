from operator import itemgetter
from topkgp import TopKSkylineGroupsDominatedPoints
from skyline_layers import SkylineLayer
from directed_skyline_graph import SkylineGraph

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
    skyline_graph = SkylineGraph(skyline_layer.layers, skyline_layer.max_layer)
    skyline_graph.processing()
    for x in skyline_graph.graph:
        print(f"key {x}")
        print(f"val {skyline_graph.graph[x]}")

    print("\n---- Top K Skyline Group ----")
    topkgp = TopKSkylineGroupsDominatedPoints(
        skyline_graph.graph, 3, skyline_layer.layers, 4)
    topkgp.processing()
    for group in topkgp.skyline_groups:
        print(group)
