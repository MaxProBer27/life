import pyglet
import random as r
from pyglet.shapes import Rectangle

class GameOfLife():
    def __init__(self, distance = 40, size = 39,
                 fullscreen = True):
        self.distance = distance
        self.size = size
        self.window = pyglet.window.Window(fullscreen = fullscreen)
        self.batch = pyglet.graphics.Batch()
    
    class Rectangles(Rectangle):
        def __init__(self, x, y, width, height, color=(30,30,30), batch=None, group=None):
            super().__init__(x, y, width, height, color, batch, group)
            self.i = 0
            self.j = 0
        
        def reset_color(self,dt):
            self.color = self.original_color
        
        def live(self):
            return self.color == (255,255,255)

    def make_recs(self):
        Recs = [[self.Rectangles(x = w*self.distance,y = h*self.distance,
                            width=self.size, height=self.size,
                            batch = self.batch)
                            for w in range(self.window.width//self.distance)]
                            for h in range(self.window.height//self.distance)]
        recs = []
        for i in range(len(Recs)):
            for j in range(len(Recs[i])):
                Recs[i][j].i = i
                Recs[i][j].i = j
                recs.append(Recs[i][j])
        self.recs = recs

    def live_neighboors(self, i, j):
        nb_colors = [rec.color for rec in self.recs if (any(rec.i == i + x for x in (1,-1)) or
                                                        any(rec.j == j + x for x in (1,-1)))]
        tot = 0
        for color in nb_colors:
            if color == (255,255,255):
                tot += 1
        return tot


game = GameOfLife(40,39)
game.make_recs()

@game.window.event
def on_draw():
    game.window.clear()
    game.batch.draw()
    pass

@game.window.event
def on_mouse_press(x,y,button,modifier):
    for rec in game.recs:
            if (rec.x < x < rec.x + game.size) and (rec.y < y < rec.y + game.size):
                rec.color = (255,255,255)
    pass

@game.window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.ESCAPE:
        game.window.close()
    elif symbol == pyglet.window.key.SPACE:
        for rec in game.recs:
            rec.color = (30,30,30)
    pass

pyglet.app.run()