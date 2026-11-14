import arcade

class Animation(arcade.Sprite):
    i = 0
    frame_time = 0
    anim_speed = 0.1
    def update_animation(self, delta_time):
        self.frame_time += delta_time
        if self.frame_time >= self.anim_speed:
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.texture = self.textures[self.i]
            self.frame_time = 0