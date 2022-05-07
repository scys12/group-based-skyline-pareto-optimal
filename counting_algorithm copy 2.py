from itertools import combinations_with_replacement
from math import comb
from util import MaximumBipartiteMatchingGraph, create_subset
from collections import Counter


class CountingAlgorithm:
    def __init__(self, dsg, group_size):
        self.dsg = dsg
        self.group_size = group_size
        self.existing_types = {}
        # self.total_number = self.get_total_number()
        # print(self.total_number)

    def get_total_number(self):
        mock_group = [(x, x) for x in range(self.group_size)]
        subset = create_subset(mock_group, 1, len(mock_group))
        mock_group_types_dict = Counter(subset)
        return len(list(self.combinations_with_replacements(subset, self.group_size, mock_group, mock_group_types_dict)))

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

    def count_total_points_dominated(self, group, group_types_dict):
        total = 1
        for g in set(group):
            total_g = group_types_dict[g]
            if len(g) == 1:
                total_g += 1
            total *= comb(total_g, group.count(g))
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

    def is_bipartite(self, group_type, group):
        bipartite_graph = MaximumBipartiteMatchingGraph(group_type, group)
        is_bipartite = True
        if bipartite_graph.max_matching() != len(group):
            is_bipartite = False
        return is_bipartite

    def combinations_with_replacement(self, iterable, r, group, group_types_dict):
        pool = tuple(iterable)
        n = len(pool)
        if not n and r:
            return
        indices = [0] * r
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (r - i)
            yield tuple(pool[i] for i in indices)

    def combinations_with_replacements(self, iterable, r, group, group_types_dict):
        pool = tuple(iterable)
        n = len(pool)
        count = 0
        if not n and r:
            return
        indices = [0] * r
        gt = tuple(pool[i] for i in indices)
        yield gt
        # if self.is_bipartite(gt, group):
        #     count += self.count_total_points_dominated(gt, group_types_dict)
        #     yield count
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (r - i)
            gt = tuple(pool[i] for i in indices)
            yield gt
            # if self.is_bipartite(gt, group):
            #     count += self.count_total_points_dominated(
            #         gt, group_types_dict)
            #     yield count

    def get_number_of_groups_dominated_group(self, group, group_size):
        children_set = set()
        for point in group:
            cs = [point] + self.dsg[point].children
            children_set.update(cs)
        group_types_dict = self.build_all_group_types(children_set, group)
        # count, group_type = self.get_existing_group_type(group_types_dict)
        count = 0
        for g in combinations_with_replacement(group_types_dict.keys(), group_size):
            if self.is_bipartite(g, group):
                count += self.count_total_points_dominated(
                    g, group_types_dict)
        # if count == -1:
            # res = islice(self.combinations_with_replacements(
            #     group_types_dict.keys(), group_size, group, group_types_dict), self.total_number-1, None)
            # count = 0
            # for g in combinations_with_replacement(group_types_dict.keys(), group_size):
            #     count += self.count_total_points_dominated(
            #         g, group_types_dict)

            # self.add_to_existing_type(group_type, count)

        print(count-1)
        return count - 1
