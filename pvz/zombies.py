import arcade
import animation
from constants import *

class Zombie(animation.Animation):
    def __init__(self, image, hp, row, y, window):
        super().__init__(image, 1)
        self.hp = hp
        self.row = row
        self.window = window
        self.change_x = -0.5
        self.center_y = y
        self.center_x = SCREEN_WIDTH +30
        self.eating = False

    def update(self):
        if self.hp <= 0:
            self.kill()
            self.window.killed += 1
        if not self.eating:
            self.center_x = self.center_x + self.change_x
        hits = arcade.check_for_collision_with_list(self, self.window.plants)
        self.eating = False    
        if hits:
            for i in hits:
                if i.row == self.row:
                    self.eating = True
                    i.hp -= 0.5
        if self.right<240:
            self.window.game = False





class Ordianry_zombie(Zombie):
    def __init__(self, row, y, window):
        super().__init__("zombies\OrdinaryZombie\Zombie_0.png", 80, row, y, window)
        for i in range(22):
            self.textures.append(arcade.load_texture(f"zombies\OrdinaryZombie\Zombie_{i}.png"))


class Conehead_zombie(Zombie):
    def __init__(self, row, y, window):
        super().__init__("zombies\ConeheadZombie\ConeheadZombie_0.png", 120, row, y, window)
        for i in range(21):
            self.textures.append(arcade.load_texture(f"zombies\ConeheadZombie\ConeheadZombie_{i}.png"))


class Buckethead_zombie(Zombie):
    def __init__(self, row, y, window):
        super().__init__("zombies\BucketheadZombie\BucketheadZombie_0.png", 160, row, y, window)
        for i in range(15):
            self.textures.append(arcade.load_texture(f"zombies\BucketheadZombie\BucketheadZombie_{i}.png"))

