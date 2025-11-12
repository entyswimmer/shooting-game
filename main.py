import pyxel
from app import App

# --- 定数定義 ---
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
SIZE = 16
PLAYER_U = 0
PLAYER_V = 0
ENEMY_U = 16
ENEMY_V = 0
BULLET_U = 32
BULLET_V = 0

# すべての定数をAppクラスに渡すための辞書
CONSTANTS = {
    "SCREEN_WIDTH": SCREEN_WIDTH,
    "SCREEN_HEIGHT": SCREEN_HEIGHT,
    "SIZE": SIZE,
    "PLAYER_U": PLAYER_U,
    "PLAYER_V": PLAYER_V,
    "ENEMY_U": ENEMY_U,
    "ENEMY_V": ENEMY_V,
    "BULLET_U": BULLET_U,
    "BULLET_V": BULLET_V,
}

# ゲームの開始
App(CONSTANTS)