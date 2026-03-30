# world.py
from pygame import Rect

class Trap:
    def __init__(self, actor_class, gx, gy, tile_size):
        self.sprite = actor_class('trap_idle')
        self.tile_size = tile_size
        self.grid_x, self.grid_y = gx, gy
        self.offset_x, self.offset_y = 0, 0
        self.damage = 15

    def set_offset(self, ox, oy):
        self.offset_x = ox
        self.offset_y = oy
        self.sprite.x = self.grid_x * self.tile_size + self.tile_size // 2 + self.offset_x
        self.sprite.y = self.grid_y * self.tile_size + self.tile_size // 2 + self.offset_y

    def draw(self):
        self.sprite.draw()

class Item:
    def __init__(self, item_type, rect):
        self.type = item_type
        self.rect = rect

    def apply(self, player):
        if self.type == 'Health':
            player.max_hp += 50
            player.hp = player.max_hp
        elif self.type == 'Speed':
            player.speed += 2
        elif self.type == 'Damage':
            player.damage += 15

    def draw(self, screen):
        screen.draw.filled_rect(self.rect, (60, 60, 120))
        screen.draw.rect(self.rect, (255, 255, 255))
        screen.draw.text(f"+ {self.type}", center=self.rect.center, color="white", fontsize=30)

class RoomManager:
    def __init__(self, actor_class, enemy_class, boss_class, tile_size, screen_w, screen_h):
        self.actor_class = actor_class
        self.enemy_class = enemy_class
        self.boss_class = boss_class
        self.tile_size = tile_size
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        self.current_room = 1
        self.enemies = []
        self.traps = []
        self.boss = None
        
        # Atributos dinâmicos da sala
        self.cols, self.rows = 5, 5
        self.offset_x, self.offset_y = 0, 0
        self.floor_tex = 'floor_1'
        self.door_tex = 'door'
        self.door_pos = (-1, -1)

    def load_room(self, player):
        self.enemies.clear()
        self.traps.clear()
        self.boss = None
        spawn_x, spawn_y = 2, 4
        
        if self.current_room == 1:
            self.cols, self.rows = 5, 5
            self.floor_tex = 'floor_1'
            self.door_pos = (2, 0) # Porta no topo
            spawn_x, spawn_y = 2, 4  # Nasce embaixo
            self.enemies = [
                self.enemy_class(self.actor_class, 1, 2, self.tile_size, (1, 1, 1, 3), 'vertical'),
                self.enemy_class(self.actor_class, 3, 2, self.tile_size, (3, 3, 1, 3), 'vertical')
            ]
        elif self.current_room == 2:
            self.cols, self.rows = 5, 5
            self.floor_tex = 'floor_1'
            self.door_pos = (2, 0) # Porta no topo
            spawn_x, spawn_y = 2, 4  # Nasce embaixo
            self.enemies = [
                self.enemy_class(self.actor_class, 1, 1, self.tile_size, (1, 3, 1, 1), 'horizontal'),
                self.enemy_class(self.actor_class, 3, 3, self.tile_size, (1, 3, 3, 3), 'horizontal')
            ]
        elif self.current_room == 3:
            self.cols, self.rows = 5, 5
            self.floor_tex = 'floor_1'
            self.door_pos = (4, 2) # Porta na direita
            spawn_x, spawn_y = 2, 4  # Nasce embaixo vindo da sala 2
            self.enemies = [
                self.enemy_class(self.actor_class, 1, 1, self.tile_size, (1, 3, 1, 3), 'perimeter')
            ]
        elif self.current_room == 4:
            self.cols, self.rows = 12, 5
            self.floor_tex = 'floor_boss'
            self.door_pos = (-1, -1) # Sem porta de saída
            spawn_x, spawn_y = 0, 2  # Nasce na esquerda vindo da sala 3
            self.boss = self.boss_class(self.actor_class, 9, 2, self.tile_size)
            
        # Calcula onde a sala deve ser desenhada para ficar perfeitamente centralizada
        self.offset_x = (self.screen_w - self.cols * self.tile_size) // 2
        self.offset_y = (self.screen_h - self.rows * self.tile_size) // 2
        
        # Aplica o offset às entidades
        player.set_position(spawn_x, spawn_y, self.offset_x, self.offset_y)
        for e in self.enemies: e.set_offset(self.offset_x, self.offset_y)
        for t in self.traps: t.set_offset(self.offset_x, self.offset_y)
        if self.boss: self.boss.set_offset(self.offset_x, self.offset_y)