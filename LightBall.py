import pyxel


class LightBall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.col = 7

    def update(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(1, 5)

    def draw(self):
        pyxel.pset(self.x, self.y, self.col)
