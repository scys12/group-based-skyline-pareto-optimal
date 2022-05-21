from topkgg.pruning_algorithm import PruningAlgorithm
from topkgg.counting_algorithm import CountingAlgorithm
from util import KeyWrapper, create_subset, reverse_bisort, get_top_points_by_approximate
from math import comb


class TopKSkylineGroupsDominatedGroups:
    ALGO = ["PA", "CA"]

    def __init__(self, dsg, group_size, layers, k, algo="PA"):
        self.dominated_groups_of_group = {}
        self.children_set = {}
        self.group_size = group_size
        self.dsg = dsg
        self.layers = layers
        self.number_of_maximum_layer = 0
        self.points_in_layer = []
        self.upper_dominated_groups = {}
        self.k = k
        self.skyline_groups = None
        self.dominated_group_algo = self.initialize_dominated_group_algo(algo)
        self.get_all_points_from_dsg(self.dsg, self.group_size)

    def initialize_dominated_group_algo(self, algo):
        if algo == self.ALGO[1]:
            return CountingAlgorithm(self.dsg, self.group_size)
        return PruningAlgorithm(self.dsg)

    def get_children_set(self, point_key):
        return self.dsg[point_key].children + [point_key]

    def get_dominated_groups_of_point(self, point):
        return len(self.dsg[point].children)

    def get_dominated_groups_of_group(self, group):
        if group in self.dominated_groups_of_group:
            return self.dominated_groups_of_group[group]

        return self.dominated_group_algo.get_number_of_groups_dominated_group(group)

    def get_upper_bound_dominated_groups(self, group):
        if group in self.upper_dominated_groups:
            return self.upper_dominated_groups[group]

        total = 1
        for point in group:
            total *= (self.get_dominated_groups_of_point(point) + 1)
        self.upper_dominated_groups[group] = total-1
        return total-1

    def get_all_points_from_dsg(self, dsg, group_size):
        for point in dsg:
            unit_group = dsg[point].parents + [point]
            if len(unit_group) <= group_size:
                yield point

    def sort_points_in_layer(self):
        points = self.get_all_points_from_dsg(self.dsg, self.group_size)
        return sorted(points, key=lambda point: self.get_dominated_groups_of_point(point), reverse=True)

    def processing(self):
        self.points_in_layer = get_top_points_by_approximate(
            self.sort_points_in_layer(), self.group_size, self.k)
        new_groups = list(create_subset(
            self.points_in_layer, -1, self.group_size))
        new_groups.sort(
            key=lambda group: self.get_upper_bound_dominated_groups(group), reverse=True)

        total_groups = comb(len(self.points_in_layer), self.group_size)
        candidate_groups = []
        for i in range(self.k):
            self.dominated_groups_of_group[new_groups[i]] = self.get_dominated_groups_of_group(
                new_groups[i])
            candidate_groups.append(new_groups[i])
        candidate_groups.sort(
            key=lambda group: self.dominated_groups_of_group[group], reverse=True)
        temp = self.dominated_groups_of_group[candidate_groups[self.k-1]]

        for i in range(self.k, total_groups):
            group = new_groups[i]
            if self.upper_dominated_groups[group] > temp:
                dominated_group = self.get_dominated_groups_of_group(group)
                if dominated_group > temp:
                    candidate_idx = reverse_bisort(KeyWrapper(
                        candidate_groups, key=self.dominated_groups_of_group), dominated_group)
                    candidate_groups.insert(candidate_idx, group)
                    self.dominated_groups_of_group[group] = dominated_group
                    del self.dominated_groups_of_group[candidate_groups[self.k]]
                    del candidate_groups[self.k]
                    temp = self.dominated_groups_of_group[candidate_groups[self.k-1]]

        self.skyline_groups = candidate_groups
