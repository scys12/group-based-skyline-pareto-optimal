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
        self.skyline_groups = []
        self.get_maximum_points_from_layer()

    def get_children_set(self, point):
        return self.dsg[point]["children"] + [point]

    def get_dominated_points_of_point(self, point):
        return len(self.dsg[point]["children"])

    def get_dominated_points_of_group(self, group):
        if group in self.dominated_points_of_group:
            return self.dominated_points_of_group[group]

        dominated_points = set()
        for point in group:
            dominated_points.update(self.get_children_set(point))
        total = len(dominated_points) - self.group_size
        return total

    def get_upper_bound_dominated_points(self, group):
        if group in self.upper_dominated_points:
            return self.upper_dominated_points[group]

        total = 0
        for point in group:
            total += self.get_dominated_points_of_point(point)
        self.upper_dominated_points[group] = total
        return total

    def get_maximum_points_from_layer(self):
        self.points_of_max_layer = []
        for layer in self.layers:
            self.points_of_max_layer.extend(self.layers[layer])
            if comb(len(self.points_of_max_layer), self.group_size) >= self.k:
                break

    def get_top_points_of_max_layer(self):
        self.points_of_max_layer.sort(
            key=lambda point: self.get_dominated_points_of_point(point), reverse=True
        )
        self.points_of_max_layer = get_top_points_by_approximate(
            self.points_of_max_layer, self.group_size, self.k
        )

    def create_child_skyline_group(self, candidate_groups, parent_group):
        children_set = set()
        candidate_groups_set = {frozenset(x) for x in candidate_groups}
        for point in parent_group:
            children_set.update(self.get_children_set(point))
        children_list = list(children_set)
        children_list.sort(
            key=lambda point: self.get_dominated_points_of_point(point), reverse=True
        )
        children_list = get_top_points_by_approximate(
            children_list, self.group_size, self.k
        )
        for group in create_subset(children_list, -1, self.group_size):
            if frozenset(group) not in candidate_groups_set:
                yield group

    def update_skyline_candidate_groups(
        self,
        candidate_groups,
        dominated_points_of_group,
        dpg,
        group,
        k,
        group_flag=None,
    ):
        position = reverse_bisort(
            KeyWrapper(candidate_groups, key=dominated_points_of_group), dpg
        )
        candidate_groups.insert(position, group)
        dominated_points_of_group[group] = dpg
        if group_flag:
            group_flag.discard(frozenset(candidate_groups[k]))
        del dominated_points_of_group[candidate_groups[k]]
        del candidate_groups[k]

    def processing(self):
        self.get_top_points_of_max_layer()
        new_groups = list(create_subset(self.points_of_max_layer, -1, self.group_size))
        new_groups.sort(
            key=lambda group: self.get_upper_bound_dominated_points(group), reverse=True
        )

        for i in range(self.k):
            self.dominated_points_of_group[
                new_groups[i]
            ] = self.get_dominated_points_of_group(new_groups[i])
            self.skyline_groups.append(new_groups[i])
        self.skyline_groups.sort(
            key=lambda group: self.dominated_points_of_group[group], reverse=True
        )
        temp = self.dominated_points_of_group[self.skyline_groups[self.k - 1]]
        for i in range(self.k, len(new_groups)):
            group = new_groups[i]
            if self.upper_dominated_points[group] > temp:
                dpg = self.get_dominated_points_of_group(group)
                if dpg > temp:
                    self.update_skyline_candidate_groups(
                        self.skyline_groups,
                        self.dominated_points_of_group,
                        dpg,
                        group,
                        self.k,
                    )
                    temp = self.dominated_points_of_group[
                        self.skyline_groups[self.k - 1]
                    ]

        g_first = self.skyline_groups[0]
        dpg_g_first = self.get_dominated_points_of_group(g_first)
        group_flag = set()
        while dpg_g_first > temp + 1:
            group_flag.add(frozenset(g_first))
            for group in self.create_child_skyline_group(self.skyline_groups, g_first):
                udp = self.get_upper_bound_dominated_points(group)
                if udp > temp:
                    dpg = self.get_dominated_points_of_group(group)
                    if dpg > temp:
                        self.update_skyline_candidate_groups(
                            self.skyline_groups,
                            self.dominated_points_of_group,
                            dpg,
                            group,
                            self.k,
                            group_flag,
                        )
                        temp = self.dominated_points_of_group[
                            self.skyline_groups[self.k - 1]
                        ]

            for group in self.skyline_groups:
                if frozenset(group) not in group_flag:
                    g_first = group
                    dpg_g_first = self.get_dominated_points_of_group(g_first)
                    break
