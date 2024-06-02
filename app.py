# Copyright 2024, Sam Tygier
# Distributed as LGPL-3.0-only

import app

from events.input import Buttons, BUTTON_TYPES


class ExampleApp(app.App):
    def __init__(self):
        self.counter = 0
        self.button_states = Buttons(self)
        self.scale = 120

    def update(self, delta):
        if self.counter == 256:
            self.counter = 0
        else:
            self.counter += 1

        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        ctx.save()
        ctx.rgb(0.0,0,0).rectangle(-120,-120,240,240).fill()
        for i in range(16):
            z = (self.counter - 16*i) / 256.0
            s = 1 if (i%2 == 0) else -1
            if z > 0.01:
                self.draw_lines(ctx, self.make_cube((8.0 * s * (z**2+0.01), 0), (0.5*z, 1.0*z)))
    
        if self.counter & 16:
            ctx.rgb(1,0,0).move_to(-100,50).text("Hack the planet")
        ctx.restore()


    def make_cube(self, center, size):
        (cx, cy), (sx, sy) = center, size
        #front
        f1, f2, f3, f4 = (cx-sx, cy-sy), (cx-sx, cy+sy), (cx+sx, cy+sy), (cx+sx, cy-sy)
        #back
        bsx, bsy = sx * 0.7, sy*0.7
        b1, b2, b3, b4 = (cx-bsx, cy-bsy), (cx-bsx, cy+bsy), (cx+bsx, cy+bsy), (cx+bsx, cy-bsy)

        return ((f1, f2, f3, f4, f1), (b1, b2, b3, b4, b1), (f1, b1), (f2, b2), (f3, b3), (f4, b4))

    def draw_lines(self, ctx, lines):
        "lines on coords -1 to 1"
        for line_group in lines:
            ctx.rgb(0.2, 0.2, 1).begin_path()
            x1, y1 = line_group[0]
            x1p = int((x1) * self.scale)
            y1p = int((y1) * self.scale)
            ctx.move_to(x1p,y1p)

            for x1, y1 in line_group[1:]:

                x1p = int((x1) * self.scale)
                y1p = int((y1) * self.scale)
                ctx.line_to(x1p,y1p)
            ctx.stroke()

__app_export__ = ExampleApp
