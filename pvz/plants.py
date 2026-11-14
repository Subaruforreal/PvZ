import arcade
import animation
import time
import random
import zombies


class Plants(animation.Animation):
    def __init__(self, image, hp, cost, window):
        super().__init__(image, 0.15)
        self.hp = hp
        self.cost = cost
        self.window = window

    def planting(self, x, y, column, row):
        self.row = row
        self.column = column
        self.center_x = x
        self.center_y = y

    def update(self):
        if self.hp <= 0:
            self.kill()
            self.window.lawns.remove((self.column, self.row))



class Sunflower(Plants):
    def __init__(self, window):
        super().__init__("plants/sun1.png", 100, 50, window)
        self.textures.append(arcade.load_texture("plants/sun2.png"))
        self.anim_speed = 0.2
        self.sun_time = time.time()
        self.sun_sound = arcade.load_sound("sounds\sunspawn.mp3")

    def update(self):
        super().update()
        if time.time() - self.sun_time >= 8:
            sun = Sun()
            sun.center_x = self.center_x + random.randint(-20, 20)
            sun.center_y = self.center_y + random.randint(-20, 20)
            self.window.suns.append(sun)
            arcade.play_sound(self.sun_sound, 2)
            self.sun_time = time.time()




class Sun(arcade.Sprite):
    def __init__(self):
        super().__init__("items/sun.png", 0.2)
        self.kill_timer = time.time()
        
    def update(self):
        self.angle +=0.1
        if time.time() - self.kill_timer >= 5:
            self.kill()

    


class Peashooter(Plants):
    def __init__(self, window):
        super().__init__("plants/pea1.png",  100, 100, window)
        self.textures.append(arcade.load_texture("plants/pea2.png"))
        self.textures.append(arcade.load_texture("plants/pea3.png"))
        self.anim_speed = 0.2
        self.pea_timer = time.time()
        self.shoot_sound = arcade.load_sound("sounds\hit.mp3")

    def update(self):

        for i in self.window.zombies:
            if i.row == self.row:
                if time.time() - self.pea_timer > 1.5:
                    pea = Pea(self.window)
                    pea.center_x = self.center_x
                    pea.center_y = self.center_y + 10
                    self.window.peas.append(pea)
                    arcade.play_sound(self.shoot_sound, 1.3)
                    self.pea_timer = time.time()
                    

class Pea(arcade.Sprite):
    def __init__(self, window):
        super().__init__("items/bul.png", 0.1)
        self.change_x = 5
        self.window = window
        self.dmg = 10
        

    def update(self):
        self.center_x = self.center_x + self.change_x
        self.hits = arcade.check_for_collision_with_list(self,self.window.zombies)
        if self.hits:
            self.kill()
            for i in self.hits:
                i.hp -= self.dmg




class Nut(Plants):
    def __init__(self, window):
        super().__init__("plants/nut1.png", 600, 50, window)
        self.textures.append(arcade.load_texture("plants/nut2.png"))
        self.textures.append(arcade.load_texture("plants/nut3.png"))
        self.anim_speed = 0.3


class Tree(Plants):
    def __init__(self, window):
        super().__init__("plants/tree1.png", 100, 175, window)
        self.textures.append(arcade.load_texture("plants/tree2.png"))
        self.textures.append(arcade.load_texture("plants/tree3.png"))
        
    def update(self):
        fire_hit = arcade.check_for_collision_with_list(self, self.window.peas)
        if fire_hit:
            for i in fire_hit:
                i.texture = arcade.load_texture("items/firebul.png")
                i.dmg = 20

