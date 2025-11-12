import pyxel
import random
from objects import Particle, Star, Bullet, Enemy # クラスをインポート

#シーン定数
SCENE_TITLE = 0
SCENE_GAME = 1
SCENE_GAMEOVER = 2

class App:
    def __init__(self, constants):
        # 定数をクラス変数として保存
        self.C = constants
        pyxel.init(self.C["SCREEN_WIDTH"], self.C["SCREEN_HEIGHT"], title="Pyxel Shooter")

        try:
            pyxel.load("assets/my_shooter.pyxres")
        except FileNotFoundError:
            print("エラー: 'assets/my_shooter.pyxres'が見つかりません。")
            pyxel.quit()

        # サウンド設定の修正 (定数を使用)
        pyxel.sounds[0].set("c3b2a2f2e2d2c2", "N", "7531000", "NFNFNNN", 10) #爆発音
        pyxel.sounds[1].set("a1f1", "N", "7777", "N", 20)  # 被弾音
        pyxel.sounds[2].set("c2c3g3", "P", "777", "NFN", 8) #スタート音
        pyxel.sounds[3].set("c3g2e2c2", "T", "7777", "NFNf", 12) #ゲームオーバー音
        
        # 初期シーン設定
        self.scene = SCENE_TITLE
        self.score = 0
        self.lives = 3
        self.reset_game()
        pyxel.run(self.update, self.draw)

    #画面遷移
    def reset_game(self):
        """ゲーム初期化"""
        self.player_x = self.C["SCREEN_WIDTH"] // 2 + self.C["SIZE"] // 2
        self.player_y = self.C["SCREEN_HEIGHT"] - 16
        self.bullets = []
        self.enemies = []
        self.particles = []
        self.stars = [Star() for _ in range(100)]
        self.enemy_spawn_timer = 0
        self.score = 0
        self.lives = 3

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_GAME:
            self.update_game()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover()

    #シーンごとのアップデート
    def update_title(self):
        """タイトル画面の更新ロジック"""
        # スペースキーを押すとゲーム開始
        if pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.play(0, 2)
            self.scene = SCENE_GAME
            self.score = 0 # 新しいゲーム開始時にスコアをリセット
            self.reset_game()

    def update_game(self):
        """ゲーム中の更新ロジック"""
        self.update_player()
        self.update_enemies()
        self.update_bullets()
        self.update_particles()
        self.update_stars()
        self.check_collisions()
        self.spawn_enemies()

        self.bullets = [b for b in self.bullets if b.is_active]
        self.enemies = [e for e in self.enemies if e.is_active]
        self.particles = [p for p in self.particles if p.life > 0]
        
        #ゲームオーバーシーンへ移行
        if self.lives <= 0:
            pyxel.play(0, 3)
            self.scene = SCENE_GAMEOVER

    def update_gameover(self):
        """ゲームオーバー画面の更新ロジック"""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_TITLE

    #ゲームロジックの詳細なアップデート
    def update_player(self):
        if pyxel.btn(pyxel.KEY_Z):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_C):
            self.player_x = min(self.player_x + 2, self.C["SCREEN_WIDTH"] - self.C["SIZE"])

        if pyxel.btnp(pyxel.KEY_SPACE):
            # Bulletオブジェクトを生成し、CONSTANTSを渡す
            bullet = Bullet(self.player_x + self.C["SIZE"] // 2 - 2, self.player_y, self.C)
            self.bullets.append(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update()
            # 敵がプレイヤーに到達したらライフ減少
            if enemy.y + self.C["SIZE"] >= self.player_y and abs(enemy.x - self.player_x) < self.C["SIZE"]:
                enemy.is_active = False
                pyxel.play(0, 1)  # 被弾音
                self.lives -= 1
                self.create_explosion(self.player_x + self.C["SIZE"] // 2, self.player_y)
                if self.lives <= 0:
                    self.game_over = True

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def update_particles(self):
        for particle in self.particles:
            particle.update()
    
    def update_stars(self):
        for star in self.stars:
            star.update()

    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        spawn_rate = max(30 - self.score // 50, 5)
        enemy_speed = 1 + self.score // 200

        if self.enemy_spawn_timer >= spawn_rate:
            x = random.randint(0, self.C["SCREEN_WIDTH"] - self.C["SIZE"])
            # Enemyオブジェクトを生成し、CONSTANTSを渡す
            self.enemies.append(Enemy(x, -self.C["SIZE"], enemy_speed, self.C))
            self.enemy_spawn_timer = 0

    def create_explosion(self, x, y):
        for _ in range(10):
            self.particles.append(Particle(x, y))

    def check_collisions(self):
        for bullet in self.bullets:
            if not bullet.is_active:
                continue
            for enemy in self.enemies:
                if not enemy.is_active:
                    continue
                
                # 衝突判定 (SIZEは16に統一)
                if (bullet.x < enemy.x + self.C["SIZE"] and
                    bullet.x + 4 > enemy.x and # 弾の幅4px
                    bullet.y < enemy.y + self.C["SIZE"] and
                    bullet.y + 8 > enemy.y): # 弾の高さ8px

                    bullet.is_active = False
                    enemy.is_active = False
                    pyxel.play(0, 0) # 撃破音
                    self.create_explosion(enemy.x + self.C["SIZE"] // 2, enemy.y + self.C["SIZE"] // 2)
                    self.score += 10

    def draw(self):
        pyxel.cls(0) # 背景を黒でクリア

        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_GAME:
            self.draw_game()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover()

    # --- シーンごとの描画 ---
    def draw_title(self):
        """タイトル画面の描画ロジック"""
        screen_center_x = self.C["SCREEN_WIDTH"] // 2
        title_text = "SHOOTING GAME"
        pyxel.text(screen_center_x - len(title_text) * 2, 40, title_text, 5)
        pyxel.blt(screen_center_x - self.C["SIZE"] // 2, 60, 0, self.C["PLAYER_U"], self.C["PLAYER_V"], self.C["SIZE"], self.C["SIZE"], 0)
        guide_text = "PRESS SPACE TO START"
        if pyxel.frame_count % 30 < 15:
            pyxel.text(screen_center_x - len(guide_text) * 2, 90, guide_text, 7)

    def draw_game(self):
        """ゲーム中の描画ロジック"""
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for particle in self.particles:
            particle.draw()
        for star in self.stars:
            star.draw()
            
        # プレイヤー描画
        pyxel.blt(self.player_x, self.player_y, 0, self.C["PLAYER_U"], self.C["PLAYER_V"], self.C["SIZE"], self.C["SIZE"], 0)

        # スコアとライフ表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 11)
        pyxel.text(120, 5, f"LIVES: {self.lives}", 11)
        
    def draw_gameover(self):
        """ゲームオーバー画面の描画ロジック"""
        screen_center_x = self.C["SCREEN_WIDTH"] // 2
        
        pyxel.text(screen_center_x - len("GAME OVER") * 2, 50, "GAME OVER", 8)
        
        score_text = f"FINAL SCORE: {self.score}"
        pyxel.text(screen_center_x - len(score_text) * 2, 70, score_text, 5)
        
        restart_text = "Press SPACE for Title"
        pyxel.text(screen_center_x - len(restart_text) * 2, 90, restart_text, 7)
