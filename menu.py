# menu.py
from pygame import Rect

class Menu:
    def __init__(self, width, height):
        btn_w, btn_h = 200, 50
        center_x = width // 2 - btn_w // 2
        
        self.start_btn = Rect(center_x, 200, btn_w, btn_h)
        self.sound_btn = Rect(center_x, 300, btn_w, btn_h)
        self.exit_btn = Rect(center_x, 400, btn_w, btn_h)
        self.sound_on = True

    def draw(self, screen):
        screen.fill((30, 30, 30))
        screen.draw.filled_rect(self.start_btn, (50, 150, 50))
        screen.draw.text("Start Game", center=self.start_btn.center, color="white")

        sound_color = (50, 150, 150) if self.sound_on else (150, 50, 50)
        screen.draw.filled_rect(self.sound_btn, sound_color)
        status_text = "ON" if self.sound_on else "OFF"
        screen.draw.text(f"Sound: {status_text}", center=self.sound_btn.center, color="white")

        screen.draw.filled_rect(self.exit_btn, (150, 50, 50))
        screen.draw.text("Exit", center=self.exit_btn.center, color="white")

    def handle_click(self, pos):
        if self.start_btn.collidepoint(pos): return "START"
        if self.sound_btn.collidepoint(pos):
            self.sound_on = not self.sound_on
            return "SOUND"
        if self.exit_btn.collidepoint(pos): return "EXIT"
        return None