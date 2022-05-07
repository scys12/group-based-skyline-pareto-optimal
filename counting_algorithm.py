from itertools import combinations_with_replacement
from math import comb
from util import BipartiteGraph, MaximumBipartiteMatching, MaximumBipartiteMatchingGraph, create_subset
from collections import Counter


class CountingAlgorithm:
    def __init__(self, dsg, group_size):
        self.dsg = dsg
        self.group_size = group_size
        self.mock_group = [x for x in range(self.group_size)]
        self.existing_types = {}

        self.group_types = []
        self.processing_mock_group(self.mock_group, self.group_size)

    def build_all_group_types(self, group_subset, children_set, group):
        group_types = dict()
        for g in group_subset:
            s = set(g)
            group_types[tuple(s)] = 0
        for point in children_set:
            parents = self.dsg[point].parents
            point_parents = tuple(set(group).intersection(set(parents)))
            if point_parents in group_types:
                group_types[point_parents] += 1
        return group_types

    def count_total_points_dominated(self, mock_group, subset, group_types_dict):
        total = 1
        values = list(group_types_dict.values())
        for gt in mock_group:
            total_g = values[gt[0]]
            if len(subset[gt[0]]) == 1:
                total_g += 1
            total *= comb(total_g, gt[1])
        return total

    def get_existing_group_type(self, group_types_dict):
        group_type = [[] for _ in range(self.group_size)]
        count = -1
        for g in group_types_dict.keys():
            group_type[len(g)-1].append(group_types_dict[g])
        for ex_type in self.existing_types.keys():
            is_existing = True
            for i in range(self.group_size):
                if Counter(ex_type[i]) != Counter(group_type[i]):
                    is_existing = False
                    break
            if is_existing:
                count = self.existing_types[ex_type]
                break

        return count, group_type

    def add_to_existing_type(self, group_type, count):
        self.existing_types[tuple(tuple(x) for x in group_type)] = count

    def get_number_of_groups_dominated_group(self, group):
        children_set = set()
        for point in group:
            cs = [point] + self.dsg[point].children
            children_set.update(cs)
        subset = create_subset(group, 1, len(group))
        group_types_dict = self.build_all_group_types(
            subset, children_set, group)
        count = 0
        count, group_type = self.get_existing_group_type(group_types_dict)
        if count == -1:
            count = 0
            for gt in self.group_types:
                count += self.count_total_points_dominated(
                    gt, subset, group_types_dict)
            self.add_to_existing_type(group_type, count)
        return count - 1

    def is_bipartite(self, group_type, group):
        bipartite_graph = MaximumBipartiteMatchingGraph(group_type, group)
        is_bipartite = True
        if bipartite_graph.max_matching() != len(group):
            is_bipartite = False
        return is_bipartite

    def processing_mock_group(self, group, group_size):
        subset = create_subset(group, 1, len(group))
        for g in combinations_with_replacement(subset, group_size):
            if self.is_bipartite(g, group):
                self.group_types.append(
                    [(subset.index(x), g.count(x)) for x in set(g)])
