import tkinter as tk
import math


class drawcurve(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(width=800, height=400)
        self.canvas.pack(fill="both", expand=True)

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x, y) = coord
        self.canvas.create_oval(x-5, y-5, x+5, y+5,
                                outline=color, fill=color, tags="token")

    def create(self, xA, yA, xB, yB, r, left):
        self._create_token((xA, yA), "white")
        self._create_token((xB, yB), "pink")

        t = math.atan2(yB - yA, xB - xA)
        xC = (xA + xB)/2 + r * math.sin(t)
        yC = (yA + yB)/2 - r * math.cos(t)
        xD = (xA + xB)/2 - r * math.sin(t)
        yD = (yA + yB)/2 + r * math.cos(t)

        if left == 0:
            self.canvas.create_line((xA, yA), (xC, yC), (xB, yB), smooth=True)
        else:
            self.canvas.create_line((xA, yA), (xD, yD), (xB, yB), smooth=True, fill="red")

    def drawenv(self, lens1_r1, lens1_r2, lens1_t, d1, lens2_r1, lens2_r2, lens2_t, d2, lens3_r1, lens3_r2, lens3_t):

        self.create(100, 100, 100, 250, lens1_r1, 1)
        self.create(100 + lens1_t, 100, 100 + lens1_t, 250, lens1_r2, 0)
        self.create(150 + lens1_t + d1, 100, 150 + lens1_t + d1, 250, lens2_r1, 0)
        self.create(150 + lens1_t + d1 + lens2_t, 100, 150 + lens1_t + d1 + lens2_t, 250, lens2_r2, 1)
        self.create(200 + lens1_t + d1 + lens2_t + d2, 100, 200 + lens1_t + d1 + lens2_t + d2, 250, lens3_r1, 1)
        self.create(200 + lens1_t + d1 + lens2_t + d2 + lens3_t, 100, 200 + lens1_t + d1 + lens2_t + d2 + lens3_t,
                          250, lens3_r2, 0)


if __name__ == "__main__":
    curve = drawcurve()
    curve.drawenv(20, 30, 5, 25, 15, 1, 10, 30, 0.000001, 30, 9)
    curve.mainloop()





