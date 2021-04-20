import pyxel
import random

WIDTH = 200
HEIGHT = 100


class TitleBall:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.col = (pyxel.frame_count // 5) % 15 + 1

    def update(self):
        self.x += random.randint(-1, 1)
        self.y -= random.randint(1, 2)
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)
        self.update_col()

    def update_col(self):
        self.col = (pyxel.frame_count // 16) % 15 + 1

    def draw(self):
        pyxel.pset(self.x, self.y, self.col)
