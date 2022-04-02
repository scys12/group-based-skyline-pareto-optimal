class Skyline:
    @staticmethod
    def dominate(p1, p2):
        is_dominated = False
        count = 0
        for i in range(len(p1)):
            if p1[i] <= p2[i]:
                count += 1
            if p1[i] < p2[i]:
                is_dominated = True
        return count == len(p1) and is_dominated
