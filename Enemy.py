import pyxel


class Enemy:
    def __init__(self, name, hp, mp, at, df, sp):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.at = at
        self.df = df
        self.sp = sp

        self.max_hp = hp
        self.max_mp = mp

        self.damage = 0

        self.is_alive = True
