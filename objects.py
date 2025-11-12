import pyxel
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 30
        self.color = random.choice([8, 10, 9])
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx *= 0.95
        self.vy *= 0.95

    def draw(self):
        if self.life > 0:
            #size = max(1, self.life // 10)
            pyxel.pset(self.x, self.y, self.color)

class Star:
    def __init__(self):
        self.x = random.randint(0, 159)
        self.y = random.randint(0, 119)
        self.speed = random.uniform(0.5, 1.5)
        self.color = random.choice([7, 12])

    def update(self):
        self.y += self.speed
        if self.y > 120:
            self.y = 0
            self.x = random.randint(0, 159)
    
    def draw(self):
        pyxel.pset(int(self.x), int(self.y), self.color)

# Bullet, Enemyクラスは定数を引数として受け取るように変更

class Bullet:
    def __init__(self, x, y, constants):
        self.x = x
        self.y = y
        self.C = constants # 定数を保持
        self.is_active = True

    def update(self):
        self.y -= 4
        if self.y < -self.C["SIZE"]:
            self.is_active = False

    def draw(self):
        if self.is_active:
            # 定数からスプライト座標を取得
            pyxel.blt(self.x, self.y, 0, self.C["BULLET_U"], self.C["BULLET_V"], self.C["SIZE"], self.C["SIZE"], 0)

class Enemy:
    def __init__(self, x, y, speed, constants):
        self.x = x
        self.y = y
        self.speed = speed
        self.C = constants # 定数を保持
        self.is_active = True

    def update(self):
        self.y += self.speed
        if self.y > self.C["SCREEN_HEIGHT"]:
            self.is_active = False

    def draw(self):
        if self.is_active:
            # 定数からスプライト座標を取得
            pyxel.blt(self.x, self.y, 0, self.C["ENEMY_U"], self.C["ENEMY_V"], self.C["SIZE"], self.C["SIZE"], 0)