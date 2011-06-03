import curses
import itertools
import math
import random

from mnrl.entities import Being
from mnrl.fov import FieldOfView
from mnrl.astar import AStar, AStarNode
from mnrl.map import Cave
        
class DreamCreature(Being):
    def __init__(self, glyph, name):
        super(Entity, self).__init__(glyph, name)
        self.tame = False
        
class Rudwot(DreamCreature):
    def __init__(self):
        super(Rudwot, self).__init__("r", "Rudwot")
        
class Player(Being):
    def __init__(self, x, y):
        super(Player, self).__init__("@", "Tony")
        self.move(x, y)

def make_graph(mapp):
    nodes = [[AStarNode(x, y) for y in range(mapp.height)] for x in range(mapp.width)]
    graph = {}
    for x, y in itertools.product(range(mapp.width), range(mapp.height)):
        node = nodes[x][y]
        graph[node] = []
        for i, j in itertools.product(range(-1, 2), range(-1, 2)):
            if x + i < 0: continue
            if y + j < 0: continue
            if mapp.tiles[y][x].solid: continue
            # if monster_here(): continue
            try:
                graph[nodes[x][y]].append(nodes[x+i][y+j])
            except IndexError:
                continue
    return graph, nodes
                        
def main(stdscr):
    def setup():
        curses.curs_set(0)
            
    def teardown():
        curses.curs_set(1)
    
    mmap = Cave(75, 22)
    fov = FieldOfView(mmap)
    px, py = mmap.blink()
    player = Player(px, py)
    fov.light_circle(px, py, 5)
    sx, sy = mmap.blink()
    graph, nodes = make_graph(mmap)
    paths = AStar(graph)
    path = paths.search(nodes[px][py], nodes[sx][sy])
    
    #return
    
    setup()
    
    def redraw():
        for y, row in enumerate(mmap.tiles):
            for x, tile in enumerate(row):
                if tile.lit:
                    stdscr.addch(y, x, tile.glyph)
        for c in path:
            stdscr.addch(c.y, c.x, "x")
        stdscr.addch(sy, sx, "$")
        stdscr.addch(player.y, player.x, player.glyph)
    
    redraw()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            if mmap.traversable(player.x, player.y - 1):
                player.step(0, -1)
        elif key == curses.KEY_DOWN:
            if mmap.traversable(player.x, player.y + 1):
                player.step(0, 1)
        elif key == curses.KEY_LEFT:
            if mmap.traversable(player.x - 1, player.y):
                player.step(-1, 0)
        elif key == curses.KEY_RIGHT:
            if mmap.traversable(player.x + 1, player.y):
                player.step(1, 0)
        fov.light_circle(player.x, player.y, 5)
        redraw()
    teardown()

if __name__ == "__main__":
    curses.wrapper(main)
    #main({})