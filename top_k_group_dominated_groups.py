from util import KeyWrapper, RepresentativeSkylineGraph, create_subset, reverse_bisort


class TopKSkylineGroupsDominatedGroups:
    def __init__(self, dsg, group_size, layers, k):
        self.dominated_groups_of_group = {}
        self.children_set = {}
        self.group_size = group_size
        self.dsg = dsg
        self.layers = layers
        self.number_of_maximum_layer = 0
        self.points_in_layer = []
        self.upper_dominated_groups = {}
        self.k = k
        self.group_flag = []
        self.skyline_groups = None

        self.get_all_points_from_layer(self.group_size)

    def get_children_set(self, point_key):
        return self.dsg[point_key].children + [point_key]

    def get_dominated_groups_of_point(self, point):
        return len(self.dsg[point].children)

    def get_dominated_groups_of_group(self, group):
        srg = RepresentativeSkylineGraph(self.dsg, group)
        child_groups = srg.graph[group[0]]['children_set'].copy()
        total_dg = 0

        for idx_group in range(1, len(group)):
            temp_groups = []
            for point_child in srg.graph[group[idx_group]]['children_set']:
                temp_group = []
                for k in range(len(child_groups)):
                    if isinstance(child_groups[k][0], set):
                        s = child_groups[k][0].copy()
                        total = child_groups[k][1]
                    else:
                        s = {child_groups[k]}
                        total = srg.graph[child_groups[k]]['weight']

                    s.add(point_child)
                    total *= srg.graph[point_child]['weight']

                    if len(s) != idx_group + 1:
                        continue
                    temp_group.append((s, total))

                # check if point of temp_group combinations exist in temp_groups
                # if yes, then remove it
                temp_group = [x for x in temp_group if not any(
                    [set(y[0]).issubset(set(x[0])) for y in temp_groups])]
                temp_groups.extend(temp_group)
            child_groups = temp_groups
        for cg in child_groups:
            total_dg += cg[1]
        return total_dg-1

    def get_upper_bound_dominated_groups(self, group):
        total = 1
        for point in group:
            total *= (self.get_dominated_groups_of_point(point) + 1)
        return total-1

    def get_all_points_from_layer(self, group_size):
        for layer_index in self.layers:
            if layer_index > group_size:
                break
            self.points_in_layer.extend(self.layers[layer_index])

    def sort_points_in_layer(self):
        dominated_groups_of_point = {}
        for point in self.points_in_layer:
            dominated_groups_of_point[point] = self.get_dominated_groups_of_point(
                point)
        self.points_in_layer.sort(
            key=lambda point: dominated_groups_of_point[point], reverse=True)

    def processing(self):
        self.sort_points_in_layer()

        new_groups = list(create_subset(
            self.points_in_layer, -1, self.group_size))
        for group in new_groups:
            self.upper_dominated_groups[group] = self.get_upper_bound_dominated_groups(
                group)
        new_groups.sort(
            key=lambda group: self.upper_dominated_groups[group], reverse=True)

        candidate_groups = []
        for i in range(self.k):
            self.dominated_groups_of_group[new_groups[i]] = self.get_dominated_groups_of_group(
                new_groups[i])
            candidate_groups.append(new_groups[i])
        candidate_groups.sort(
            key=lambda group: self.dominated_groups_of_group[group], reverse=True)
        temp = self.dominated_groups_of_group[candidate_groups[self.k-1]]

        new_groups = new_groups[self.k:]
        for group in new_groups:
            if self.upper_dominated_groups[group] > temp:
                dpg = self.get_dominated_groups_of_group(
                    group)
                if dpg > temp:
                    blidx = reverse_bisort(KeyWrapper(
                        candidate_groups, key=self.dominated_groups_of_group), dpg)
                    candidate_groups.insert(blidx, group)
                    self.dominated_groups_of_group[group] = dpg
                    del self.dominated_groups_of_group[candidate_groups[self.k]]
                    candidate_groups = candidate_groups[:self.k]
                    temp = self.dominated_groups_of_group[candidate_groups[self.k-1]]

        self.skyline_groups = candidate_groups
