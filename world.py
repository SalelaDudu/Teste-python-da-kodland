# world.py
from pygame import Rect

class Trap:
    def __init__(self, actor_class, gx, gy, tile_size):
        self.sprite = actor_class('trap_idle')
        self.grid_x, self.grid_y = gx, gy
        self.sprite.x = gx * tile_size + tile_size // 2
        self.sprite.y = gy * tile_size + tile_size // 2
        self.damage = 15

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
    def __init__(self, actor_class, enemy_class, boss_class, tile_size):
        self.actor_class = actor_class
        self.enemy_class = enemy_class
        self.boss_class = boss_class
        self.tile_size = tile_size
        self.current_room = 1
        self.enemies = []
        self.traps = []
        self.boss = None

    def load_room(self, player):
        self.enemies.clear()
        self.traps.clear()
        self.boss = None
        
        player.grid_x, player.grid_y = 1, 4
        player.target_x = player.grid_x * self.tile_size + self.tile_size // 2
        player.target_y = player.grid_y * self.tile_size + self.tile_size // 2
        player.sprite.x, player.sprite.y = player.target_x, player.target_y
        player.is_moving = False

        if self.current_room == 1:
            self.enemies = [
                self.enemy_class(self.actor_class, 8, 2, self.tile_size, (5, 10, 1, 7)),
                self.enemy_class(self.actor_class, 8, 6, self.tile_size, (5, 10, 1, 7))
            ]
        elif self.current_room == 2:
            self.enemies = [
                self.enemy_class(self.actor_class, 7, 2, self.tile_size, (4, 11, 1, 8)),
                self.enemy_class(self.actor_class, 7, 7, self.tile_size, (4, 11, 1, 8)),
                self.enemy_class(self.actor_class, 10, 4, self.tile_size, (4, 11, 1, 8))
            ]
            self.traps = [Trap(self.actor_class, 5, 4, self.tile_size), Trap(self.actor_class, 6, 4, self.tile_size)]
        elif self.current_room == 3:
            self.enemies = [
                self.enemy_class(self.actor_class, 6, 2, self.tile_size, (2, 11, 1, 8)),
                self.enemy_class(self.actor_class, 9, 7, self.tile_size, (2, 11, 1, 8)),
                self.enemy_class(self.actor_class, 6, 7, self.tile_size, (2, 11, 1, 8)),
                self.enemy_class(self.actor_class, 9, 2, self.tile_size, (2, 11, 1, 8))
            ]
            self.traps = [Trap(self.actor_class, x, 4, self.tile_size) for x in range(4, 8)]
        elif self.current_room == 4:
            self.boss = self.boss_class(self.actor_class, 9, 4, self.tile_size)
            self.traps = [Trap(self.actor_class, 4, 2, self.tile_size), Trap(self.actor_class, 4, 6, self.tile_size)]