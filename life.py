import pyglet
import random as r
from pyglet.shapes import Rectangle

window = pyglet.window.Window(fullscreen = False)
batch = pyglet.graphics.Batch()

class Rectangles(Rectangle):
    def __init__(self, x, y, width, height, color=(30,30,30), batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)
        self.original_color = color # Initial square color (30,30,30)
    
    def reset_color(self,dt):
        self.color = self.original_color

def make_recs(distance, size):
    Recs = [[Rectangles(x = w*distance,y = h*distance,
                        width=size, height=size,
                        batch = batch)
                        for w in range(window.width//distance)]
                        for h in range(window.height//distance)]
    return Recs

dis,s = 40,39
Recs = make_recs(40,39)
@window.event
def on_draw():
    window.clear()
    batch.draw()
    pass

@window.event
def on_mouse_press(x,y,button,modifier):
    for i in range(len(Recs)):
        for j in range(len(Recs[i])):
            if (Recs[i][j].x < x < Recs[i][j].x + s) and (Recs[i][j].y < y < Recs[i][j].y + s):
                Recs[i][j].color = (255,255,255)
                pyglet.clock.schedule_once(Recs[i][j].reset_color,0.1)

                Recs[i-1][j-1].color = (255,255,255)
                Recs[i][j-1].color = (255,255,255)
                Recs[i+1][j-1].color = (255,255,255)

                Recs[i-1][j].color = (255,255,255)
                Recs[i+1][j].color = (255,255,255)

                Recs[i-1][j+1].color = (255,255,255)
                Recs[i][j+1].color = (255,255,255)
                Recs[i+1][j].color = (255,255,255)

                

    pass

@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()
    pass

pyglet.app.run()