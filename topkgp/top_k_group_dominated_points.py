from util import get_top_points_by_approximate
from util import KeyWrapper, create_subset, reverse_bisort
from math import comb


class TopKSkylineGroupsDominatedPoints:
    def __init__(self, dsg, group_size, layers, k):
        self.dominated_points_of_group = {}
        self.group_size = group_size
        self.dsg = dsg
        self.layers = layers
        self.points_of_max_layer = []
        self.upper_dominated_points = {}
        self.k = k
        self.group_flag = set()
        self.skyline_groups = None
        self.get_maximum_top_k_layer()

    def get_children_set(self, point_key):
        return self.dsg[point_key].children + [point_key]

    def get_dominated_points_of_point(self, point):
        return len(self.dsg[point].children)

    def get_dominated_points_of_group(self, group):
        if group in self.dominated_points_of_group:
            return self.dominated_points_of_group[group]

        dominated_points = set()
        for point in group:
            dominated_points.update(self.get_children_set(point))
        total = len(dominated_points)-self.group_size
        return total

    def get_upper_bound_dominated_points(self, group):
        if group in self.upper_dominated_points:
            return self.upper_dominated_points[group]

        total = 0
        for point in group:
            total += self.get_dominated_points_of_point(point)
        self.upper_dominated_points[group] = total
        return total

    def get_maximum_top_k_layer(self):
        total_points = 0
        points = []
        for layer in self.layers:
            total_points += len(self.layers[layer])
            points.extend(self.layers[layer])
            if comb(total_points, self.group_size) >= self.k:
                break
        self.points_of_max_layer = points

    def get_top_points_of_max_layer(self):
        self.points_of_max_layer.sort(
            key=lambda point: self.get_dominated_points_of_point(point), reverse=True)
        self.points_of_max_layer = get_top_points_by_approximate(
            self.points_of_max_layer, self.group_size, self.k)

    def create_child_skyline_group(self, candidate_groups, parent_group):
        children_set = set()
        candidate_groups_set = {frozenset(x) for x in candidate_groups}
        for point in parent_group:
            children_set.update(self.get_children_set(point))
        children_list = list(children_set)
        children_list.sort(
            key=lambda point: self.get_dominated_points_of_point(point), reverse=True)
        children_list = get_top_points_by_approximate(
            children_list, self.group_size, self.k)
        for group in create_subset(children_list, -1, self.group_size):
            if frozenset(group) not in candidate_groups_set:
                yield group

    def update_skyline_candidate_groups(self, candidate_groups, dominated_points_of_group, dpg, group, k, remove_g_first=False):
        blidx = reverse_bisort(KeyWrapper(
            candidate_groups, key=dominated_points_of_group), dpg)
        candidate_groups.insert(blidx, group)
        dominated_points_of_group[group] = dpg
        if remove_g_first:
            self.group_flag.discard(frozenset(candidate_groups[k]))
        del dominated_points_of_group[candidate_groups[k]]
        del candidate_groups[k]
        return candidate_groups

    def processing(self):
        self.get_top_points_of_max_layer()
        new_groups = list(create_subset(
            self.points_of_max_layer, -1, self.group_size))
        new_groups.sort(
            key=lambda group: self.get_upper_bound_dominated_points(group), reverse=True)
        candidate_groups = []
        for i in range(self.k):
            self.dominated_points_of_group[new_groups[i]] = self.get_dominated_points_of_group(
                new_groups[i])
            candidate_groups.append(new_groups[i])
        candidate_groups.sort(
            key=lambda group: self.dominated_points_of_group[group], reverse=True)
        temp = self.dominated_points_of_group[candidate_groups[self.k-1]]

        for i in range(self.k, len(new_groups)):
            group = new_groups[i]
            if self.upper_dominated_points[group] > temp:
                dpg = self.get_dominated_points_of_group(
                    group)
                if dpg > temp:
                    candidate_groups = self.update_skyline_candidate_groups(
                        candidate_groups, self.dominated_points_of_group, dpg, group, self.k)
                    temp = self.dominated_points_of_group[candidate_groups[self.k-1]]

        g_first = candidate_groups[0]
        dpg_g_first = self.get_dominated_points_of_group(g_first)
        while dpg_g_first > temp + 1:
            self.group_flag.add(frozenset(group))
            for group in self.create_child_skyline_group(candidate_groups, g_first):
                udp = self.get_upper_bound_dominated_points(group)
                if udp > temp:
                    dpg = self.get_dominated_points_of_group(group)
                    if dpg > temp:
                        candidate_groups = self.update_skyline_candidate_groups(
                            candidate_groups, self.dominated_points_of_group, dpg, group, self.k, True)
                        temp = self.dominated_points_of_group[candidate_groups[self.k-1]]

            for group in candidate_groups:
                if frozenset(group) not in self.group_flag:
                    g_first = group
                    dpg_g_first = self.get_dominated_points_of_group(g_first)
                    break

        self.skyline_groups = candidate_groups
