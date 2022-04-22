from util import BipartiteGraph, MaximumBipartiteMatching, create_subset
from collections import Counter


class CountingAlgorithm:
    def __init__(self, dsg, group, group_size):
        self.dsg = dsg
        self.group = group
        self.group_size = group_size

    def build_all_group_types(self, children_set, group):
        subset = create_subset(group, 1, len(group))
        group_types = dict()
        for g in subset:
            s = set(g)
            group_types[tuple(s)] = 0
        for point in children_set:
            parents = self.dsg[point].parents
            point_parents = tuple(set(group).intersection(set(parents)))
            if point_parents in group_types:
                group_types[point_parents] += 1
        return group_types

    def count_total_points_dominated(self, group, group_type, total_group, total_group_types):
        total = total_group
        if len(group_type) == 1:
            total_group_types += 1
        group_set = set(group)
        len_before = len(group_set)
        group_set.add(group_type)
        len_after = len(group_set)
        if len_after > len_before:
            total *= total_group_types
        return total

    def build_candidate_groups(self, group_types_dict, group_size):
        group_types = list(group_types_dict.keys())
        candidate_groups = group_types.copy()
        for i in range(group_size-1):
            temp_groups = []
            for gt in group_types:
                temp_group = []
                for k in range(len(candidate_groups)):
                    if isinstance(candidate_groups[k][0], int):
                        total = candidate_groups[k][0]
                        g = list(candidate_groups[k][1])
                    else:
                        g = list(candidate_groups[k])
                        total = group_types_dict[candidate_groups[k]]
                        if len(candidate_groups[k]) == 1:
                            total += 1
                    if i == 0:
                        g = [candidate_groups[k]]

                    total = self.count_total_points_dominated(
                        g, gt, total, group_types_dict[gt])
                    g.append(gt)
                    if i == group_size - 2:
                        if not any([Counter(g) == Counter(y[1]) for y in temp_group]):
                            temp_group.append((total, tuple(g)))
                    else:
                        temp_group.append((total, tuple(g)))

                if i == group_size - 2:
                    temp_group = [x for x in temp_group if not any(
                        [set(y[1]).issubset(set(x[1])) for y in temp_groups])]
                temp_groups.extend(temp_group)
            candidate_groups = temp_groups
        return candidate_groups

    def get_number_of_groups_dominated_group(self, group, group_size):
        children_set = set()
        count = 0
        for point in group:
            cs = [point] + self.dsg[point].children
            children_set.update(cs)
        group_types_dict = self.build_all_group_types(children_set, group)
        group_types = self.build_candidate_groups(group_types_dict, group_size)
        for gt in list(group_types):
            bipartite_graph = BipartiteGraph(gt[1], group)
            max_bipartite = MaximumBipartiteMatching()
            if max_bipartite.max_matching(bipartite_graph) != len(group):
                group_types.remove(gt)
                continue
            count += gt[0]
        return count - 1
