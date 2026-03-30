# main.py
import pgzrun
from pygame import Rect
from settings import *
from player import Player
from enemy import Enemy, Boss
from menu import Menu
from world import RoomManager, Item
from projectile import Projectile

state = "MENU"
menu = Menu(WIDTH, HEIGHT)
player = None
room_mgr = None
active_items = []
projectiles = []

def generate_items():
    global active_items
    active_items.clear()
    types = ['Health', 'Speed', 'Damage']
    spacing = 220
    start_x = WIDTH // 2 - spacing
    for i, t in enumerate(types):
        r = Rect(start_x + i * spacing - 75, HEIGHT // 2 - 100, 150, 200)
        active_items.append(Item(t, r))

def reset_game():
    global player, room_mgr, state, projectiles
    player = Player(Actor, 1, 4, TILE_SIZE)
    room_mgr = RoomManager(Actor, Enemy, Boss, TILE_SIZE)
    projectiles.clear()
    room_mgr.load_room(player)
    state = "PLAYING"
    if menu.sound_on:
        try: music.play("bg_music")
        except: pass

def draw():
    screen.clear()
    if state == "MENU":
        menu.draw(screen)
    elif state in ("PLAYING", "ITEM_SELECT"):
        screen.fill((20, 20, 20))
        for x in range(0, WIDTH, TILE_SIZE):
            for y in range(0, HEIGHT, TILE_SIZE):
                screen.draw.rect(Rect(x, y, TILE_SIZE, TILE_SIZE), (40, 40, 40))

        for t in room_mgr.traps: t.draw()
        for e in room_mgr.enemies: e.draw()
        if room_mgr.boss: room_mgr.boss.draw()
        
        for p in projectiles: p.draw()
        
        player.draw()

        screen.draw.text(f"HP: {player.hp}/{player.max_hp}", topleft=(10, 10), color="white", fontsize=30)
        screen.draw.text(f"ROOM: {room_mgr.current_room}/4", topright=(WIDTH - 10, 10), color="white", fontsize=30)

        if room_mgr.boss:
            bar_w, bar_h = 400, 20
            px, py = WIDTH // 2 - bar_w // 2, HEIGHT - 40
            screen.draw.filled_rect(Rect(px, py, bar_w, bar_h), (100, 0, 0))
            current_w = int(bar_w * (max(0, room_mgr.boss.hp) / room_mgr.boss.max_hp))
            if current_w > 0:
                screen.draw.filled_rect(Rect(px, py, current_w, bar_h), (255, 0, 0))
            screen.draw.text("BOSS", center=(WIDTH//2, py - 15), color="white")

        if state == "ITEM_SELECT":
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 150))
            screen.draw.text("CHOOSE AN UPGRADE", center=(WIDTH//2, 100), color="white", fontsize=50)
            for item in active_items: item.draw(screen)

    elif state == "GAME_OVER":
        screen.fill((100, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")
    elif state == "VICTORY":
        screen.fill((0, 100, 0))
        screen.draw.text("YOU WON!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")

def update():
    global state, projectiles
    if state == "PLAYING":
        player.update()
        
        # Atualiza projéteis e remove inativos da lista
        for p in projectiles:
            p.update(WIDTH, HEIGHT, room_mgr.enemies, room_mgr.boss)
        projectiles = [p for p in projectiles if p.active]
        
        room_mgr.enemies = [e for e in room_mgr.enemies if e.hp > 0]
        if room_mgr.boss and room_mgr.boss.hp <= 0:
            room_mgr.boss = None

        for e in room_mgr.enemies: e.update(player.speed, player)
        if room_mgr.boss: room_mgr.boss.update(player.speed, player)

        if player.hp <= 0:
            state = "GAME_OVER"
            
        if not room_mgr.enemies and not room_mgr.boss:
            if room_mgr.current_room < 4:
                state = "ITEM_SELECT"
                generate_items()
            else:
                state = "VICTORY"

def on_key_down(key):
    global projectiles
    if state == "PLAYING":
        # Suporte simultâneo a WASD e Setas
        if key in (keys.UP, keys.W): 
            player.move(0, -1, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.DOWN, keys.S): 
            player.move(0, 1, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.LEFT, keys.A): 
            player.move(-1, 0, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.RIGHT, keys.D): 
            player.move(1, 0, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        
        # Sistema de Ataque
        elif key == keys.SPACE:
            p = Projectile(Actor, player.sprite.x, player.sprite.y, player.last_dir[0], player.last_dir[1], player.damage)
            projectiles.append(p)

def on_mouse_down(pos):
    global state
    if state == "MENU":
        action = menu.handle_click(pos)
        if action == "START": reset_game()
        elif action == "SOUND":
            if not menu.sound_on:
                try: music.stop()
                except: pass
        elif action == "EXIT": exit()
    elif state == "ITEM_SELECT":
        for item in active_items:
            if item.rect.collidepoint(pos):
                item.apply(player)
                room_mgr.current_room += 1
                projectiles.clear() # Limpa tiros soltos antes de ir para a próxima sala
                room_mgr.load_room(player)
                state = "PLAYING"
    elif state in ("GAME_OVER", "VICTORY"):
        state = "MENU"

pgzrun.go()