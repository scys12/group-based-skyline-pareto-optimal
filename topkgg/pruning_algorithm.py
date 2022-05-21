from itertools import product
from util import RepresentativeSkylineGraph


class PruningAlgorithm:
    def __init__(self, dsg):
        self.dsg = dsg

    def count_total_points_dominated(self, representative_graph, group):
        total = 1
        for point in group:
            total *= representative_graph.graph[point]['weight']
        return total

    def get_number_of_groups_dominated_group(self, group):
        rsg = RepresentativeSkylineGraph(self.dsg, group)
        child_groups = [rsg.graph[group[x]]['children_set']
                        for x in range(len(group))]
        total_dg = 0
        existing_child_group = set()
        for child_group in product(*child_groups):
            if len(set(child_group)) == len(group) and frozenset(child_group) not in existing_child_group:
                existing_child_group.add(frozenset(child_group))
                total_dg += self.count_total_points_dominated(rsg, child_group)
        return total_dg-1
