# projectile.py

class Projectile:
    def __init__(self, actor_class, x, y, dx, dy, damage):
        self.sprite = actor_class('projectile_idle')
        self.sprite.x = x
        self.sprite.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 10
        self.damage = damage
        self.active = True
        self.off_screen_timer = 0

    def update(self, width, height, enemies, boss):
        if not self.active: return

        self.sprite.x += self.dx * self.speed
        self.sprite.y += self.dy * self.speed

        hit_target = False
        for e in enemies:
            if e.hp > 0 and self.sprite.colliderect(e.sprite):
                e.hp -= self.damage
                hit_target = True
                break
        
        if not hit_target and boss and boss.hp > 0 and self.sprite.colliderect(boss.sprite):
            boss.hp -= self.damage
            hit_target = True

        if hit_target:
            self.active = False
            return

        is_off_screen = (self.sprite.right < 0 or self.sprite.left > width or 
                         self.sprite.bottom < 0 or self.sprite.top > height)

        if is_off_screen:
            self.off_screen_timer += 1
            if self.off_screen_timer >= 120:  
                self.active = False

    def draw(self):
        if self.active: self.sprite.draw()