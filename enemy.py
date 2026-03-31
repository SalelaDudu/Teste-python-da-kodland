import math

class Enemy:
    def __init__(self, actor_class, gx, gy, tile_size, bounds, pattern='vertical', sprite_base='enemy'):
        self.sprite = actor_class(f'{sprite_base}_idle_0')
        self.tile_size = tile_size
        self.grid_x, self.grid_y = gx, gy
        self.offset_x, self.offset_y = 0, 0
        self.target_x, self.target_y = 0, 0
        self.is_moving = False
        self.bounds = bounds
        
        self.max_hp = 20
        self.hp = 20
        self.damage = 10
        self.pattern = pattern
        
        self.dir_x = 1 if pattern == 'horizontal' else 0
        self.dir_y = -1 if pattern == 'vertical' else 0
        
        self.state = 'idle'
        self.frame_index = 0
        self.anim_timer, self.move_timer = 0, 0
        self.move_delay = 50
        
        self.idle_frames = [f'{sprite_base}_idle_0', f'{sprite_base}_idle_1']
        self.walk_frames = [f'{sprite_base}_walk_0', f'{sprite_base}_walk_1']

    def set_offset(self, ox, oy):
        self.offset_x = ox
        self.offset_y = oy
        self.target_x = self.grid_x * self.tile_size + self.tile_size // 2 + self.offset_x
        self.target_y = self.grid_y * self.tile_size + self.tile_size // 2 + self.offset_y
        self.sprite.x = self.target_x
        self.sprite.y = self.target_y

    # movimento e tomada de decisao
    def think(self, player):
        next_gx, next_gy = self.grid_x, self.grid_y
        
        if self.pattern == 'vertical':
            if self.bounds and (self.bounds[2] <= self.grid_y + self.dir_y <= self.bounds[3]):
                next_gy = self.grid_y + self.dir_y
            else:
                self.dir_y *= -1
                next_gy = self.grid_y + self.dir_y
                
        elif self.pattern == 'horizontal':
            if self.bounds and (self.bounds[0] <= self.grid_x + self.dir_x <= self.bounds[1]):
                next_gx = self.grid_x + self.dir_x
            else:
                self.dir_x *= -1
                next_gx = self.grid_x + self.dir_x
                
        elif self.pattern == 'perimeter':
            if self.grid_y == self.bounds[2] and self.grid_x < self.bounds[1]:
                next_gx = self.grid_x + 1
            elif self.grid_x == self.bounds[1] and self.grid_y < self.bounds[3]:
                next_gy = self.grid_y + 1
            elif self.grid_y == self.bounds[3] and self.grid_x > self.bounds[0]:
                next_gx = self.grid_x - 1
            elif self.grid_x == self.bounds[0] and self.grid_y > self.bounds[2]:
                next_gy = self.grid_y - 1
            else:
                next_gx, next_gy = self.bounds[0], self.bounds[2]

        # Dano ao colidir no player
        if next_gx == player.grid_x and next_gy == player.grid_y:
            player.hp -= self.damage
        else:
            self.set_target(next_gx, next_gy)

    def set_target(self, gx, gy):
        self.grid_x, self.grid_y = gx, gy
        self.target_x = self.grid_x * self.tile_size + self.tile_size // 2 + self.offset_x
        self.target_y = self.grid_y * self.tile_size + self.tile_size // 2 + self.offset_y
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

        # Animacao
        self.anim_timer += 1
        if self.anim_timer > 12:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames if self.state == 'walk' else self.idle_frames)
            self.sprite.image = (self.walk_frames if self.state == 'walk' else self.idle_frames)[self.frame_index]

    def draw(self):
        self.sprite.draw()

class Enemy2(Enemy):
    def __init__(self, actor_class, gx, gy, tile_size, bounds, pattern='vertical'):
        super().__init__(actor_class, gx, gy, tile_size, bounds, pattern, 'enemy2')
        self.max_hp = 60
        self.hp = 60
        self.damage = 10
        self.move_delay = 80

class Enemy3(Enemy):
    def __init__(self, actor_class, gx, gy, tile_size, bounds, pattern='vertical'):
        super().__init__(actor_class, gx, gy, tile_size, bounds, pattern, 'enemy3')
        self.max_hp = 30
        self.hp = 30
        self.damage = 10
        self.move_delay = 5

class Boss(Enemy):
    def __init__(self, actor_class, gx, gy, tile_size):
        super().__init__(actor_class, gx, gy, tile_size, None, 'random', 'boss')
        self.max_hp = 250
        self.hp = 250
        self.damage = 25
        self.move_delay = 45

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