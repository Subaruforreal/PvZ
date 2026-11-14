import arcade
import plants
import zombies
import time
import random
from constants import *




class Game(arcade.Window):
    def __init__(self):
        super().__init__(1000, 800)
        self.bg = arcade.load_texture("textures/background.jpg")
        self.vertical_menu = arcade.load_texture("textures/menu_vertical.png")
        self.plants = arcade.SpriteList()
        self.seed = None
        self.seed_sound = arcade.load_sound("sounds/seed.mp3")
        self.lawns = []
        self.zombies = arcade.SpriteList()
        self.zombie_time = time.time()
        self.suns = arcade.SpriteList()
        self.money = 150
        self.peas = arcade.SpriteList()
        self.win = False   
        self.game = True  
        self.loose = arcade.load_texture("textures/end.png")    
        self.win_texture = arcade.load_texture("textures/logo.png")
        self.killed = 0
        self.zombie_amount = 0   
        self.bg_music = arcade.load_sound("sounds/grasswalk.mp3") 
        arcade.play_sound(self.bg_music, 0.3, looping=True)               
        
        






    def on_draw(self):
        arcade.draw_texture_rectangle(self.width/2, self.height/2, self.width, self.height, self.bg)
        arcade.draw_texture_rectangle(75, self.height/2, 150, self.height, self.vertical_menu)
        self.plants.draw()
        self.zombies.draw()
        self.suns.draw()
        self.peas.draw()
        arcade.draw_text(self.money, 53, SCREEN_HEIGHT-140, arcade.color.WHITE, 50)
        if self.seed != None:
            self.seed.draw()
        if not self.game and not self.win:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2+50, SCREEN_HEIGHT/2, SCREEN_WIDTH/1.5, SCREEN_HEIGHT/1.5, self.loose)
        if not self.game and self.win:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2+50, SCREEN_HEIGHT/2, SCREEN_WIDTH/1.5, SCREEN_HEIGHT/1.5, self.win_texture)


    def update(self, delta_time):
        if self.game:
            self.plants.update()
            self.plants.update_animation(delta_time)
            self.zombies.update()
            self.zombies.update_animation(delta_time)
            self.suns.update()
            self.peas.update()
            if time.time() - self.zombie_time >= 8 and ALL_ZOMBIES > self.zombie_amount:
                y, row = self.y_leveling(random.randint(35, 680))

                if self.zombie_amount>=4:
                    zombie_num = random.randint(1, 5)
                    
                    if 1<= zombie_num <=3:
                        zombie = zombies.Ordianry_zombie(row, y, self)
                    elif zombie_num == 4:
                        zombie = zombies.Buckethead_zombie(row, y, self)
                    else:
                        zombie = zombies.Conehead_zombie(row, y, self)
                else:
                    zombie = zombies.Ordianry_zombie(row, y, self)     


                print(zombie.row)
                self.zombies.append(zombie)
                self.zombie_amount += 1
                self.zombie_time = time.time()

            if self.killed == ALL_ZOMBIES:
                self.win = True
                self.game = False
            
        



    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)

        
        for sun in self.suns:
            if sun.left <= x <= sun.right and sun.top >= y >= sun.bottom:
                sun.kill()
                self.money += 25



        if 15<=  x  <=130 and button==arcade.MOUSE_BUTTON_LEFT:
            if 40<=  y  <=180:
                self.seed = plants.Tree(self)
            if 195<=  y  <=335:
                self.seed = plants.Nut(self)
            if 345<=  y  <=490:
                self.seed = plants.Peashooter(self)
            if 500<=  y  <=640:
                self.seed = plants.Sunflower(self)
            

            if self.seed != None:
                if self.seed.cost > self.money:
                    self.seed = None
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 120

            
        if button==arcade.MOUSE_BUTTON_RIGHT:
            self.seed = None


        

    def on_mouse_release(self, x, y, button, modifiers):
        if 245<= x <=960 and 35<= y <= 680:
            if self.seed != None:
                pos_x, col = self.x_leveling(x)
                pos_y, row = self.y_leveling(y)
                
                if (col, row) not in self.lawns and self.money >= self.seed.cost:
                    self.money = self.money-self.seed.cost
                    self.lawns.append((col, row))
                    self.seed.planting(pos_x, pos_y, col, row)
                    self.seed.alpha = 255
                    self.plants.append(self.seed)
                    self.seed = None
                    arcade.play_sound(self.seed_sound)



    def on_mouse_motion(self, x, y, dx, dy):
        if self.seed != None:
            self.seed.center_x = x
            self.seed.center_y = y

    
    def x_leveling(self, x):
        col = x// CELL_WIDTH +1
        x = col*CELL_WIDTH-CELL_WIDTH/2
        return x, col
    
    def y_leveling(self, y):
        row = (y-35)// CELL_HEIGHT +1
        y = row*CELL_HEIGHT-CELL_HEIGHT/2 +35
        return y, row





window = Game()

arcade.run()
