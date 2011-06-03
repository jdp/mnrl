import random

from . import entities

class Floor(entities.Entity):
    def __init__(self, x, y):
        super(Floor, self).__init__(".")
        self.solid = False
        self.opaque = False
        self.move(x, y)
        
class Wall(entities.Entity):
    def __init__(self, x, y):
        super(Wall, self).__init__("#")
        self.move(x, y)
        
class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dcs = []
        self.tiles = [([None] * self.width) for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = Wall(x, y)

    def bump_map(self, test):
        bump = [[test(self.tiles[y][x]) for x in range(self.width)] for y in range(self.height)]
        return bump
        
    def opaque(self, x, y):
        if self.tiles[y][x].opaque:
            return True
        for dc in self.dcs:
            if dc.opaque:
                return True
        return False

    def traversable(self, x, y):
        if (x < 0) or (x > (self.width - 1)):
            return False
        if (y < 0) or (y > (self.height - 1)):
            return False
        if self.tiles[y][x].solid:
            return False
        return True

    def blink(self):
        while True:
            x, y = random.randrange(self.width), random.randrange(self.height)
            if self.traversable(x, y):
                return x, y

class Cave(Map):
    def __init__(self, width, height, noise=3, smooth=2):
        super(Cave, self).__init__(width, height)
        self.dig(noise, smooth)

    def dig(self, noise, smooth):
        floor_tiles = 0
        random.seed()
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if random.choice([True, False]):
                    self.tiles[y][x] = Wall(x, y)
                else:
                    self.tiles[y][x] = Floor(x, y)
        def R(r, x, y):
            n = 0
            for yo in range(-r, r + 1):
                for xo in range(-r, r + 1):
                    try:
                        if self.tiles[y + yo][x + xo].solid:
                            n = n + 1
                    except IndexError:
                        pass
            return n
        for n in range(noise):
            tmp = [([True] * self.width) for i in range(self.height)]
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    tmp[y][x] = R(1, x, y) >= 5 or R(2, x, y) == 2
            for y in range(self.height):
                for x in range(self.width):
                    if tmp[y][x]:
                        self.tiles[y][x] = Wall(x, y)
                    else:
                        self.tiles[y][x] = Floor(x, y)
        for s in range(smooth):
            tmp = [([True] * self.width) for i in range(self.height)]
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    tmp[y][x] = R(1, x, y) >= 5
            for y in range(self.height):
                for x in range(self.width):
                    if tmp[y][x]:
                        self.tiles[y][x] = Wall(x, y)
                    else:
                        self.tiles[y][x] = Floor(x, y)
                        