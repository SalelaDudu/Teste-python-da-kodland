# player.py
import math

class Player:
    def __init__(self, actor_class, start_gx, start_gy, tile_size):
        self.sprite = actor_class('player_idle1')
        self.tile_size = tile_size
        self.grid_x = start_gx
        self.grid_y = start_gy
        self.sprite.x = self.grid_x * self.tile_size + self.tile_size // 2
        self.sprite.y = self.grid_y * self.tile_size + self.tile_size // 2
        self.target_x = self.sprite.x
        self.target_y = self.sprite.y
        self.is_moving = False
        self.last_dir = (1, 0)  # Padrão: olhando para a direita

        self.max_hp = 100
        self.hp = 100
        self.damage = 15
        self.speed = 4

        self.state = 'idle'
        self.frame_index = 0
        self.anim_timer = 0
        self.idle_frames = ['player_idle1', 'player_idle2']
        self.runframes = ['player_run1', 'player_run2', 'player_run3', 'player_run4']

    def move(self, dx, dy, max_x, max_y, enemies, boss, traps):
        self.last_dir = (dx, dy)
        if self.is_moving: return
        
        new_gx = self.grid_x + dx
        new_gy = self.grid_y + dy
        
        if not (0 <= new_gx < max_x and 0 <= new_gy < max_y): return

        # Checa colisão física com inimigos (agora eles apenas bloqueiam)
        target_enemy = next((e for e in enemies if e.grid_x == new_gx and e.grid_y == new_gy), None)
        if boss and boss.grid_x == new_gx and boss.grid_y == new_gy:
            target_enemy = boss

        if target_enemy:
            return  # Caminho bloqueado

        self.grid_x = new_gx
        self.grid_y = new_gy
        self.target_x = self.grid_x * self.tile_size + self.tile_size // 2
        self.target_y = self.grid_y * self.tile_size + self.tile_size // 2
        self.is_moving = True
        self.state = 'walk'

        for t in traps:
            if t.grid_x == self.grid_x and t.grid_y == self.grid_y:
                self.hp -= t.damage

    def update(self):
        if self.is_moving:
            dx = self.target_x - self.sprite.x
            dy = self.target_y - self.sprite.y
            dist = math.hypot(dx, dy)

            if dist < self.speed:
                self.sprite.x, self.sprite.y = self.target_x, self.target_y
                self.is_moving = False
                self.state = 'idle'
            else:
                self.sprite.x += (dx / dist) * self.speed
                self.sprite.y += (dy / dist) * self.speed

        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_timer = 0
            self.frame_index += 1
            frames = self.runframes if self.state == 'walk' else self.idle_frames
            if self.frame_index >= len(frames): self.frame_index = 0
            self.sprite.image = frames[self.frame_index]

    def draw(self):
        self.sprite.draw()