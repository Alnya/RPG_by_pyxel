import pyxel
import random
import math

WIDTH = 200
HEIGHT = 100


class AldoBall:
    def __init__(self):
        col_list = [8, 12, 7, 7]
        self.col = col_list[random.randint(0, 3)]
        self.cx = WIDTH // 2 - 16 + 8
        self.cy = HEIGHT * 3 // 8 - 12 + 8
        self.pi = random.uniform(0, 2 * math.pi)
        self.r = 2
        self.x = 0
        self.y = 0
        self.save_x = 1
        self.save_y = 1

    def update(self):
        self.pi += math.pi / 16
        self.save_x += random.uniform(0, 3)
        self.save_y += random.uniform(0, 3)
        self.x = int(self.cx + math.cos(self.pi) * self.r * self.save_x)
        self.y = int(self.cy + math.sin(self.pi) * self.r * self.save_y)

    def draw(self):
        pyxel.pset(self.x, self.y, self.col)
