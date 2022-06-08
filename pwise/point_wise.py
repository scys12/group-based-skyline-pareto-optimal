class GSkylineGroup:
    class SETreeNode:
        def __init__(self, points, max_layer_group, children_set, point_index=-1):
            self.points = points
            self.tail_sets = list()
            self.point_index = point_index
            self.max_layer_group = max_layer_group
            self.children_set = children_set

        def get_tail_sets(self, dsg_keys):
            for i in range(self.point_index + 1, len(dsg_keys)):
                yield dsg_keys[i]

        def __str__(self):
            return str(
                {
                    "points": self.points,
                    "level": len(self.points),
                    "point_index": self.point_index,
                    "tail_sets": self.tail_sets,
                }
            )

    def __init__(self, dsg, group_size) -> None:
        self.dsg = dsg
        self.group_size = group_size
        self.unit_group = {}
        self.skyline_groups = []
        self.create_unit_group(self.dsg)
        self.dsg_keys = list(dsg)

    def create_unit_group(self, dsg):
        removed_dsg = 0
        for point_key in list(dsg):
            unit_group_points = dsg[point_key].parents + [point_key]
            dsg[point_key].point_index -= removed_dsg
            if len(unit_group_points) >= self.group_size:
                if len(unit_group_points) == self.group_size:
                    self.skyline_groups.append(unit_group_points)
                del dsg[point_key]
                removed_dsg += 1
            else:
                self.unit_group[point_key] = unit_group_points

    def verificate_g_skyline_group(self, group):
        unit_group_set = set()
        for point in group:
            unit_group_set.update(self.unit_group[point])
        return len(unit_group_set) == len(group)

    def processing(self):
        root = self.SETreeNode([], 0, set())
        temp_groups = [root]
        for i in range(1, self.group_size + 1):
            candidate_groups = []
            for group in temp_groups:
                children_set = group.children_set
                max_layer_group = group.max_layer_group
                group_points = group.points.copy()
                if len(group.points) > 0:
                    children_set = set(self.dsg[group.points[-1]].children)
                    children_set.update(group.children_set)
                    max_layer_group = max(
                        self.dsg[group.points[-1]].layer_index, group.max_layer_group
                    )
                for point in group.get_tail_sets(self.dsg_keys):
                    if point not in children_set and self.dsg[point].layer_index != 1:
                        continue
                    if self.dsg[point].layer_index - max_layer_group >= 2:
                        break
                    group_points.append(point)
                    if self.verificate_g_skyline_group(group_points):
                        point_index = max(
                            group.point_index, self.dsg[point].point_index
                        )
                        if i == self.group_size:
                            yield group_points.copy()
                        else:
                            sg = self.SETreeNode(
                                group_points.copy(),
                                max_layer_group,
                                children_set,
                                point_index,
                            )
                            candidate_groups.append(sg)
                    group_points.pop()
            temp_groups = candidate_groups
