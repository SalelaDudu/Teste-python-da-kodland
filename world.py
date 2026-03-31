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

# Cartao de upgrade
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
        screen.draw.text(f"+ {self.type}", center=self.rect.center, color="white", fontname="pixeled", fontsize=25)

# Controla as waves e o spawn do mapa
class RoomManager:
    def __init__(self, actor_class, enemy_class, enemy2_class, enemy3_class, boss_class, tile_size, screen_w, screen_h):
        self.actor_class = actor_class
        self.enemy_class = enemy_class
        self.enemy2_class = enemy2_class
        self.enemy3_class = enemy3_class
        self.boss_class = boss_class
        
        self.tile_size = tile_size
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        self.current_room = 1
        self.enemies = []
        self.traps = []
        self.boss = None
        
        self.cols, self.rows = 5, 5
        self.offset_x, self.offset_y = 0, 0
        self.floor_tex = 'floor_1'
        self.door_tex = 'door'
        self.door_pos = None

    def load_room(self, player):
        self.enemies.clear()
        self.traps.clear()
        self.boss = None
        spawn_x, spawn_y = 2, 4
        
        # genrencia de salas
        if self.current_room == 1:
            self.cols, self.rows = 5, 5
            self.floor_tex = 'floor_1'
            self.door_pos = (2, -1) 
            spawn_x, spawn_y = 2, 4
            self.enemies = [
                self.enemy_class(self.actor_class, 1, 2, self.tile_size, (1, 1, 1, 3), 'vertical'),
                self.enemy_class(self.actor_class, 3, 2, self.tile_size, (3, 3, 1, 3), 'vertical')
            ]
            
        elif self.current_room == 2:
            self.cols, self.rows = 5, 5
            self.floor_tex = 'floor_1'
            self.door_pos = (2, -1) 
            spawn_x, spawn_y = 2, 4
            self.enemies = [
                self.enemy2_class(self.actor_class, 1, 1, self.tile_size, (1, 3, 1, 1), 'horizontal'),
                self.enemy2_class(self.actor_class, 3, 3, self.tile_size, (1, 3, 3, 3), 'horizontal')
            ]
            
        elif self.current_room == 3:
            self.cols, self.rows = 5, 5
            self.floor_tex = 'floor_1'
            self.door_pos = (5, 2) 
            spawn_x, spawn_y = 2, 4
            self.enemies = [
                self.enemy3_class(self.actor_class, 1, 1, self.tile_size, (1, 3, 1, 3), 'perimeter'),
                self.enemy3_class(self.actor_class, 3, 3, self.tile_size, (1, 3, 1, 3), 'perimeter')
            ]
            # Coloca armadilhas
            self.traps = [
                Trap(self.actor_class, 2, 2, self.tile_size),
                Trap(self.actor_class, 4, 1, self.tile_size),
                Trap(self.actor_class, 4, 3, self.tile_size)
            ]
            
        elif self.current_room == 4:
            self.cols, self.rows = 12, 5
            self.floor_tex = 'floor_boss'
            self.door_pos = None 
            spawn_x, spawn_y = 0, 2
            self.boss = self.boss_class(self.actor_class, 9, 2, self.tile_size)
            
        # Centraliza a sala
        self.offset_x = (self.screen_w - self.cols * self.tile_size) // 2
        self.offset_y = (self.screen_h - self.rows * self.tile_size) // 2
        
        player.set_position(spawn_x, spawn_y, self.offset_x, self.offset_y)
        for e in self.enemies: e.set_offset(self.offset_x, self.offset_y)
        for t in self.traps: t.set_offset(self.offset_x, self.offset_y)
        if self.boss: self.boss.set_offset(self.offset_x, self.offset_y)