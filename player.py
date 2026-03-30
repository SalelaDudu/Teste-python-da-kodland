# player.py
import math

class Player:
    def __init__(self, actor_class, tile_size):
        self.sprite = actor_class('player_idle_0')
        self.tile_size = tile_size
        self.grid_x, self.grid_y = 0, 0
        self.offset_x, self.offset_y = 0, 0
        self.target_x, self.target_y = 0, 0
        
        self.is_moving = False
        self.last_dir = (0, -1) 

        self.max_hp = 100
        self.hp = 100
        self.damage = 15
        self.speed = 4

        self.state = 'idle'
        self.frame_index = 0
        self.anim_timer = 0
        self.idle_frames = ['player_idle_0', 'player_idle_1']
        self.walk_frames = ['player_walk_0', 'player_walk_1', 'player_walk_2', 'player_walk_3']

    def set_position(self, gx, gy, ox, oy):
        self.grid_x = gx
        self.grid_y = gy
        self.offset_x = ox
        self.offset_y = oy
        self.target_x = self.grid_x * self.tile_size + self.tile_size // 2 + self.offset_x
        self.target_y = self.grid_y * self.tile_size + self.tile_size // 2 + self.offset_y
        self.sprite.x = self.target_x
        self.sprite.y = self.target_y
        self.is_moving = False

    def move(self, dx, dy, max_cols, max_rows, enemies, boss, traps):
        self.last_dir = (dx, dy)
        if self.is_moving: return
        
        new_gx = self.grid_x + dx
        new_gy = self.grid_y + dy
        
        # O player agora não consegue pisar fora dos limites texturizados da sala
        if not (0 <= new_gx < max_cols and 0 <= new_gy < max_rows): return

        target_enemy = next((e for e in enemies if e.grid_x == new_gx and e.grid_y == new_gy), None)
        if boss and boss.grid_x == new_gx and boss.grid_y == new_gy:
            target_enemy = boss

        if target_enemy: return  

        self.grid_x, self.grid_y = new_gx, new_gy
        self.target_x = self.grid_x * self.tile_size + self.tile_size // 2 + self.offset_x
        self.target_y = self.grid_y * self.tile_size + self.tile_size // 2 + self.offset_y
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
            frames = self.walk_frames if self.state == 'walk' else self.idle_frames
            if self.frame_index >= len(frames): self.frame_index = 0
            self.sprite.image = frames[self.frame_index]

    def draw(self):
        self.sprite.draw()