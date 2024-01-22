import pyglet
import numpy as np
import scipy as sp
import time
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

    def set_recs(self):
        recs = [[self.Rectangles(x = w*self.distance,y = h*self.distance,
                            width=self.size, height=self.size,
                            batch = self.batch)
                            for w in range(self.window.width//self.distance)]
                            for h in range(self.window.height//self.distance)]
        self.recs = recs

    def set_cells(self):
        cells = np.zeros((self.window.height//self.distance,self.window.width//self.distance))
        for i in range(len(self.recs)):
            for j in range(len(self.recs[i])):
                cells[i,j] = int(self.recs[i][j].alive())
        self.cells = cells

    def reset_recs(self):
        for i in range(len(self.recs)):
            for j in range(len(self.recs[i])):
                if self.cells[i][j] == 1:
                    self.recs[i][j].born()
                else:
                    self.recs[i][j].dies()

    def live_neighboors(self):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        return sp.signal.convolve2d(self.cells, kernel, mode='same')
    
    def run(self):
        new_cells = np.zeros(1)
        while True:
            new_cells = np.copy(self.cells)
            neighboors = self.live_neighboors()
            for i in range(len(self.cells)):
                for j in range(len(self.cells[i])):
                    if self.cells[i,j] == 1:
                        if neighboors[i,j] not in [2,3]:
                            new_cells[i,j] = 0
                    else:
                        if neighboors[i,j] == 3:
                            new_cells[i,j] = 1
            if (self.cells == new_cells).all():
                break
            self.cells = new_cells
            self.reset_recs()
            self.window.draw(0.1)
            time.sleep(0.05)

game = GameOfLife(20,19, fullscreen=True)
game.set_recs()

@game.window.event
def on_draw():
    game.window.clear()
    game.batch.draw()
    pass

@game.window.event
def on_mouse_press(x,y,button,modifier):
    for i in range(len(game.recs)):
        for j in range(len(game.recs[i])):
            if (game.recs[i][j].x < x < game.recs[i][j].x + game.size) and (game.recs[i][j].y < y < game.recs[i][j].y + game.size):
                game.recs[i][j].change()

@game.window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.ESCAPE:
        game.window.close()
    elif symbol == pyglet.window.key.SPACE:
        game.set_cells()
        game.run()
    pass

pyglet.app.run()