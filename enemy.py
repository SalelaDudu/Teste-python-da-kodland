# enemy.py
import math
import random

class Enemy:
    def __init__(self, actor_class, gx, gy, tile_size, bounds):
        self.sprite = actor_class('enemy_idle1')
        self.tile_size = tile_size
        self.grid_x, self.grid_y = gx, gy
        self.sprite.x = gx * tile_size + tile_size // 2
        self.sprite.y = gy * tile_size + tile_size // 2
        self.target_x, self.target_y = self.sprite.x, self.sprite.y
        self.is_moving = False
        self.bounds = bounds
        
        self.max_hp = 30
        self.hp = 30
        self.damage = 10
        
        self.state = 'idle'
        self.frame_index = 0
        self.anim_timer, self.move_timer = 0, 0
        self.move_delay = 60
        self.idleframes = ['enemy_idle1', 'enemy_idle2']
        self.runframes = ['enemy_run1', 'enemy_run2']

    def think(self, player):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_gx, new_gy = self.grid_x + dx, self.grid_y + dy
        
        if new_gx == player.grid_x and new_gy == player.grid_y:
            player.hp -= self.damage
        elif self.bounds and (self.bounds[0] <= new_gx <= self.bounds[1] and self.bounds[2] <= new_gy <= self.bounds[3]):
            self.set_target(new_gx, new_gy)

    def set_target(self, gx, gy):
        self.grid_x, self.grid_y = gx, gy
        self.target_x = self.grid_x * self.tile_size + self.tile_size // 2
        self.target_y = self.grid_y * self.tile_size + self.tile_size // 2
        self.is_moving = True
        self.state = 'walk'

    def update(self, speed, player):
        if not self.is_moving:
            self.move_timer += 1
            if self.move_timer > self.move_delay:
                self.move_timer = 0
                self.think(player)

        if self.is_moving:
            dx, dy = self.target_x - self.sprite.x, self.target_y - self.sprite.y
            dist = math.hypot(dx, dy)
            if dist < speed:
                self.sprite.x, self.sprite.y = self.target_x, self.target_y
                self.is_moving = False
                self.state = 'idle'
            else:
                self.sprite.x += (dx / dist) * speed
                self.sprite.y += (dy / dist) * speed

        self.anim_timer += 1
        if self.anim_timer > 12:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.runframes if self.state == 'walk' else self.idleframes)
            self.sprite.image = (self.runframes if self.state == 'walk' else self.idleframes)[self.frame_index]

    def draw(self):
        self.sprite.draw()

class Boss(Enemy):
    def __init__(self, actor_class, gx, gy, tile_size):
        super().__init__(actor_class, gx, gy, tile_size, None)
        self.sprite.image = 'boss_idle1'
        self.max_hp = 150
        self.hp = 150
        self.damage = 25
        self.move_delay = 45
        self.idleframes = ['boss_idle1', 'boss_idle2']
        self.runframes = ['boss_run1', 'boss_run2']

    def think(self, player):
        dx, dy = 0, 0
        if player.grid_x > self.grid_x: dx = 1
        elif player.grid_x < self.grid_x: dx = -1
        elif player.grid_y > self.grid_y: dy = 1
        elif player.grid_y < self.grid_y: dy = -1
        
        new_gx, new_gy = self.grid_x + dx, self.grid_y + dy
        if new_gx == player.grid_x and new_gy == player.grid_y:
            player.hp -= self.damage
        else:
            self.set_target(new_gx, new_gy)