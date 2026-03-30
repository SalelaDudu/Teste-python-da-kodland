# enemy.py
import math
import random

class Enemy:
    def __init__(self, actor_class, gx, gy, tile_size, bounds, pattern='vertical'):
        self.sprite = actor_class('enemy_idle_0')
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
        self.pattern = pattern
        
        self.dir_x = 1 if pattern == 'horizontal' else 0
        self.dir_y = -1 if pattern == 'vertical' else 0
        
        self.state = 'idle'
        self.frame_index = 0
        self.anim_timer, self.move_timer = 0, 0
        self.move_delay = 50
        self.idle_frames = ['enemy_idle_0', 'enemy_idle_1']
        self.walk_frames = ['enemy_walk_0', 'enemy_walk_1']

    def think(self, player):
        if self.pattern == 'vertical':
            new_gy = self.grid_y + self.dir_y
            if self.bounds and (self.bounds[2] <= new_gy <= self.bounds[3]):
                self.set_target(self.grid_x, new_gy)
            else:
                self.dir_y *= -1
                self.set_target(self.grid_x, self.grid_y + self.dir_y)
                
        elif self.pattern == 'horizontal':
            new_gx = self.grid_x + self.dir_x
            if self.bounds and (self.bounds[0] <= new_gx <= self.bounds[1]):
                self.set_target(new_gx, self.grid_y)
            else:
                self.dir_x *= -1
                self.set_target(self.grid_x + self.dir_x, self.grid_y)
                
        elif self.pattern == 'perimeter':
            if self.grid_y == self.bounds[2] and self.grid_x < self.bounds[1]:
                self.set_target(self.grid_x + 1, self.grid_y) # Direita
            elif self.grid_x == self.bounds[1] and self.grid_y < self.bounds[3]:
                self.set_target(self.grid_x, self.grid_y + 1) # Baixo
            elif self.grid_y == self.bounds[3] and self.grid_x > self.bounds[0]:
                self.set_target(self.grid_x - 1, self.grid_y) # Esquerda
            elif self.grid_x == self.bounds[0] and self.grid_y > self.bounds[2]:
                self.set_target(self.grid_x, self.grid_y - 1) # Cima
            else:
                self.set_target(self.bounds[0], self.bounds[2])

        # Se chocar com o player durante o movimento
        if self.target_x // self.tile_size == player.grid_x and self.target_y // self.tile_size == player.grid_y:
            player.hp -= self.damage
            self.set_target(self.grid_x, self.grid_y) # Cancela passo

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
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames if self.state == 'walk' else self.idle_frames)
            self.sprite.image = (self.walk_frames if self.state == 'walk' else self.idle_frames)[self.frame_index]

    def draw(self):
        self.sprite.draw()

class Boss(Enemy):
    def __init__(self, actor_class, gx, gy, tile_size):
        super().__init__(actor_class, gx, gy, tile_size, None, 'random')
        self.sprite.image = 'boss_idle_0'
        self.max_hp = 150
        self.hp = 150
        self.damage = 25
        self.move_delay = 45
        self.idle_frames = ['boss_idle_0', 'boss_idle_1']
        self.walk_frames = ['boss_walk_0', 'boss_walk_1']

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