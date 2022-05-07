from math import comb
from util import BipartiteGraph, MaximumBipartiteMatching, create_subset
from collections import Counter


class CountingAlgorithm:
    def __init__(self, dsg, group_size):
        self.dsg = dsg
        self.group_size = group_size
        self.mock_group = [(x, x) for x in range(self.group_size)]
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

    def count_total_points_dominated(self, mock_group, group, group_types_dict):
        total = 1
        ctr_group = Counter(mock_group)
        # (((20, 180),), ((8, 260),), ((16, 60),)))
        # (((2, 2),), ((1, 1),), ((0, 0),))
        for g in ctr_group.keys():
            real_g = []
            for i in range(len(g)):
                real_g.append(group[g[i][0]])
            real_g = tuple(real_g)
            total_g = group_types_dict[tuple(set(real_g))]
            if len(g) == 1:
                total_g += 1
            total *= comb(total_g, ctr_group[g])
        return total

    def power(self, group_size, candidate_group, total):
        if total == 0:
            return None
        temp_group = self.power(group_size, candidate_group, int(total/2))

        if total % 2:
            iteration = int(total/2)
        else:
            iteration = total

        result_group = None if temp_group is None else self.pairing_group(
            iteration, group_size, temp_group)

        if total % 2 == 0:
            return result_group
        else:
            return candidate_group if result_group is None else self.pairing_group(total, group_size, candidate_group, result_group)

    def extract_groups(self, group, k):
        if isinstance(group[k][0], int):
            g = list(group[k][1])
        else:
            g = [group[k]]
        return g

    def pairing_group(self, iteration, group_size, group_one, group_two=None):
        candidate_groups = []
        ctr_groups = []
        if group_two is None:
            group_two = group_one.copy()
        for j in range(len(group_one)):
            for k in range(len(group_two)):
                g = self.extract_groups(group_two, k)
                g2 = self.extract_groups(
                    group_one, j)
                g.extend(g2)
                if iteration == group_size:
                    ctr = Counter(g)
                    if ctr not in ctr_groups:
                        candidate_groups.append((iteration, tuple(g)))
                        ctr_groups.append(ctr)
                else:
                    candidate_groups.append((iteration, tuple(g)))
        return candidate_groups

    def get_number_of_groups_dominated_group(self, group):
        children_set = set()
        count = 0
        for point in group:
            cs = [point] + self.dsg[point].children
            children_set.update(cs)
        subset = create_subset(group, 1, len(group))
        group_types_dict = self.build_all_group_types(
            subset, children_set, group)
        for gt in self.group_types:
            count += self.count_total_points_dominated(
                gt[1], group, group_types_dict)
        print(count - 1)
        return count - 1

    def processing_mock_group(self, group, group_size):
        subset = create_subset(group, 1, len(group))
        self.group_types = self.power(group_size, list(
            subset), group_size)
        for gt in list(self.group_types):
            bipartite_graph = BipartiteGraph(gt[1], group)
            max_bipartite = MaximumBipartiteMatching()
            if max_bipartite.max_matching(bipartite_graph) != len(group):
                self.group_types.remove(gt)
                continue
