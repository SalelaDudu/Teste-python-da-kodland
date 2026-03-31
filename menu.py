from pygame import Rect

class Menu:
    def __init__(self, width, height, actor_class):
        btn_w, btn_h = 430, 100
        center_x = width // 2 - btn_w // 2
        
        margin = 30 
        
        self.cover = actor_class('menu_cover')
        self.cover.center = (width // 2, height // 2)
        
        start_y = 250 
        sound_y = start_y + btn_h + margin
        exit_y = sound_y + btn_h + margin
        
        self.start_btn = Rect(center_x, start_y, btn_w, btn_h)
        self.sound_btn = Rect(center_x, sound_y, btn_w, btn_h)
        self.exit_btn = Rect(center_x, exit_y, btn_w, btn_h)
        self.sound_on = True

    def draw(self, screen):
        self.cover.draw()
        
        screen.draw.filled_rect(self.start_btn, (50, 150, 50))
        screen.draw.text("Comecar Jogo", center=self.start_btn.center, color="white", fontname="pixeled")

        sound_color = (50, 150, 150) if self.sound_on else (150, 50, 50)
        screen.draw.filled_rect(self.sound_btn, sound_color)
        status_text = "Ligado" if self.sound_on else "Desligado"
        screen.draw.text(f"Musica e Sons: {status_text}", center=self.sound_btn.center, color="white", fontname="pixeled")

        screen.draw.filled_rect(self.exit_btn, (150, 50, 50))
        screen.draw.text("Saida", center=self.exit_btn.center, color="white", fontname="pixeled")

    def handle_click(self, pos):
        if self.start_btn.collidepoint(pos): return "START"
        if self.sound_btn.collidepoint(pos):
            self.sound_on = not self.sound_on
            return "SOUND"
        if self.exit_btn.collidepoint(pos): return "EXIT"
        return None