# Copyright 2024, Sam Tygier
# Distributed as LGPL-3.0-only

import app
import imu

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
        z_off = imu.acc_read()[1] / 10
        for i in range(16):
            z = (self.counter - 16*i) / 256.0
            s = 1 if (i%2 == 0) else -1
            if z > 0.01:
                lines = self.make_gibson_console(ctx, z, s, z_off)
                if i == 8 and (self.counter & 4):
                    garbage = len(lines) - 5
                else:
                    garbage = False
                self.draw_lines(ctx, lines, garbage)

        if self.counter & 16:
            ctx.rgb(1,0,0).move_to(-100,50).text("Hack the planet")
        ctx.restore()

    def make_gibson_console(self, ctx, z, s, z_off):
        zb = z - (1/64)
        center_front = (8.0 * s * (z**2+0.01)+z_off, 0)
        size_front = (0.5*z, 1.0*z)

        center_back = (8.0 * s * (zb**2+0.01)+z_off, 0)
        size_back = (0.5*zb, 1.0*zb)
        return self.make_cube(center_front, size_front, center_back, size_back)

    def make_cube(self, center, size, center_back, size_back):
        (cx, cy), (sx, sy) = center, size
        #front
        f1, f2, f3, f4 = (cx-sx, cy-sy), (cx-sx, cy+sy), (cx+sx, cy+sy), (cx+sx, cy-sy)
        #back
        (cxb, cyb), (bsx, bsy) = center_back, size_back
        b1, b2, b3, b4 = (cxb-bsx, cyb-bsy), (cxb-bsx, cyb+bsy), (cxb+bsx, cyb+bsy), (cxb+bsx, cyb-bsy)

        frame = [(f1, f2, f3, f4, f1), (b1, b2, b3, b4, b1), (f1, b1), (f2, b2), (f3, b3), (f4, b4)]

        files = []
        for i in range(-3, 4, 1):
            h = cy + (i * sy / 4)
            files.append(((cx-(sx/4), h), (cx+(sx/2), h)))
        return frame + files

    def draw_lines(self, ctx, lines, garbage=False):
        "lines on coords -1 to 1"
        for n, line_group in enumerate(lines):
            if garbage and garbage == n:
              ctx.rgb(1, 0.8, 0.8).begin_path()
            else:
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
