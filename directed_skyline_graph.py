from skyline import Skyline


class DSG:
    def __init__(self, layer_index, point_index) -> None:
        self.layer_index = layer_index
        self.point_index = point_index
        self.parents = []
        self.children = []

    def __str__(self):
        return str({
            "layer_index": self.layer_index,
            "point_index": self.point_index,
            "parents": self.parents,
            "children": self.children,
        })


class SkylineGraph:
    def __init__(self, layers, max_layer):
        self.graph = {}
        self.layers = layers
        self.max_layer = max_layer
        self.current_point_index = 0

        for i in range(len(self.layers[1])):
            key = tuple(self.layers[1][i])
            self.graph[key] = DSG(1, self.current_point_index)
            self.current_point_index += 1

    def processing(self):
        for i in range(2, self.max_layer+1):
            for j in range(len(self.layers[i])):
                dsg = DSG(i, self.current_point_index)
                self.current_point_index += 1
                for k in range(i-1, 0, -1):
                    for l in range(len(self.layers[k])):
                        if Skyline.dominate(self.layers[k][l], self.layers[i][j]):
                            dsg.parents.append(self.layers[k][l])
                            key = tuple(self.layers[k][l])
                            self.graph[key].children.append(self.layers[i][j])
                key = tuple(self.layers[i][j])
                self.graph[key] = dsg
