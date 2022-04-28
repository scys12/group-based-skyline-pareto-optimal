class Skyline:
    def __init__(self, point):
        self.layer = None
        self.point = tuple(point)

    def dominate(self, other):
        p1 = self.point
        p2 = other.point

        if len(p1) != len(p2):
            return False

        for i in range(len(p1)):
            if p1[i] > p2[i]:
                return False
        return True

    def __str__(self):
        return str({
            "layer": self.layer,
            "point": self.point
        })
