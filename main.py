import pyxel
import random
import math

WIDTH = 200
HEIGHT = 100

SPEED = 100

TITLE = 0
SELECTING = 1
RUNNING = 2
WIN = 3
LOSE = 4


class App:
    def __init__(self):
        pyxel.init(width=WIDTH, height=HEIGHT, caption="Guildna")
        pyxel.load("assets/guildna.pyxres")
        self.text_h = HEIGHT // 16
        self.text_w = WIDTH // 8
        self.player_h = HEIGHT // 2 + 6
        self.player_w = WIDTH // 32
        self.enemy_height = HEIGHT * 3 // 8 - 12
        self.enemy_width = WIDTH // 2 - 16
        self.player_list = [
            Player(name="Aldo", hp=160, mp=80, at=120, df=100, sp=300, place=self.player_w),
            Player(name="Cyrus", hp=130, mp=100, at=150, df=90, sp=330, place=self.player_w + WIDTH // 4),
            Player(name="Riica", hp=150, mp=150, at=100, df=100, sp=320, place=self.player_w + WIDTH // 2),
            Player(name="Anabel", hp=200, mp=120, at=100, df=110, sp=290, place=self.player_w + (WIDTH * 3) // 4),
        ]
        self.enemy = Enemy(name="Guildna", hp=2000, mp="????", at=100, df=10, sp=310)

        self.player_list[0].set_skill(skill_name="X BLADE", skill_type="attack", rate=5, skill_mp=40)
        self.player_list[1].set_skill(skill_name="NIRVANA SLASH", skill_type="attack", rate=1.7, skill_mp=20)
        self.player_list[2].set_skill(skill_name="POWER HEAL", skill_type="heal", rate=0.7, skill_mp=15)
        self.player_list[3].set_skill(skill_name="HOLY SWORD OF PRAYER", skill_type="attack", rate=2, skill_mp=30)

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
        self.alive_list = []

        self.light_ball_list = []
        self.aldo_ball_list = []
        self.fire_ball_list = []
        for _ in range(20):
            self.fire_ball_list.append(FireBall())
        self.title_ball_list = []
        for _ in range(10):
            self.title_ball_list.append(TitleBall())

        self.mode = TITLE
        self.fc = -1
        self.title_fc = -1
        self.dead_count = 0

        self.win_fc = -1
        self.lose_fc = -1

        pyxel.play(ch=0, snd=4, loop=True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_title()
        self.update_select()
        self.update_hp()
        self.update_select_list_dead()
        self.update_win()
        self.lose_judge()
        self.update_lose()
        self.reset_running_to_selecting()
        self.update_fire_ball()

    def update_title(self):
        if self.mode == TITLE:
            if pyxel.btnp(pyxel.KEY_ENTER) and self.fc == -1:
                self.fc = pyxel.frame_count + SPEED
                self.title_fc = pyxel.frame_count + SPEED * 2
            if self.title_fc == pyxel.frame_count:
                self.mode = SELECTING
                pyxel.playm(1, loop=True)

    def update_select(self):
        if self.mode == SELECTING:
            for i in range(len(self.select_list)):
                if self.select_list[i]:
                    self.update_select_list(i)
                    break
        if True not in self.select_list and self.mode == SELECTING:
            self.mode = RUNNING
            self.define_action_turn_list()
            self.fc = pyxel.frame_count

    def update_hp(self):
        for player in self.player_list:
            if not player.is_alive:
                player.hp = 0
                continue
            if player.hp <= 0 and player.is_alive:
                player.hp = 0
                player.is_alive = False
                player.dead_fc = pyxel.frame_count + SPEED * 3 // 10
            elif player.hp > player.max_hp:
                player.hp = player.max_hp
        if self.enemy.hp <= 0 and self.enemy.is_alive:
            self.enemy.hp = 0
            self.enemy.is_alive = False
            self.win_fc = pyxel.frame_count + SPEED // 2

    def update_win(self):
        if self.win_fc == pyxel.frame_count:
            self.mode = WIN

    def update_lose(self):
        if self.lose_fc == pyxel.frame_count:
            self.mode = LOSE

    def update_select_list_dead(self):
        for i in range(len(self.player_list)):
            if not self.player_list[i].is_alive:
                self.select_list[i] = False

    def lose_judge(self):
        count = 0
        for player in self.player_list:
            if not player.is_alive:
                count += 1
        self.dead_count = count
        if self.dead_count == 4 and self.lose_fc == -1 and self.mode == SELECTING:
            self.lose_fc = pyxel.frame_count + 1

    def update_select_list(self, index):
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_UP):
            self.player_list[index].is_attack = False if self.player_list[index].is_attack else True
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.select_list[index] = False
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and index > 0:
            self.select_list[index - 1] = True

    def reset_running_to_selecting(self):
        if self.mode == RUNNING and pyxel.frame_count - self.fc == SPEED * len(self.action_turn_list):
            for i in range(len(self.select_list)):
                self.select_list[i] = True
            self.mode = SELECTING

    def update_fire_ball(self):
        for ball in self.fire_ball_list:
            ball.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=0, v=16 * ((pyxel.frame_count // 4) % 8), w=16,
                  h=16)
        self.draw_players_and_enemy()
        self.draw_fire_ball()

        self.draw_selected_choices()
        self.draw_select()

        self.draw_running()
        self.check_player_mp()
        self.draw_dead()
        self.draw_win()
        self.draw_lose()
        if self.mode == TITLE:
            self.draw_title()

    def draw_lose(self):
        if self.mode == LOSE:
            if pyxel.frame_count - self.lose_fc == 0:
                pyxel.stop()
                pyxel.play(0, 16)
            if 0 <= pyxel.frame_count - self.lose_fc < SPEED * 2:
                message = "ANNIHILATION...\nYOU LOSE............"
                ans = self.return_message(message, pyxel.frame_count - self.lose_fc)
                pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=8)
            else:
                pyxel.cls(0)
                message = "GAME OVER"
                ans = self.return_message(message, pyxel.frame_count - self.lose_fc - SPEED * 2)
                pyxel.text(x=WIDTH // 2 - 24, y=HEIGHT // 2 - 4, s=f"{ans}", col=8)

    def draw_win(self):
        if self.mode == WIN:
            pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}",
                       col=8)
            if pyxel.frame_count - self.win_fc == 0:
                pyxel.stop()
            elif pyxel.frame_count - self.win_fc == SPEED // 2:
                pyxel.play(0, 15)
            if 0 <= pyxel.frame_count - self.win_fc < SPEED // 2:
                self.hide_enemy_image()
                self.effect_when_enemy_is_attacked()
            elif SPEED // 2 <= pyxel.frame_count - self.win_fc < SPEED * 2:
                message = "VICTORY!!!!!!!\nYOU WIN!!!!!!!!!!!!!"
                ans = self.return_message(message, pyxel.frame_count - self.win_fc - SPEED // 2)
                pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=10)
                self.hide_enemy_image()
                v = ((pyxel.frame_count - self.win_fc - SPEED // 2) // 5) * 16
                if 14 * 16 < v:
                    v = 14 * 16
                pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=80, v=v, w=16, h=16, colkey=0)
            else:
                pyxel.cls(7)
                message = "Congratulations!"
                ans = self.return_message(message, pyxel.frame_count - self.win_fc - SPEED * 2)
                pyxel.text(x=WIDTH // 4 + 16, y=HEIGHT // 2 - 4, s=f"{ans}", col=10)

    @staticmethod
    def return_message(message, fc) -> str:
        ans = ""
        for i in range(len(message)):
            if i < fc:
                ans += message[i]
        return ans

    def draw_running(self):
        if self.mode == RUNNING:
            for i in range(len(self.action_turn_list)):
                if SPEED * i <= pyxel.frame_count - self.fc < SPEED * (i + 1):
                    attacker = self.action_turn_list[i]
                    if attacker.is_alive:
                        if attacker != self.enemy:
                            self.attack(attacker)
                        else:
                            self.enemy_attack()
                    else:
                        message = f"{attacker.name}'s ..."
                        ans = self.return_message(message, pyxel.frame_count - self.fc - SPEED * i)
                        pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=7)
                        if SPEED * i + SPEED // 3 <= pyxel.frame_count - self.fc:
                            message = f"But {attacker.name} is dead..."
                            ans = self.return_message(message, pyxel.frame_count - self.fc - SPEED * i - SPEED // 3)
                            pyxel.text(x=self.text_w, y=self.text_h + 8, s=f"{ans}", col=8)

    def draw_players_and_enemy(self):
        for player in self.player_list:
            pyxel.text(x=player.place, y=self.player_h, s=player.name, col=7)
            pyxel.text(x=player.place, y=self.player_h + 8, s=f"HP {player.hp}/{player.max_hp}", col=7)
            pyxel.text(x=player.place, y=self.player_h + 16, s=f"MP {player.mp}/{player.max_mp}", col=7)
            pyxel.text(x=player.place, y=self.player_h + 24, s=f" ATTACK", col=7)
            pyxel.text(x=player.place, y=self.player_h + 32, s=f" SKILL", col=7)

        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height, s=self.enemy.name, col=7)
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}", col=7)
        pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 16, s=f"MP {self.enemy.mp}/{self.enemy.max_mp}",
                   col=7)

    def draw_select(self):
        if self.mode == SELECTING:
            for i in range(len(self.select_list)):
                if self.select_list[i]:
                    h = 24 if self.player_list[i].is_attack else 32
                    pyxel.text(x=self.player_list[i].place, y=self.player_h + h, s=">", col=3)
                    break

    def draw_selected_choices(self):
        for i in range(len(self.select_list)):
            if not self.select_list[i]:
                if self.player_list[i].is_attack:
                    pyxel.text(x=self.player_list[i].place, y=self.player_h + 24, s=f">ATTACK", col=14)
                    pyxel.text(x=self.player_list[i].place, y=self.player_h + 32, s=f">SKILL", col=0)
                else:
                    pyxel.text(x=self.player_list[i].place, y=self.player_h + 32, s=f">SKILL", col=10)
                    pyxel.text(x=self.player_list[i].place, y=self.player_h + 24, s=f">ATTACK", col=0)

    def draw_fire_ball(self):
        for ball in self.fire_ball_list:
            ball.draw()

    def draw_title(self):
        pyxel.cls(0)
        pyxel.text(x=WIDTH // 2 - 24, y=HEIGHT // 2 - 4, s=f"GAME START", col=7 if pyxel.frame_count % 40 < 20 else 8)
        pyxel.text(x=WIDTH // 2 - 27, y=HEIGHT * 3 // 4 - 8, s=f"PRESS  ENTER",
                   col=9 if pyxel.frame_count % 6 < 3 else 10)
        for ball in self.title_ball_list:
            ball.update()
            ball.draw()
        efc = pyxel.frame_count - self.fc + SPEED
        if self.fc != -1:
            pyxel.cls(0)
            if 0 <= efc < SPEED // 2:
                period_count = (pyxel.frame_count // 8) % 4
                period = ""
                for _ in range(period_count):
                    period += "."
                pyxel.text(x=WIDTH - 60, y=HEIGHT - 10, s=f"Now loading{period}", col=7)
            elif SPEED // 2 <= efc < SPEED // 2 + self.enemy_height + 16:
                pyxel.blt(x=self.enemy_width, y=efc - SPEED // 2 - 16, img=0, u=0,
                          v=16 * ((pyxel.frame_count // 4) % 8),
                          w=16, h=16)
            elif SPEED // 2 + self.enemy_height + 16 <= efc < SPEED:
                pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=0, v=16 * ((pyxel.frame_count // 4) % 8),
                          w=16, h=16)
            elif SPEED <= efc:
                self.draw_enemy_attack_self(pyxel.frame_count % 2)
                for i in range(len(self.player_list)):
                    player = self.player_list[i]
                    self.draw_enemy_attack_fire(player, i * 2)
                    self.draw_enemy_attack_fire(player, i * 2 + 8)
            if efc == SPEED - 5:
                pyxel.stop()

    def draw_dead(self):
        for player in self.player_list:
            if player.dead_fc > pyxel.frame_count:
                self.effect_when_player_is_attacked(player)
            elif not player.is_alive:
                pyxel.text(x=player.place, y=self.player_h, s=player.name, col=13)
                pyxel.text(x=player.place, y=self.player_h + 8, s=f"HP {player.hp}/{player.max_hp}", col=13)
                pyxel.text(x=player.place, y=self.player_h + 16, s=f"MP {player.mp}/{player.max_mp}", col=13)
                pyxel.text(x=player.place, y=self.player_h + 24, s=f" ATTACK", col=13)
                pyxel.text(x=player.place, y=self.player_h + 32, s=f" SKILL", col=13)
                pyxel.text(x=player.place, y=self.player_h + 24, s=f">", col=0)
                pyxel.text(x=player.place, y=self.player_h + 32, s=f">", col=0)

    def check_player_mp(self):
        for player in self.player_list:
            if player.is_alive and player.mp == 0:
                self.draw_player_mp_red(player)

    def define_action_turn_list(self):
        dic = {}
        for player in self.player_list:
            dic[player] = player.sp * random.uniform(0.9, 1.1)
        dic[self.enemy] = self.enemy.sp * random.uniform(0.9, 1.1)
        ls = sorted(dic.items(), key=lambda x: -x[1])
        self.action_turn_list = []
        for i, v in ls:
            if not i.is_alive:
                continue
            self.action_turn_list.append(i)

    def attack(self, player):
        efc = (pyxel.frame_count - self.fc) % SPEED
        self.attacker_status_effect(player)

        if player.is_attack or player.skill_type == "attack" and player.mp_after_skill >= 0:
            if SPEED // 2 <= efc:
                message = f"{player.damage} damage to {self.enemy.name}!"
                ans = self.return_message(message, efc - SPEED // 2)
                pyxel.text(x=self.text_w, y=self.text_h + 8, s=f"{ans}", col=7)

        if player.is_attack:
            if efc == SPEED // 2 - 1:
                player.damage = int(player.at * random.uniform(0.9, 1.1)) - int(
                    self.enemy.df * random.uniform(0.4, 0.6))
                self.enemy.hp -= player.damage
            message = f"{player.name}'s ATTACK!!"
            ans = self.return_message(message, efc)
            pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=7)
            self.draw_attacked_enemy_hp()
            self.attack_effect(player)
        else:
            if efc == 0:
                player.mp_after_skill = player.mp - player.skill_mp
            if player.mp_after_skill < 0:
                message = f"{player.name}'s SKILL! {player.skill_name}!!"
                ans = self.return_message(message, efc)
                pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=7)
                if SPEED // 2 <= efc:
                    message = f"BUT {player.name} HAS NOT ENOUGH MP..."
                    ans = self.return_message(message, efc - SPEED // 2)
                    pyxel.text(x=self.text_w, y=self.text_h + 8, s=f"{ans}", col=8)
            else:
                if player.skill_type == "heal":
                    if efc == 0:
                        player.mp = player.mp_after_skill
                        player.damage = int(player.at * player.rate * random.uniform(0.9, 1.1))
                elif efc == SPEED // 2 - 1:
                    player.mp = player.mp_after_skill
                    player.damage = int(player.at * player.rate * random.uniform(0.9, 1.1))
                    if player.skill_type == "attack":
                        player.damage -= self.enemy.df
                        self.enemy.hp -= player.damage

                message = f"{player.name}'s SKILL! {player.skill_name}!!"
                ans = self.return_message(message, efc)
                pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=7)
                if player.skill_type == "attack":
                    self.draw_attacked_enemy_hp()
                    if SPEED // 2 <= efc < SPEED // 2 + 5:
                        self.effect_when_enemy_is_attacked()
                    if player.name == "Aldo":
                        self.x_blade_effect()
                    elif player.name == "Cyrus":
                        self.nirvana_slash_effect()
                    elif player.name == "Anabel":
                        self.holy_sword_of_prayer()
                    else:
                        self.attack_effect(player)
                elif player.skill_type == "heal":
                    if efc == 0:
                        self.alive_list = []
                        for player in self.player_list:
                            if player.is_alive:
                                self.alive_list.append(player)
                    if SPEED // 2 <= efc:
                        message = f"Everyone gets {player.damage} points of heal!!"
                        ans = self.return_message(message, efc - SPEED // 2)
                        pyxel.text(x=self.text_w, y=self.text_h + 8, s=f"{ans}", col=7)
                    for i in range(len(self.alive_list)):
                        p = self.alive_list[i]
                        if SPEED // 4 + i * 9 == efc:
                            p.hp += player.damage
                            pyxel.play(1, 11)
                        if SPEED // 4 + i * 9 <= efc:
                            pyxel.text(x=p.place, y=self.player_h + 8, s=f"HP {p.hp}/{p.max_hp}", col=3)
                    self.heal_effect()

    def draw_attacked_enemy_hp(self):
        if SPEED // 2 == (pyxel.frame_count - self.fc) % SPEED:
            pyxel.play(1, 10)
        if SPEED // 2 <= (pyxel.frame_count - self.fc) % SPEED < SPEED // 2 + 5:
            self.effect_when_enemy_is_attacked()
        elif SPEED // 2 + 5 <= (pyxel.frame_count - self.fc) % SPEED:
            pyxel.text(x=self.enemy_width + 32, y=self.enemy_height + 8,
                       s=f"HP {self.enemy.hp}/{self.enemy.max_hp}", col=8)

    def attacker_status_effect(self, player):
        pyxel.text(x=player.place, y=self.player_h, s=player.name, col=0)
        if 0 <= (pyxel.frame_count - self.fc) % SPEED < 5:
            y = self.player_h - (pyxel.frame_count - self.fc) % SPEED
        elif 5 <= (pyxel.frame_count - self.fc) % SPEED < SPEED - 4:
            y = self.player_h - 4
        else:
            y = self.player_h + (pyxel.frame_count - self.fc) % SPEED - SPEED
        pyxel.text(x=player.place, y=y, s=player.name, col=7)

    def effect_when_player_is_attacked(self, player):
        self.hide_player_status(player)
        x = random.randint(-2, 2)
        y = random.randint(-2, 2)
        pyxel.text(x=player.place + x, y=self.player_h + y, s=player.name, col=7)
        pyxel.text(x=player.place + x, y=self.player_h + 8 + y, s=f"HP {player.hp}/{player.max_hp}", col=8)
        pyxel.text(x=player.place + x, y=self.player_h + 16 + y, s=f"MP {player.mp}/{player.max_mp}", col=7)

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
                   s=f"MP {self.enemy.mp}/{self.enemy.max_mp}", col=7)
        x = random.randint(-2, 2)
        y = random.randint(-2, 2)
        pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=16, v=16, w=16, h=16)
        pyxel.blt(x=self.enemy_width + x, y=self.enemy_height + y, img=0, u=0, v=0, w=16, h=16)

    def attack_effect(self, player):
        effect_sp = 3
        length = 12
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED - SPEED // 3) * effect_sp
        x = self.enemy_width - 8
        y = self.enemy_height - 8
        u = 0
        if player.name == "Aldo" or player.name == "Anabel":
            u = 0
        elif player.name == "Cyrus":
            u = 48
        elif player.name == "Riica":
            u = 80
        v = 0
        w = 32
        h = 32
        frag = True

        if 0 <= effect_fc < length:
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

        if effect_fc == 0:
            if player.name == "Aldo" or player.name == "Anabel":
                pyxel.play(0, 7)
            elif player.name == "Cyrus":
                pyxel.play(0, 8)
            elif player.name == "Riica":
                pyxel.play(0, 9)

    def x_blade_effect(self):
        effect_sp = 2
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED) * effect_sp
        x = self.enemy_width - 8
        y = self.enemy_height - 8
        u = 0 if pyxel.frame_count % 2 == 0 else 32
        v = 32
        w = 32
        h = 32
        frag = True
        frag_2 = True

        x += random.randint(-1, 1)
        y += random.randint(-1, 1)

        if effect_fc == 0:
            pyxel.play(0, 12)

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

        if (pyxel.frame_count - self.fc) % SPEED == 0:
            self.aldo_ball_list = []
        elif 10 <= (pyxel.frame_count - self.fc) % SPEED < 15:
            for _ in range(10):
                self.aldo_ball_list.append(AldoBall())
        elif 35 <= (pyxel.frame_count - self.fc) % SPEED < 45:
            for _ in range(10):
                self.aldo_ball_list.append(AldoBall())
        for ball in self.aldo_ball_list:
            ball.update()
            ball.draw()

    def nirvana_slash_effect(self):
        if (pyxel.frame_count - self.fc) % SPEED == 0:
            pyxel.play(0, 13, loop=True)
        elif (pyxel.frame_count - self.fc) % SPEED == SPEED - 1:
            pyxel.play(0, 50)
        theta = ((pyxel.frame_count - self.fc) % SPEED) // 2
        x1 = int(math.cos(theta) * 10) + self.enemy_width
        y1 = int(math.sin(theta) * 10) + self.enemy_height
        x2 = int(math.cos(theta + 2 * math.pi / 3) * 10) + self.enemy_width + 16
        y2 = int(math.sin(theta + 2 * math.pi / 3) * 10) + self.enemy_height
        x3 = int(math.cos(theta + 4 * math.pi / 3) * 10) + self.enemy_width + 8
        y3 = int(math.sin(theta + 4 * math.pi / 3) * 10) + self.enemy_height + 16
        pyxel.trib(x1, y1, x2, y2, x3, y3, 7)
        u = 34
        v = 8
        w = 1
        h = 1
        min_x = min(x1, x2, x3) - 16
        max_x = max(x1, x2, x3) + 16
        min_y = min(y1, y2, y3) - 16
        max_y = max(y1, y2, y3) + 16
        for _ in range(int(math.cos(theta) * 10)):
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            pyxel.blt(x, y, 2, u, v, w, h, 0)

    def holy_sword_of_prayer(self):
        if (pyxel.frame_count - self.fc) % SPEED == 0:
            self.light_ball_list = []
            for _ in range(150):
                self.light_ball_list.append(LightBall(random.randint(0, WIDTH), random.randint(-HEIGHT, 0)))
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED) // 5 - 2
        x = self.enemy_width - 8 + random.randint(-4, 4)
        y = self.enemy_height - 8 + random.randint(-4, 4)
        if 0 <= effect_fc < 8:
            u = 16 if pyxel.frame_count % 2 == 0 else 80
            v = effect_fc * 32
            w = 32
            h = 32
            pyxel.blt(x, y, 1, u, v, w, h, 0)
        for ball in self.light_ball_list:
            ball.update()
            ball.draw()

        if (pyxel.frame_count - self.fc) % SPEED == 0:
            pyxel.play(0, 14)

    def heal_effect(self):
        if (pyxel.frame_count - self.fc) % SPEED < SPEED:
            start = (((pyxel.frame_count - self.fc) % SPEED) * (WIDTH - 7) // 20) - SPEED * 2
            end = (((pyxel.frame_count - self.fc) % SPEED) * (WIDTH - 7) // 20)
            for _ in range(20):
                x = random.randint(start, end)
                y = random.randint(self.player_h, HEIGHT - 7)
                pyxel.blt(x=x, y=y, img=2, u=32, v=0, w=7, h=7, colkey=0)

    def enemy_attack(self):
        efc = (pyxel.frame_count - self.fc) % SPEED
        self.draw_enemy_attack_self(pyxel.frame_count % 2)
        if efc == 0:
            self.enemy.damage = int(self.enemy.at * random.uniform(0.9, 1.2))
        message = f"{self.enemy.name}'s ATTACK!!"
        ans = self.return_message(message, (pyxel.frame_count - self.fc) % SPEED)
        pyxel.text(x=self.text_w, y=self.text_h, s=f"{ans}", col=7)
        if SPEED // 2 <= efc:
            message = f"Everyone took damage from {self.enemy.name}!"
            ans = self.return_message(message, efc - SPEED // 2)
            pyxel.text(x=self.text_w, y=self.text_h + 8, s=f"{ans}", col=7)

        if efc == 0:
            self.alive_list = []
            for player in self.player_list:
                if player.is_alive:
                    self.alive_list.append(player)
        for i in range(len(self.alive_list)):
            player = self.alive_list[i]
            self.draw_enemy_attack_fire(player, i * 3)
            if SPEED // 2 + i * 9 == efc:
                player.hp -= self.enemy.damage - int(player.df * random.uniform(0.4, 0.5))
                pyxel.play(1, 10)
            if SPEED // 2 + i * 9 <= efc < SPEED // 2 + i * 9 + 5:
                self.effect_when_player_is_attacked(player)
            elif SPEED // 2 + i * 9 + 5 <= efc:
                if player.is_alive:
                    pyxel.text(x=player.place, y=self.player_h + 8, s=f"HP {player.hp}/{player.max_hp}", col=8)
                else:
                    pyxel.text(x=player.place, y=self.player_h + 8, s=f"HP {player.hp}/{player.max_hp}", col=13)

    def draw_enemy_attack_self(self, index):
        index *= 2
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED) // 3
        if 0 <= effect_fc <= 18:
            self.hide_enemy_image()
            pyxel.bltm(x=self.enemy_width, y=self.enemy_height, tm=0, u=index, v=effect_fc * 2, w=2, h=2, colkey=0)
        else:
            self.hide_enemy_image()
            pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=0, v=16 * ((pyxel.frame_count // 4) % 8), w=16,
                      h=16)

    def draw_enemy_attack_fire(self, player, fc_point):
        effect_fc = ((pyxel.frame_count - self.fc) % SPEED - SPEED // 4) // 3 - fc_point
        x = player.place + random.randint(-4, 4)
        y = self.player_h + random.randint(-4, 4)
        if 0 <= effect_fc < 8:
            u = 48
            v = effect_fc * 32
            w = 32
            h = 32
            pyxel.blt(x, y, 1, u, v, w, h, 0)
        if effect_fc == 0:
            pyxel.play(0, 6)

    def draw_player_mp_red(self, player):
        pyxel.text(x=player.place, y=self.player_h + 16, s=f"   {player.mp}", col=8)

    def hide_player_status(self, player):
        pyxel.text(x=player.place, y=self.player_h, s=player.name, col=0)
        pyxel.text(x=player.place, y=self.player_h + 8, s=f"HP {player.hp}/{player.max_hp}", col=0)
        pyxel.text(x=player.place, y=self.player_h + 16, s=f"MP {player.mp}/{player.max_mp}", col=0)

    def hide_enemy_status(self):
        pyxel.text(self.enemy_width + 32, self.enemy_height, s=self.enemy.name, col=0)
        pyxel.text(self.enemy_width + 32, self.enemy_height + 8, s=f"HP {self.enemy.hp}/{self.enemy.max_hp}", col=0)
        pyxel.text(self.enemy_width + 32, self.enemy_height + 16, s=f"MP {self.enemy.mp}/{self.enemy.max_mp}", col=0)

    def hide_enemy_image(self):
        pyxel.blt(x=self.enemy_width, y=self.enemy_height, img=0, u=16, v=0, w=16, h=16)


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
        self.damage = 0
        self.skill_type = "attack"
        self.rate = 1
        self.skill_name = ""
        self.skill_mp = 0
        self.mp_after_skill = self.max_mp
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

        self.damage = 0

        self.is_alive = True


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


App()
