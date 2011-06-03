class Entity(object):
    def __init__(self, glyph):
        self.glyph = glyph
        self.solid = True
        self.opaque = True
        self.being = False
        self.seen = False
        self.lit = False
        self.move(0, 0)
    
    def move(self, x, y):
        self.x = x
        self.y = y
        
class Being(Entity):
    def __init__(self, glyph, name):
        super(Being, self).__init__(glyph)
        self.alive = True
        self.name = name
        
    def step(self, x, y):
        self.x = self.x + x
        self.y = self.y + y