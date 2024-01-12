import pyglet
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
            self.original_color = color
        
        def reset_color(self,dt):
            self.color = self.original_color
        
        def alive(self):
            return self.color == (255,255,255,255)
        
        def born(self):
            self.color = (255,255,255,255)
        
        def dies(self):
            self.color = self.original_color
        
        def change(self):
            if self.alive():
                self.dies()
            else:
                self.born()

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
                Recs[i][j].j = j
                recs.append(Recs[i][j])
        return recs
        
    def set_recs(self):
        self.recs = self.make_recs()
    

    def live_neighboors(self, ind):
        nb = [rec.alive() for rec in self.recs if (any(rec.i == self.recs[ind].i + x for x in (1,-1,0)) and
                                                   any(rec.j == self.recs[ind].j + x for x in (1,-1,0)))
                                                   and rec != self.recs[ind]]
        return sum(nb)
    
    def run(self):
        while any(rec.alive() for rec in self.recs):
            new_recs = self.make_recs()
            for rec in self.recs:
                if rec.alive():
                    if not (2 <= self.live_neighboors(self.recs.index(rec)) <= 3):
                        new_recs[self.recs.index(rec)].dies()
                    else:
                        new_recs[self.recs.index(rec)].born()
                else:
                    if self.live_neighboors(self.recs.index(rec)) == 3:
                        new_recs[self.recs.index(rec)].born()
            self.recs = new_recs
            self.window.draw(0.1)

game = GameOfLife(60,59, fullscreen=True)
game.set_recs()

@game.window.event
def on_draw():
    game.window.clear()
    game.batch.draw()
    pass

@game.window.event
def on_mouse_press(x,y,button,modifier):
    for rec in game.recs:
            if (rec.x < x < rec.x + game.size) and (rec.y < y < rec.y + game.size):
                rec.change()
    pass

@game.window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.ESCAPE:
        game.window.close()
    elif symbol == pyglet.window.key.SPACE:
        game.run()
    pass

pyglet.app.run()