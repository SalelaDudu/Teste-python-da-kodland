# main.py
import pgzrun
from pygame import Rect
from settings import *
from player import Player
# Importa os novos inimigos
from enemy import Enemy, Enemy2, Enemy3, Boss 
from menu import Menu
from world import RoomManager, Item
from projectile import Projectile

state = "MENU"
menu = Menu(WIDTH, HEIGHT, Actor)
player = None
room_mgr = None
active_items = []
projectiles = []

cam_x, cam_y = 0, 0
cam_target_x, cam_target_y = 0, 0
old_room_data = {}

def generate_items():
    global active_items
    active_items.clear()
    types = ['Health', 'Speed', 'Damage']
    spacing = 260
    start_x = WIDTH // 2 - spacing
    for i, t in enumerate(types):
        r = Rect(start_x + i * spacing - 100, HEIGHT // 2 - 100, 200, 200)
        active_items.append(Item(t, r))

def start_camera_transition():
    global state, cam_x, cam_y, cam_target_x, cam_target_y, old_room_data
    old_room_data = {
        'cols': room_mgr.cols, 'rows': room_mgr.rows,
        'offset_x': room_mgr.offset_x, 'offset_y': room_mgr.offset_y,
        'floor_tex': room_mgr.floor_tex, 'door_pos': room_mgr.door_pos,
        'door_tex': room_mgr.door_tex
    }
    room_mgr.current_room += 1
    state = "TRANSITION"
    cam_x, cam_y = 0, 0
    
    if room_mgr.current_room in (2, 3): cam_target_x, cam_target_y = 0, -HEIGHT
    elif room_mgr.current_room == 4: cam_target_x, cam_target_y = WIDTH, 0
        
    projectiles.clear()
    room_mgr.load_room(player)

def reset_game():
    global player, room_mgr, state, projectiles
    player = Player(Actor, TILE_SIZE)
    # Passa as novas classes para o RoomManager
    room_mgr = RoomManager(Actor, Enemy, Enemy2, Enemy3, Boss, TILE_SIZE, WIDTH, HEIGHT)
    projectiles.clear()
    room_mgr.load_room(player)
    state = "PLAYING"
    
    if menu.sound_on:
        try: 
            music.play("bg_music")
            music.set_volume(0.3)
        except: pass

def draw_room_textures(screen, cols, rows, ox, oy, floor_tex, door_tex, door_pos, cam_ox, cam_oy):
    start_x = ox + cam_ox
    start_y = oy + cam_oy
    
    for c in range(cols):
        for r in range(rows):
            screen.blit(floor_tex, (start_x + c * TILE_SIZE, start_y + r * TILE_SIZE))
            
    if door_pos is not None:
        dx, dy = door_pos
        screen.blit(door_tex, (start_x + dx * TILE_SIZE, start_y + dy * TILE_SIZE))

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
        
    elif state == "TUTORIAL":
        screen.fill((0, 0, 0))
        screen.draw.text("Use WASD ou os direcionais para se movimentar,", center=(WIDTH//2, HEIGHT//2 - 60), color="white", fontname="pixeled", fontsize=20)
        screen.draw.text("use 'barra de espaco' para atacar", center=(WIDTH//2, HEIGHT//2 - 20), color="white", fontname="pixeled", fontsize=20)
        screen.draw.text("Cuidado com os inimigos", center=(WIDTH//2, HEIGHT//2 + 40), color="white", fontname="pixeled", fontsize=20)
        screen.draw.text("Aperte espaco para avancar", center=(WIDTH//2, HEIGHT//2 + 120), color="yellow", fontname="pixeled", fontsize=25)
        
    elif state in ("PLAYING", "ITEM_SELECT"):
        screen.fill((20, 20, 20)) 
        
        draw_room_textures(screen, room_mgr.cols, room_mgr.rows, room_mgr.offset_x, room_mgr.offset_y, 
                           room_mgr.floor_tex, room_mgr.door_tex, room_mgr.door_pos, 0, 0)

        for t in room_mgr.traps: t.draw()
        for e in room_mgr.enemies: e.draw()
        if room_mgr.boss: room_mgr.boss.draw()
        for p in projectiles: p.draw()
        player.draw()

        screen.draw.text(f"HP: {player.hp}/{player.max_hp}", topleft=(10, 10), color="white", fontname="pixeled", fontsize=30)
        screen.draw.text(f"ROOM: {room_mgr.current_room}", topright=(WIDTH - 10, 10), color="white", fontname="pixeled", fontsize=30)

        if room_mgr.boss:
            bar_w, bar_h = 400, 20
            px, py = WIDTH // 2 - bar_w // 2, HEIGHT - 40
            screen.draw.filled_rect(Rect(px, py, bar_w, bar_h), (100, 0, 0))
            current_w = int(bar_w * (max(0, room_mgr.boss.hp) / room_mgr.boss.max_hp))
            if current_w > 0:
                screen.draw.filled_rect(Rect(px, py, current_w, bar_h), (255, 0, 0))
            screen.draw.text("BOSS", center=(WIDTH//2, py - 15), color="white", fontname="pixeled")

        if state == "ITEM_SELECT":
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 150))
            screen.draw.text("CHOOSE AN UPGRADE", center=(WIDTH//2, 100), color="white", fontname="pixeled", fontsize=50)
            for item in active_items: item.draw(screen)
            
    elif state == "TRANSITION":
        screen.fill((20, 20, 20))
        old_cam_ox, old_cam_oy = -cam_x, -cam_y
        draw_room_textures(screen, old_room_data['cols'], old_room_data['rows'], old_room_data['offset_x'], old_room_data['offset_y'],
                           old_room_data['floor_tex'], old_room_data['door_tex'], old_room_data['door_pos'], old_cam_ox, old_cam_oy)
        
        new_cam_ox = cam_target_x - cam_x
        new_cam_oy = cam_target_y - cam_y
        draw_room_textures(screen, room_mgr.cols, room_mgr.rows, room_mgr.offset_x, room_mgr.offset_y,
                           room_mgr.floor_tex, room_mgr.door_tex, room_mgr.door_pos, new_cam_ox, new_cam_oy)
        
        for t in room_mgr.traps: draw_with_offset(t, new_cam_ox, new_cam_oy)
        for e in room_mgr.enemies: draw_with_offset(e, new_cam_ox, new_cam_oy)
        if room_mgr.boss: draw_with_offset(room_mgr.boss, new_cam_ox, new_cam_oy)
        draw_with_offset(player, new_cam_ox, new_cam_oy)

    elif state == "GAME_OVER":
        screen.fill((100, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white", fontname="pixeled")
    elif state == "VICTORY":
        screen.fill((0, 100, 0))
        screen.draw.text("YOU WON!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white", fontname="pixeled")

def update():
    global state, projectiles, cam_x, cam_y
    if state == "PLAYING":
        
        prev_p_hp = player.hp
        prev_e_hp = sum(e.hp for e in room_mgr.enemies)
        if room_mgr.boss: prev_e_hp += room_mgr.boss.hp
        
        player.update()
        for p in projectiles: p.update(WIDTH, HEIGHT, room_mgr.enemies, room_mgr.boss)
        projectiles = [p for p in projectiles if p.active]
        
        room_mgr.enemies = [e for e in room_mgr.enemies if e.hp > 0]
        if room_mgr.boss and room_mgr.boss.hp <= 0: room_mgr.boss = None

        for e in room_mgr.enemies: e.update(player.speed, player)
        if room_mgr.boss: room_mgr.boss.update(player.speed, player)

        curr_e_hp = sum(e.hp for e in room_mgr.enemies)
        if room_mgr.boss: curr_e_hp += room_mgr.boss.hp
        
        if menu.sound_on:
            if player.hp < prev_p_hp:
                try: sounds.hurt_sound.play()
                except: pass
            if curr_e_hp < prev_e_hp:
                try: sounds.hit_sound.play()
                except: pass

        if player.hp <= 0: 
            state = "GAME_OVER"
            try: music.stop()
            except: pass
            
        if not room_mgr.enemies and not room_mgr.boss:
            if room_mgr.current_room < 4:
                state = "ITEM_SELECT"
                generate_items()
            else:
                state = "VICTORY"
                try: music.stop()
                except: pass
                
    elif state == "TRANSITION":
        cam_speed = 15
        if cam_x < cam_target_x: cam_x = min(cam_x + cam_speed, cam_target_x)
        elif cam_x > cam_target_x: cam_x = max(cam_x - cam_speed, cam_target_x)
        if cam_y < cam_target_y: cam_y = min(cam_y + cam_speed, cam_target_y)
        elif cam_y > cam_target_y: cam_y = max(cam_y - cam_speed, cam_target_y)
        if cam_x == cam_target_x and cam_y == cam_target_y: state = "PLAYING"

def on_key_down(key):
    global projectiles
    
    if state == "TUTORIAL":
        if key == keys.SPACE:
            reset_game()
            
    elif state == "PLAYING":
        if key in (keys.UP, keys.W): player.move(0, -1, room_mgr.cols, room_mgr.rows, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.DOWN, keys.S): player.move(0, 1, room_mgr.cols, room_mgr.rows, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.LEFT, keys.A): player.move(-1, 0, room_mgr.cols, room_mgr.rows, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key in (keys.RIGHT, keys.D): player.move(1, 0, room_mgr.cols, room_mgr.rows, room_mgr.enemies, room_mgr.boss, room_mgr.traps)
        elif key == keys.SPACE:
            p = Projectile(Actor, player.sprite.x, player.sprite.y, player.last_dir[0], player.last_dir[1], player.damage)
            projectiles.append(p)

def on_mouse_down(pos):
    global state
    if state == "MENU":
        action = menu.handle_click(pos)
        if action == "START": 
            state = "TUTORIAL"
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