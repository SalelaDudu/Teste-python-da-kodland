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

# Variáveis para transição suave de câmera
cam_x, cam_y = 0, 0
cam_target_x, cam_target_y = 0, 0
old_floor_x, old_floor_y = 0, 0
new_floor_x, new_floor_y = 0, 0

def generate_items():
    global active_items
    active_items.clear()
    types = ['Health', 'Speed', 'Damage']
    spacing = 220
    start_x = WIDTH // 2 - spacing
    for i, t in enumerate(types):
        r = Rect(start_x + i * spacing - 75, HEIGHT // 2 - 100, 150, 200)
        active_items.append(Item(t, r))

def start_camera_transition():
    global state, cam_x, cam_y, cam_target_x, cam_target_y, old_floor_x, old_floor_y, new_floor_x, new_floor_y
    room_mgr.current_room += 1
    state = "TRANSITION"
    cam_x, cam_y = 0, 0
    old_floor_x, old_floor_y = 0, 0
    
    # Direção de acordo com o desenho
    if room_mgr.current_room in (2, 3):
        cam_target_x, cam_target_y = 0, -HEIGHT
        new_floor_x, new_floor_y = 0, -HEIGHT
    elif room_mgr.current_room == 4:
        cam_target_x, cam_target_y = WIDTH, 0
        new_floor_x, new_floor_y = WIDTH, 0
        
    projectiles.clear()
    room_mgr.load_room(player)

def reset_game():
    global player, room_mgr, state, projectiles
    player = Player(Actor, 5, 7, TILE_SIZE)
    room_mgr = RoomManager(Actor, Enemy, Boss, TILE_SIZE)
    projectiles.clear()
    room_mgr.load_room(player)
    state = "PLAYING"
    if menu.sound_on:
        try: music.play("bg_music")
        except: pass

def draw_floor(screen, ox, oy):
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            screen.draw.rect(Rect(x + ox, y + oy, TILE_SIZE, TILE_SIZE), (40, 40, 40))

def draw_with_offset(entity, ox, oy):
    if entity:
        entity.sprite.x += ox
        entity.sprite.y += oy
        entity.draw()
        entity.sprite.x -= ox
        entity.sprite.y -= oy

def draw():
    screen.clear()
    if state == "MENU":
        menu.draw(screen)
        
    elif state in ("PLAYING", "ITEM_SELECT"):
        screen.fill((20, 20, 20))
        draw_floor(screen, 0, 0)

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
            
    elif state == "TRANSITION":
        screen.fill((20, 20, 20))
        # Desenha as duas salas com deslocamento
        draw_floor(screen, old_floor_x - cam_x, old_floor_y - cam_y)
        draw_floor(screen, new_floor_x - cam_x, new_floor_y - cam_y)
        
        ox = new_floor_x - cam_x
        oy = new_floor_y - cam_y
        
        for t in room_mgr.traps: draw_with_offset(t, ox, oy)
        for e in room_mgr.enemies: draw_with_offset(e, ox, oy)
        if room_mgr.boss: draw_with_offset(room_mgr.boss, ox, oy)
        draw_with_offset(player, ox, oy)

    elif state == "GAME_OVER":
        screen.fill((100, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")
    elif state == "VICTORY":
        screen.fill((0, 100, 0))
        screen.draw.text("YOU WON!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")

def update():
    global state, projectiles, cam_x, cam_y
    if state == "PLAYING":
        player.update()
        
        for p in projectiles: p.update(WIDTH, HEIGHT, room_mgr.enemies, room_mgr.boss)
        projectiles = [p for p in projectiles if p.active]
        
        room_mgr.enemies = [e for e in room_mgr.enemies if e.hp > 0]
        if room_mgr.boss and room_mgr.boss.hp <= 0: room_mgr.boss = None

        for e in room_mgr.enemies: e.update(player.speed, player)
        if room_mgr.boss: room_mgr.boss.update(player.speed, player)

        if player.hp <= 0: state = "GAME_OVER"
            
        if not room_mgr.enemies and not room_mgr.boss:
            if room_mgr.current_room < 4:
                state = "ITEM_SELECT"
                generate_items()
            else:
                state = "VICTORY"
                
    elif state == "TRANSITION":
        # Interpolação de movimento suave da câmera
        cam_speed = 15
        if cam_x < cam_target_x: cam_x = min(cam_x + cam_speed, cam_target_x)
        elif cam_x > cam_target_x: cam_x = max(cam_x - cam_speed, cam_target_x)
        
        if cam_y < cam_target_y: cam_y = min(cam_y + cam_speed, cam_target_y)
        elif cam_y > cam_target_y: cam_y = max(cam_y - cam_speed, cam_target_y)
        
        if cam_x == cam_target_x and cam_y == cam_target_y:
            state = "PLAYING"

def on_key_down(key):
    global projectiles
    if state == "PLAYING":
        if key in (keys.UP, keys.W): player.move(0, -1, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.DOWN, keys.S): player.move(0, 1, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.LEFT, keys.A): player.move(-1, 0, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.RIGHT, keys.D): player.move(1, 0, GRID_W, GRID_H, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
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
                start_camera_transition()
    elif state in ("GAME_OVER", "VICTORY"):
        state = "MENU"

pgzrun.go()