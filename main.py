import pyxel
import random
import math

WIDTH = 200
HEIGHT = 100

SPEED = 50

TITLE = 0
SELECTING = 1
RUNNING = 2
WIN = 3
LOSE = 4


class App:
    def __init__(self):
        pyxel.init(width=WIDTH, height=HEIGHT, caption="Guildna")
        pyxel.load("assets/guildna.pyxres")
        self.text_height = HEIGHT // 2
        self.text_width = WIDTH // 32
        self.enemy_height = HEIGHT * 3 // 8 - 16
        self.enemy_width = WIDTH // 2 - 16
        self.player_list = [
            Player(name="Aldo", hp=140, mp=80, at=120, df=100, sp=210, place=self.text_width),
            Player(name="Cyrus", hp=120, mp=100, at=150, df=70, sp=230, place=self.text_width + WIDTH // 4),
            Player(name="Riica", hp=130, mp=150, at=100, df=90, sp=220, place=self.text_width + WIDTH // 2),
            Player(name="Anabel", hp=200, mp=120, at=130, df=130, sp=190, place=self.text_width + (WIDTH * 3) // 4),
        ]
        self.enemy = Enemy(name="Guildna", hp=1000, mp=1000, at=100, df=50, sp=2000)

        self.player_list[0].set_skill(skill_name="X BLADE", skill_type="attack", rate=2, skill_mp=40)
        self.player_list[1].set_skill(skill_name="NIRVANA SLASH", skill_type="attack", rate=1.7, skill_mp=25)
        self.player_list[2].set_skill(skill_name="POWER HEAL", skill_type="heal", rate=0.7, skill_mp=15)
        self.player_list[3].set_skill(skill_name="HOLY SWORD OF PRAYER", skill_type="attack", rate=2, skill_mp=60)

        self.select_list = [
            True,
            True,
            True,
            True,
        ]

        self.action_turn_list = []
        for player in self.player_list:
            self.action_turn_list.append(player)
        self.action_turn_list.append(self.enemy)

        self.mode = TITLE
        self.title_fc = -1
        self.fc = pyxel.frame_count
        self.dead_count = 0

        self.last_attack_log = ""

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_ENTER) and self.mode == TITLE:
            self.title_fc = pyxel.frame_count + 5
        if self.title_fc == pyxel.frame_count:
            self.mode = SELECTING

        if True not in self.select_list and self.mode == SELECTING:
            self.mode = RUNNING
            self.define_action_turn_list()
            self.fc = pyxel.frame_count

        for player in self.player_list:
            if not player.is_alive:
                player.hp = 0
                continue
            if player.hp <= 0 and player.is_alive:
                player.hp = 0
                player.is_alive = False
                player.dead_fc = pyxel.frame_count + 25
            elif player.hp > player.max_hp:
                player.hp = player.max_hp
        if self.enemy.hp <= 0 and self.enemy.is_alive:
            self.enemy.hp = 0
            self.enemy.is_alive = False
            self.mode = WIN
            self.fc = pyxel.frame_count
        for i in range(len(self.player_list)):
            if not self.player_list[i].is_alive:
                self.select_list[i] = False
        count = 0
        for player in self.player_list:
            if not player.is_alive:
                count += 1
        self.dead_count = count
        if self.dead_count == 4 and self.mode != LOSE:
            self.mode = LOSE
            self.fc = pyxel.frame_count

    def update_select(self, index):
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_UP):
            self.player_list[index].is_attack = False if self.player_list[index].is_attack else True
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.select_list[index] = False
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and index > 0:
            self.select_list[index - 1] = True
        self.draw_select(index)

    def draw_select(self, index):
        h = 24 if self.player_list[index].is_attack else 32
        pyxel.text(x=self.player_list[index].place, y=self.text_height + h, s=">", col=3)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=0, v=0, w=16, h=16)

        for player in self.player_list:
            pyxel.text(x=player.place, y=self.text_height, s=player.name, col=7)
            pyxel.text(x=player.place, y=self.text_height + 8, s=f"HP {player.hp}/{player.max_hp}", col=7)
            pyxel.text(x=player.place, y=self.text_height + 16, s=f"MP {player.mp}/{player.max_mp}", col=7)
            pyxel.text(x=player.place, y=self.text_height + 24, s=f" ATTACK", col=7)
            pyxel.text(x=player.place, y=self.text_height + 32, s=f" SKILL", col=7)

        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height, s=self.enemy.name, col=7)
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}", col=7)
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 16, s=f"MP {self.enemy.mp}/{self.enemy.max_mp}",
                   col=7)

        pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=1, u=0, v=(pyxel.frame_count % 11) * 16, w=16, h=16,
                  colkey=0)

        for i in range(len(self.select_list)):
            if not self.select_list[i]:
                self.draw_select(i)
                if self.player_list[i].is_attack:
                    pyxel.text(x=self.player_list[i].place, y=self.text_height + 24, s=f">ATTACK", col=8)
                    pyxel.text(x=self.player_list[i].place, y=self.text_height + 32, s=f">SKILL", col=0)
                else:
                    pyxel.text(x=self.player_list[i].place, y=self.text_height + 32, s=f">SKILL", col=10)
                    pyxel.text(x=self.player_list[i].place, y=self.text_height + 24, s=f">ATTACK", col=0)
        if self.mode == SELECTING:
            for i in range(len(self.select_list)):
                if self.select_list[i]:
                    self.update_select(i)
                    break
        if self.mode == RUNNING:
            frag = True
            for i in range(len(self.action_turn_list)):
                if SPEED * i <= pyxel.frame_count - self.fc < SPEED * (i + 1):
                    attacker = self.action_turn_list[i]
                    frag = False
                    if not attacker.is_alive:
                        pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"{attacker.name}'s ...", col=7)
                        pyxel.text(x=WIDTH // 8, y=HEIGHT // 16 + 8, s=f"But {attacker.name} is dead...", col=8)
                    else:
                        if attacker != self.enemy:
                            self.attack(attacker)
                        else:
                            self.enemy_attack()
            if frag:
                for i in range(len(self.select_list)):
                    self.select_list[i] = True
                for player in self.player_list:
                    player.damaged = False
                self.enemy.damaged = False
                self.mode = SELECTING
        self.dead_draw()
        if self.mode == WIN:
            pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                       col=8)
            if 0 <= pyxel.frame_count - self.fc < 50:
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=self.last_attack_log, col=7)
                pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                           s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                           col=0)
                pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                           s=f"HP {random.randint(1, self.enemy.max_hp)}/{self.enemy.max_hp}",
                           col=14)
                self.attack_effect()
            elif 50 <= pyxel.frame_count - self.fc < 130:
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"VICTORY!!!!!!!\nYOUWIN!!!!!!!!!!!!", col=10)
                if pyxel.frame_count - self.fc < 80:
                    self.effect_when_enemy_is_attacked()
            else:
                pyxel.cls(7)
                pyxel.text(x=WIDTH // 2 - 24, y=HEIGHT // 2 - 4, s=f"GAME CLEAR", col=10)
        if self.mode == LOSE:
            if 0 <= pyxel.frame_count - self.fc < 51:
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=self.last_attack_log, col=8)
            elif 51 <= pyxel.frame_count - self.fc < 130:
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"ANNIHILATION...\nYOULOSE............", col=8)
            else:
                pyxel.cls(0)
                pyxel.text(x=WIDTH // 2 - 24, y=HEIGHT // 2 - 4, s=f"GAME OVER", col=8)
        if self.mode == TITLE:
            self.title_draw()

    def title_draw(self):
        pyxel.cls(0)
        pyxel.text(x=WIDTH // 2 - 24, y=HEIGHT // 2 - 4, s=f"GAME START", col=7 if pyxel.frame_count % 40 < 20 else 8)
        pyxel.text(x=WIDTH // 2 - 27, y=HEIGHT * 3 // 4 - 8, s=f"PRESS  ENTER",
                   col=9 if pyxel.frame_count % 6 < 3 else 10)

    def dead_draw(self):
        for player in self.player_list:
            if player.dead_fc > pyxel.frame_count:
                pyxel.text(x=player.place, y=self.text_height + 8, s=f"HP {player.hp}/{player.max_hp}", col=0)
                pyxel.text(x=player.place, y=self.text_height + 8,
                           s=f"HP {random.randint(1, player.max_hp)}/{player.max_hp}", col=14)
            elif not player.is_alive:
                pyxel.text(x=player.place, y=self.text_height, s=player.name, col=13)
                pyxel.text(x=player.place, y=self.text_height + 8, s=f"HP {player.hp}/{player.max_hp}", col=13)
                pyxel.text(x=player.place, y=self.text_height + 16, s=f"MP {player.mp}/{player.max_mp}", col=13)
                pyxel.text(x=player.place, y=self.text_height + 24, s=f" ATTACK", col=13)
                pyxel.text(x=player.place, y=self.text_height + 32, s=f" SKILL", col=13)
                pyxel.text(x=player.place, y=self.text_height + 24, s=f">", col=0)
                pyxel.text(x=player.place, y=self.text_height + 32, s=f">", col=0)

    def define_action_turn_list(self):
        dic = {}
        for player in self.player_list:
            dic[player] = player.sp * random.uniform(0.9, 1.1)
        dic[self.enemy] = self.enemy.sp * random.uniform(0.9, 1.1)
        ls = sorted(dic.items(), key=lambda x: -x[1])
        self.action_turn_list = []
        for i in ls:
            if not i[0].is_alive:
                continue
            self.action_turn_list.append(i[0])

    def attack(self, player):
        # pyxel.blt(x=self.enemy_width - 8, y=self.enemy_height - 8, img=2, u=0, v=0, w=31, h=31, colkey=0)
        # effect_fc = ((pyxel.frame_count - self.fc) % SPEED - 10) * 31 // 10
        # pyxel.blt(x=self.enemy_width - 8, y=self.enemy_height - 8 + effect_fc, img=2, u=0, v=effect_fc, w=31,
        #           h=31,
        #           colkey=0)
        # self.attack_effect()
        if player.is_attack:
            if not player.damaged:
                player.damage = int(player.at * random.uniform(0.9, 1.1)) - int(
                    self.enemy.df * random.uniform(0.4, 0.6))
                self.enemy.hp -= player.damage
                player.damaged = True
            if (pyxel.frame_count - self.fc) % 50 < 25:
                show_hp = random.randint(1, self.enemy.max_hp)
                pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                           s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                           col=0)
                pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {show_hp}/{self.enemy.max_hp}",
                           col=14)
            else:
                show_hp = self.enemy.hp
                pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                           s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                           col=0)
                pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {show_hp}/{self.enemy.max_hp}",
                           col=8)
            pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"{player.name}'s ATTACK!!", col=7)
            pyxel.text(x=WIDTH // 8, y=HEIGHT // 16 + 8, s=f"{player.damage} damages to {self.enemy.name}!", col=7)
            self.last_attack_log = f"{player.name}'s ATTACK!!\n{player.damage} damages to {self.enemy.name}!"
            # pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
            #            col=0)
            # pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {show_hp}/{self.enemy.max_hp}",
            #            col=14)
            if 25 <= (pyxel.frame_count - self.fc) % 50 < 30:
                self.effect_when_enemy_is_attacked()
            self.attack_effect()
        else:
            mp_after_skill = 1
            if not player.damaged:
                mp_after_skill = player.mp - player.skill_mp
            if mp_after_skill < 0:
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"{player.name}'s SKILL! {player.skill_name}!!", col=7)
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16 + 8, s=f"BUT NOT ENOUGH MP...", col=8)
            else:
                if not player.damaged:
                    player.mp = mp_after_skill
                    player.damage = int(player.at * player.rate)
                    if player.skill_type == "attack":
                        player.damage -= self.enemy.df
                        self.enemy.hp -= player.damage
                    elif player.skill_type == "heal":
                        for p in self.player_list:
                            if p.is_alive:
                                p.hp += player.damage
                    player.damaged = True
                pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"{player.name}'s SKILL! {player.skill_name}!!", col=7)
                if player.skill_type == "attack":
                    if (pyxel.frame_count - self.fc) % 50 < 25:
                        show_hp = random.randint(1, self.enemy.max_hp)
                        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                                   s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                                   col=0)
                        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                                   s=f"HP {show_hp}/{self.enemy.max_hp}",
                                   col=14)
                    else:
                        show_hp = self.enemy.hp
                        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                                   s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                                   col=0)
                        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                                   s=f"HP {show_hp}/{self.enemy.max_hp}",
                                   col=8)
                    pyxel.text(x=WIDTH // 8, y=HEIGHT // 16 + 8, s=f"{player.damage} damages to {self.enemy.name}!",
                               col=7)
                    # pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                    #            s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                    #            col=0)
                    # pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {show_hp}/{self.enemy.max_hp}",
                    #            col=14)
                    self.last_attack_log = f"{player.name}'s SKILL! {player.skill_name}!!\n{player.damage} " \
                                           f"damages to {self.enemy.name}!"
                    if 25 <= (pyxel.frame_count - self.fc) % 50 < 30:
                        self.effect_when_enemy_is_attacked()
                    if player.name == "Aldo":
                        self.x_blade_effect()
                    else:
                        self.attack_effect()
                elif player.skill_type == "heal":
                    pyxel.text(x=WIDTH // 8, y=HEIGHT // 16 + 8, s=f"Everyone gets {player.damage} points of heal!!",
                               col=7)
                    for p in self.player_list:
                        pyxel.text(x=p.place, y=self.text_height + 8, s=f"HP {p.hp}/{p.max_hp}", col=3)
                        if (pyxel.frame_count - self.fc) % 50 < 25 and p.is_alive:
                            pyxel.text(x=p.place, y=self.text_height + 8, s=f"HP {p.hp}/{p.max_hp}", col=0)
                            pyxel.text(x=p.place, y=self.text_height + 8,
                                       s=f"HP {random.randint(1, p.max_hp)}/{p.max_hp}", col=3)
                    self.heal_effect()
                pyxel.text(x=player.place, y=self.text_height + 16, s=f"MP {player.mp}/{player.max_mp}", col=12)
                if (pyxel.frame_count - self.fc) % 50 < 25:
                    pyxel.text(x=player.place, y=self.text_height + 16, s=f"MP {player.mp}/{player.max_mp}", col=0)
                    pyxel.text(x=player.place, y=self.text_height + 16,
                               s=f"MP {random.randint(1, player.max_mp)}/{player.max_mp}", col=12)

    def effect_when_player_is_attacked(self, player):
        pyxel.text(x=player.place, y=self.text_height, s=player.name, col=0)
        pyxel.text(x=player.place, y=self.text_height + 8, s=f"HP {player.hp}/{player.max_hp}", col=0)
        pyxel.text(x=player.place, y=self.text_height + 16, s=f"MP {player.mp}/{player.max_mp}", col=0)
        x = random.randint(-2, 2)
        y = random.randint(-2, 2)
        pyxel.text(x=player.place + x, y=self.text_height + y, s=player.name, col=7)
        pyxel.text(x=player.place + x, y=self.text_height + 8 + y, s=f"HP {player.hp}/{player.max_hp}", col=8)
        pyxel.text(x=player.place + x, y=self.text_height + 16 + y, s=f"MP {player.mp}/{player.max_mp}", col=7)

    def effect_when_enemy_is_attacked(self):
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height, s=self.enemy.name, col=0)
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}", col=0)
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 16, s=f"MP {self.enemy.mp}/{self.enemy.max_mp}",
                   col=0)
        x = random.randint(-2, 2)
        y = random.randint(-2, 2)
        pyxel.text(x=self.enemy_width + 32 + x, y=self.enemy_height + y, s=self.enemy.name, col=7)
        pyxel.text(x=self.enemy_width + 32 + x, y=self.enemy_height + 8 + y,
                   s=f"HP {self.enemy.hp}/{self.enemy.max_hp}", col=8)
        pyxel.text(x=self.enemy_width + 32 + x, y=self.enemy_height + 16 + y,
                   s=f"MP {self.enemy.mp}/{self.enemy.max_mp}",
                   col=7)
        x = random.randint(-2, 2)
        y = random.randint(-2, 2)
        pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=16, v=16, w=16, h=16)
        pyxel.blt(x=self.enemy_width + x, y=self.enemy_height + y, img=0, u=0, v=0, w=16, h=16)

    def attack_effect(self):
        # pyxel.blt(x=self.enemy_width - 8, y=self.enemy_height - 8, img=2, u=0, v=0, w=31, h=31, colkey=0)
        effect_sp = 3
        length = 12
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED) * effect_sp
        x = self.enemy_width - 8
        y = self.enemy_height - 8
        u = 0
        v = 0
        w = 32
        h = 32
        frag = True

        if effect_fc < length:
            h = effect_fc
        elif effect_fc < 32:
            y += effect_fc - length
            v += effect_fc - length
            h = length
        elif effect_fc < 32 + length:
            y += effect_fc - length
            v += effect_fc - length
            h = 32 + length - effect_fc
        else:
            frag = False
        if frag:
            pyxel.blt(x, y, 2, u, v, w, h, 0)

    def x_blade_effect(self):
        effect_sp = 2
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED) * effect_sp
        x = self.enemy_width - 8
        y = self.enemy_height - 8
        u = 0
        v = 32
        w = 32
        h = 32
        frag = True
        frag_2 = True

        x += random.randint(-1, 1)
        y += random.randint(-1, 1)

        if effect_fc < 32:
            h = effect_fc
        else:
            frag = False
        if frag:
            pyxel.blt(x, y, 2, u, v, w, h, 0)
        else:
            effect_fc -= 32
            if effect_fc < 32:
                h = effect_fc
            else:
                frag_2 = False
            if frag_2:
                pyxel.blt(x, y, 2, u, v, w, 32, 0)
                pyxel.blt(x, y, 2, u, v + 32, w, h, 0)
            else:
                pyxel.blt(self.enemy_width - 8, self.enemy_height - 8, 2, u, v, w, 32, 0)
                pyxel.blt(self.enemy_width - 8, self.enemy_height - 8, 2, u, v + 32, w, 32, 0)

        r = (effect_fc + 1) * 3
        x = self.enemy_width + 8
        y = self.enemy_height + 8
        for _ in range(r * 2):
            a = random.randint(-r, r)
            c = int(math.sqrt((r ** 2) - (a ** 2)))
            b = random.randint(-c, c)
            u = random.randint(32, 34)
            v = 8
            w = 1
            h = 1
            pyxel.blt(x + a, y + b, 2, u, v, w, h, 0)

    def heal_effect(self):
        if (pyxel.frame_count - self.fc) % SPEED < 50:
            start = (((pyxel.frame_count - self.fc) % SPEED) * (WIDTH - 7) // 20) - 140
            end = (((pyxel.frame_count - self.fc) % SPEED) * (WIDTH - 7) // 20) + 70
            for _ in range(20):
                pyxel.blt(
                    x=random.randint(start, end),
                    y=random.randint(self.text_height, HEIGHT - 7),
                    img=2,
                    u=32,
                    v=0,
                    w=7,
                    h=7,
                    colkey=0
                )

    def enemy_attack(self):
        if not self.enemy.damaged:
            self.enemy.damage = int(self.enemy.at * random.uniform(0.9, 1.1))
            for player in self.player_list:
                player.hp -= self.enemy.damage - int(player.df * random.uniform(0.4, 0.6))
            self.enemy.damaged = True
        pyxel.text(x=WIDTH // 8, y=HEIGHT // 16, s=f"{self.enemy.name}'s ATTACK!!", col=7)
        pyxel.text(x=WIDTH // 8, y=HEIGHT // 16 + 8, s=f"Everyone accepted damages from {self.enemy.name}!",
                   col=7)
        self.last_attack_log = f"{self.enemy.name}'s ATTACK!!\nEveryone accepted damages from {self.enemy.name}!"
        for player in self.player_list:
            pyxel.text(x=player.place, y=self.text_height + 8, s=f"HP {player.hp}/{player.max_hp}", col=8)
            if (pyxel.frame_count - self.fc) % 50 < 25 and player.is_alive:
                pyxel.text(x=player.place, y=self.text_height + 8, s=f"HP {player.hp}/{player.max_hp}", col=0)
                pyxel.text(x=player.place, y=self.text_height + 8,
                           s=f"HP {random.randint(1, player.max_hp)}/{player.max_hp}", col=14)
            elif 25 <= (pyxel.frame_count - self.fc) % 50 < 30 and player.is_alive:
                self.effect_when_player_is_attacked(player)


class Player:
    def __init__(self, name, hp, mp, at, df, sp, place):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.at = at
        self.df = df
        self.sp = sp
        self.place = place

        self.max_hp = hp
        self.max_mp = mp

        self.is_attack = True
        self.damaged = False
        self.damage = 0
        self.skill_type = "attack"
        self.rate = 1
        self.skill_name = ""
        self.skill_mp = 0
        self.dead_fc = -1

        self.is_alive = True

    def set_skill(self, skill_name, skill_type, rate, skill_mp):
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.rate = rate
        self.skill_mp = skill_mp


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

        self.damaged = False
        self.damage = 0

        self.is_alive = True


App()
