class GSkylineGroup:
    class SETreeNode:
        def __init__(self, points, level, dsg_keys, max_layer_group, children_set, point_index=-1):
            self.points = points
            self.level = level
            self.tail_sets = list()
            self.point_index = point_index
            self.add_tail_sets(dsg_keys)
            self.max_layer_group = max_layer_group
            self.children_set = children_set

        def add_tail_sets(self, dsg_keys):
            self.tail_sets = dsg_keys[self.point_index+1:]

        def __str__(self):
            return str({
                'points': self.points,
                'level': self.level,
                'point_index': self.point_index,
            })

    def __init__(self, dsg, group_size) -> None:
        self.dsg = dsg
        self.group_size = group_size
        self.unit_group = {}
        self.skyline_groups = []
        self.temp_groups = []
        self.create_unit_group(self.dsg)
        self.dsg_keys = list(dsg)

    def append_temp_groups_to_skyline_groups(self, group_size, temp_groups, skyline_groups):
        if len(skyline_groups) > group_size:
            skyline_groups[group_size].extend(temp_groups)
        elif len(skyline_groups) <= group_size:
            skyline_groups.extend([] for _ in range(
                (group_size+1)-len(skyline_groups)))
            skyline_groups[group_size].extend(temp_groups)

    def create_unit_group(self, dsg):
        for point_key in list(dsg):
            unit_group = dsg[point_key].parents + \
                [point_key]
            if len(unit_group) >= self.group_size:
                if len(unit_group) == self.group_size:
                    sg = self.SETreeNode(unit_group, self.group_size,
                                         list(dsg.keys()), 0, set(), dsg[point_key].point_index)
                    self.temp_groups.append(sg)
                del dsg[point_key]
            else:
                self.unit_group[point_key] = unit_group

    def verificate_g_skyline_group(self, group):
        points = set()
        size = len(group)
        for point in group:
            points.update(self.unit_group[point])
        return len(points) == size

    def processing(self):
        root = self.SETreeNode([], 0, self.dsg_keys, 0, set())
        self.skyline_groups = [
            [root]
        ]

        for i in range(1, self.group_size+1):
            for group in self.skyline_groups[i-1]:
                children_set = group.children_set
                max_layer_group = group.max_layer_group
                if len(group.points) > 0:
                    children_set = set(self.dsg[group.points[-1]].children)
                    children_set.update(group.children_set)
                    max_layer_group = self.dsg[group.points[-1]
                                               ].layer_index if group.max_layer_group < self.dsg[group.points[-1]].layer_index else group.max_layer_group

                for point in group.tail_sets:
                    if point not in children_set and self.dsg[point].layer_index != 1:
                        continue
                    if self.dsg[point].layer_index - max_layer_group >= 2:
                        break

                    candidate_group = group.points.copy()
                    candidate_group.append(point)

                    if self.verificate_g_skyline_group(candidate_group):
                        point_index = group.point_index if group.point_index > self.dsg[
                            point].point_index else self.dsg[point].point_index
                        sg = self.SETreeNode(candidate_group, i,
                                             self.dsg_keys, max_layer_group, children_set, point_index)
                        if len(self.skyline_groups) == i:
                            self.skyline_groups.append([])
                        self.skyline_groups[i].append(sg)
        self.append_temp_groups_to_skyline_groups(
            self.group_size, self.temp_groups, self.skyline_groups)
