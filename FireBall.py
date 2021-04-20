import pyxel
import random

WIDTH = 200
HEIGHT = 100


class FireBall:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT // 2)
        self.col_v = random.randint(8, 9)

    def update(self):
        self.x += random.randint(-1, 1)
        self.y -= 1 if random.randint(0, 5) < 5 else 0
        if self.x < 0:
            self.x = WIDTH
            self.col_v = random.randint(8, 9)
        elif self.x > WIDTH:
            self.x = 0
            self.col_v = random.randint(8, 9)
        if self.y < 0:
            self.y = HEIGHT // 2
            self.col_v = random.randint(8, 9)
        elif self.y > HEIGHT // 2:
            self.y = 0
            self.col_v = random.randint(8, 9)

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 32, self.col_v, 1, 1, 0)
