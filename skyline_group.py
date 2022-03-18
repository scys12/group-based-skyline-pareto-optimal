from operator import itemgetter
from skyline_layers import points, SkylineLayer
from directed_skyline_graph import SkylineGraph


class SETree:
    def __init__(self, points, level, dsg, point_index=-1) -> None:
        self.points = points
        self.level = level
        self.children = []
        self.tail_sets = []
        self.point_index = point_index
        self.add_tail_sets(dsg)

    def add_tail_sets(self, dsg):
        dsg_keys = list(dsg.keys())
        self.tail_sets = dsg_keys[self.point_index+1:]

    def __str__(self):
        return str({
            'points': self.points,
            'level': self.level,
            'point_index': self.point_index,
        })


class GSkylineGroup:
    def __init__(self, dsg, group_size) -> None:
        self.dsg = dsg
        self.group_size = group_size
        self.unit_group = {}
        self.skyline_groups = []

    def create_unit_group(self):
        for point_key in list(self.dsg):
            unit_group = self.dsg[point_key].parents + \
                [point_key]
            if len(unit_group) >= self.group_size:
                del self.dsg[point_key]
            else:
                self.unit_group[point_key] = unit_group

    def verificate_g_skyline_group(self, group):
        points = set()
        size = len(group)
        for point in group:
            points.update(self.unit_group[point])
        total = len({point for point in points})
        return total == size

    def processing(self):
        self.create_unit_group()
        root = SETree([], 0, self.dsg)
        self.skyline_groups = [
            [root]
        ]

        for i in range(1, self.group_size+1):
            for group in self.skyline_groups[i-1]:
                children_set = set()
                max_layer_group = 0
                for point in group.points:
                    children_set.update(self.dsg[point].children)
                    max_layer_group = self.dsg[point].layer_index if max_layer_group < self.dsg[point].layer_index else max_layer_group
                for point in list(group.tail_sets):
                    if point not in children_set and not all(p in group.points for p in self.dsg[point].parents):
                        group.tail_sets.remove(point)
                    elif self.dsg[point].layer_index - max_layer_group >= 2:
                        group.tail_sets.remove(point)
                for point in group.tail_sets:
                    candidate_group = group.points.copy()
                    candidate_group.append(point)
                    if self.verificate_g_skyline_group(candidate_group):
                        point_index = group.point_index if group.point_index > self.dsg[
                            point].point_index else self.dsg[point].point_index
                        sg = SETree(candidate_group, i, self.dsg, point_index)
                        if len(self.skyline_groups) == i:
                            self.skyline_groups.append([])
                        self.skyline_groups[i].append(sg)


if __name__ == "__main__":
    points = sorted(points, key=itemgetter(0))
    skyline_layer = SkylineLayer(points)
    skyline_layer.processing()
    skyline_graph = SkylineGraph(skyline_layer.layers, skyline_layer.max_layer)
    skyline_graph.processing()
    sg = GSkylineGroup(
        skyline_graph.graph, skyline_graph.max_layer)
    sg.processing()
    for i in sg.skyline_groups:
        for j in i:
            print(j)
