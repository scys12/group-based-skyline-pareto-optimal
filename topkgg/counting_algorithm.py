from itertools import combinations_with_replacement, filterfalse
from math import comb
from util import MaximumBipartiteMatchingGraph, create_subset
from collections import Counter


class CountingAlgorithm:
    def __init__(self, dsg, group_size):
        self.dsg = dsg
        self.group_size = group_size
        self.mock_group = [x for x in range(self.group_size)]
        self.existing_group_types = {}
        self.point_types_occurence = []
        self.processing_mock_group(self.mock_group, self.group_size)

    def build_all_point_types(self, point_types, children_set, group):
        point_types_dict = dict()
        for point_type in point_types:
            point_type_set = set(point_type)
            point_types_dict[tuple(point_type_set)] = 0
        for point in children_set:
            parents = self.dsg[point]["parents"]
            parents_points = tuple(set(group).intersection(set(parents)))
            if parents_points in point_types_dict:
                point_types_dict[parents_points] += 1
        return point_types_dict

    def count_total_points_dominated(self, mock_group, point_types, point_types_dict):
        total = 1
        values = list(point_types_dict.values())
        for point_type_mock in mock_group:
            point_type_val = values[point_type_mock[0]]
            if len(point_types[point_type_mock[0]]) == 1:
                point_type_val += 1
            total *= comb(point_type_val, point_type_mock[1])
        return total

    def get_existing_group_type(self, point_types_dict):
        group_type = [[] for _ in range(self.group_size)]
        count = -1
        for g in point_types_dict:
            group_type[len(g) - 1].append(point_types_dict[g])
        for ex_type in self.existing_group_types:
            is_existing = True
            for i in range(self.group_size):
                if Counter(ex_type[i]) != Counter(group_type[i]):
                    is_existing = False
                    break
            if is_existing:
                count = self.existing_group_types[ex_type]
                break

        return count, group_type

    def add_to_existing_type(self, group_type, count):
        self.existing_group_types[tuple(tuple(x) for x in group_type)] = count

    def get_number_of_groups_dominated_group(self, group):
        children_set = set()
        for point in group:
            cs = [point] + self.dsg[point]["children"]
            children_set.update(cs)
        point_types = create_subset(group, 1, len(group))
        point_types_dict = self.build_all_point_types(point_types, children_set, group)
        count, group_type = self.get_existing_group_type(point_types_dict)
        if count == -1:
            count = 0
            for point_type in self.point_types_occurence:
                count += self.count_total_points_dominated(
                    point_type, point_types, point_types_dict
                )
            self.add_to_existing_type(group_type, count)
        return count - 1

    def is_bipartite(self, group_type, group):
        bipartite_graph = MaximumBipartiteMatchingGraph(group_type, group)
        is_bipartite = True
        if bipartite_graph.max_matching() != len(group):
            is_bipartite = False
        return is_bipartite

    def processing_mock_group(self, group, group_size):
        point_types = create_subset(group, 1, len(group))
        for group_type in self.construct_group_types_from_subset(
            group, point_types, group_size
        ):
            self.point_types_occurence.append(
                [
                    (point_types.index(point), group_type.count(point))
                    for point in set(group_type)
                ]
            )

    def construct_group_types_from_subset(self, group, point_types, group_size):
        return filterfalse(
            lambda group_type: not self.is_bipartite(group_type, group),
            combinations_with_replacement(point_types, group_size),
        )
