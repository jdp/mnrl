class AStar(object):
    def __init__(self, graph):
        self.graph = graph
        
    def heuristic(self, node, start, end):
        import math
        return math.sqrt((end.x-node.x)**2 + (end.y-node.y)**2)
        
    def search(self, start, end):
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        while openset:
            current = min(openset, key=lambda o:o.g + o.h)
            if current == end:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.g + current.move_cost(node)
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    node.g = current.g + current.move_cost(node)
                    node.h = self.heuristic(node, start, end)
                    node.parent = current
                    openset.add(node)
        return []

class AStarNode(object):
    def __init__(self, x, y):
        self.g = 0
        self.h = 0
        self.parent = None
        self.x, self.y = x, y
        
    def move_cost(self, other):
        diagonal = abs(self.x-other.x) == 1 and abs(self.y-other.y) == 1
        return 14 if diagonal else 10
