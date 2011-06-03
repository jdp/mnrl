import itertools
import math

class FieldOfView(object):
    def __init__(self, map):
        self.map = map
        
    def reveal(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                self.map.tiles[y][x].lit = True
    
    def ray_path(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        path = []
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                try:
                    if self.map.opaque(x, y):
                        return path, False
                    path.append((x, y))
                except IndexError:
                    pass
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                try:
                    if self.map.opaque(x, y):
                        return path, False
                    path.append((x, y))
                except IndexError:
                    pass
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        path.append((x, y))
        return path, True
        
    def cast_ray(self, x0, y0, x1, y1):
        path, success = self.ray_path(x0, y0, x1, y1)
        for pt in path:
            self.map.tiles[pt[1]][pt[0]].lit = True
        
    def light_circle(self, x, y, radius):
        for j in range(-radius, radius):
            for i in range(-radius, radius):
                x1, x2 = x, x + i
                y1, y2 = y, y + j
                if math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < radius:
                    self.cast_ray(x, y, x + i, y + j)
        for i, j in itertools.product(range(self.map.width), range(self.map.height)):
            if not self.map.tiles[j][i].opaque:
                continue
            for ii,jj in itertools.product(range(-1, 2), range(-1, 2)):
                try:
                    tile = self.map.tiles[j+jj][i+ii]
                    if not tile.opaque and tile.lit:
                        self.map.tiles[j][i].lit = True
                        break
                except IndexError:
                    pass