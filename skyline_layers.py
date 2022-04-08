from skyline import Skyline


class SkylinePoint:
    def __init__(self, point):
        self.layer = None
        self.point = tuple(point)

    def __str__(self):
        return str({
            "layer": self.layer,
            "point": self.point
        })


class SkylineLayer:
    def __init__(self, points):
        self.points = []
        for p in points:
            self.points.append(SkylinePoint(p))
        self.points[0].layer = 1
        self.tail_point = [self.points[0].point]
        self.layers = {
            1: [self.points[0].point]
        }
        self.max_layer = 1

    def processing(self):

        for i in range(1, len(self.points)):
            if not Skyline.dominate(self.tail_point[0], self.points[i].point):
                self.points[i].layer = 1
                self.tail_point[0] = self.points[i].point
                self.layers[self.points[i].layer].append(
                    self.points[i].point)
            elif Skyline.dominate(self.tail_point[self.max_layer-1], self.points[i].point):
                self.max_layer += 1
                self.points[i].layer = self.max_layer
                self.tail_point.append(self.points[i].point)
                self.layers[self.points[i].layer] = [self.points[i].point]
            else:
                current_layer = self.binary_search(
                    self.tail_point, self.points[i].point, 1, self.max_layer-1)
                self.points[i].layer = current_layer
                self.tail_point[current_layer-1] = self.points[i].point
                self.layers[self.points[i].layer].append(
                    self.points[i].point)

    def binary_search(self, tail_point, point, low, high):
        if high >= low:
            current_layer = low + (high - low)//2
            if not Skyline.dominate(tail_point[current_layer], point):
                if Skyline.dominate(tail_point[current_layer-1], point):
                    return current_layer + 1
                elif not Skyline.dominate(tail_point[current_layer-1], point):
                    return self.binary_search(tail_point, point, low, current_layer-1)
            else:
                return self.binary_search(tail_point, point, current_layer + 1, high)
        else:
            return -1
