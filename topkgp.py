from util import KeyWrapper, create_subset, reverse_bisort


class TopKSkylineGroupsDominatedPoints:
    def __init__(self, dsg, group_size, layers, k):
        self.dominated_points_of_group = {}
        self.children_set = {}
        self.group_size = group_size
        self.dsg = dsg
        self.layers = layers
        self.number_of_maximum_layer = 0
        self.points_of_max_layer = []
        self.upper_dominated_points = {}
        self.k = k
        self.group_flag = []
        self.skyline_groups = None

        self.get_maximum_top_k_layer()

    def get_children_set(self, point_key):
        return self.dsg[point_key].children + [point_key]

    def get_dominated_points_of_point(self, point):
        return len(self.dsg[point].children)

    def get_dominated_points_of_group(self, group):
        dp = set()
        for point in group:
            dp.update(self.get_children_set(point))
        return len(dp)-self.group_size

    def get_upper_bound_dominated_points(self, group):
        total = 0
        for point in group:
            total += self.get_dominated_points_of_point(point)
        return total

    def get_maximum_top_k_layer(self):
        total = 0
        idx = 0
        for l in self.layers.keys():
            self.points_of_max_layer.extend(self.layers[l])
            total += len(self.layers[l])
            idx += 1
            if total >= self.k:
                break
        self.number_of_maximum_layer = idx

    def sort_points_of_max_layer(self):
        dominated_points_of_point = {}
        for point in self.points_of_max_layer:
            dominated_points_of_point[point] = self.get_dominated_points_of_point(
                point)
        self.points_of_max_layer.sort(
            key=lambda point: dominated_points_of_point[point], reverse=True)

    def processing(self):
        self.sort_points_of_max_layer()

        new_groups = list(create_subset(
            self.points_of_max_layer, self.group_size))
        for group in new_groups:
            self.upper_dominated_points[group] = self.get_upper_bound_dominated_points(
                group)
        new_groups.sort(
            key=lambda group: self.upper_dominated_points[group], reverse=True)

        candidate_groups = []
        for i in range(self.k):
            self.dominated_points_of_group[new_groups[i]] = self.get_dominated_points_of_group(
                new_groups[i])
            candidate_groups.append(new_groups[i])
        candidate_groups.sort(
            key=lambda group: self.dominated_points_of_group[group], reverse=True)
        temp = self.dominated_points_of_group[candidate_groups[self.k-1]]

        new_groups = new_groups[self.k:]
        for group in new_groups:
            if self.upper_dominated_points[group] > temp:
                dpg = self.get_dominated_points_of_group(
                    group)
                if dpg > temp:
                    blidx = reverse_bisort(KeyWrapper(
                        candidate_groups, key=self.dominated_points_of_group), dpg)
                    candidate_groups.insert(blidx, group)
                    self.dominated_points_of_group[group] = dpg
                    del self.dominated_points_of_group[candidate_groups[self.k]]
                    candidate_groups = candidate_groups[:self.k]
                    temp = self.dominated_points_of_group[candidate_groups[self.k-1]]

        g_first = candidate_groups[0]
        while self.get_dominated_points_of_group(g_first) > temp + 1:
            self.group_flag.append(group)
            child_groups = create_subset(g_first, self.group_size)
            for group in child_groups:
                udp = self.get_upper_bound_dominated_points(group)
                if udp > temp:
                    dpg = self.get_dominated_points_of_group(group)
                    if dpg > temp:
                        blidx = reverse_bisort(KeyWrapper(
                            candidate_groups, key=self.dominated_points_of_group), dpg)
                        candidate_groups.insert(blidx, group)
                        self.dominated_points_of_group[group] = dpg
                        del self.dominated_points_of_group[candidate_groups[self.k]]
                        candidate_groups = candidate_groups[:self.k]
                        temp = self.dominated_points_of_group[candidate_groups[self.k-1]]

            for group in candidate_groups:
                if group not in self.group_flag:
                    g_first = group
                    break

        self.skyline_groups = candidate_groups
