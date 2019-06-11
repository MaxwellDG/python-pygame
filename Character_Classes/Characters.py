import pygame
import random
from Sprites import Sprite_Animation
import gc
pygame.init()


class Character(object):

    def __init__(self, name, x_loc, y_loc, movement_x, movement_y, up_sprite, down_sprite, left_sprite, right_sprite, total_hp):
        self.name = name
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkcount = 3
        self.up_sprite = up_sprite
        self.down_sprite = down_sprite
        self.left_sprite = left_sprite
        self.right_sprite = right_sprite
        self.width = 64
        self.height = 64
        self.hitbox = (self.x_loc, self.y_loc, self.width, self.height)
        self.saiyan = False
        self.pretty = False
        self.inventory = []
        self.alive = True
        self.total_hp = total_hp


class Boss(Character):
    def __init__(self, name, x_loc, y_loc, movement_x, movement_y, up_sprite, down_sprite, left_sprite, right_sprite, total_hp, width,
                 height):
        super().__init__(name, x_loc, y_loc, movement_x, movement_y, up_sprite, down_sprite, left_sprite, right_sprite, total_hp)
        self.width = width
        self.height = height
        self.hitbox = (self.x_loc, self.y_loc, self.width, self.height)
        self.alive = True
        self.walkcount = 3
        self.bot_dest = random.randint(300, 500)
        self.top_dest = random.randint(100, 299)
        self.right_dest = random.randint(200, 390)
        self.left_dest = random.randint(100, 199)
        self.reached = True
        self.direction = 1

    def shoot(self, shooter, surface, shoot_list, color, shot_num, target):
        if round(self.walkcount) % 3 == 0 and len(shoot_list) < shot_num and self.direction == 1:
            shoot_list.append(Kamahamaha(shooter, round(self.x_loc + (self.width / 2)), (self.y_loc + self.height),
                                         pygame.draw.circle(surface, color, (round(self.x_loc + (self.width / 2)),
                                                            (self.y_loc + self.height)), 8), "down"))
        elif round(self.walkcount) % 3 == 0 and len(shoot_list) < shot_num and self.direction == 2:
            shoot_list.append(Kamahamaha(shooter, round(self.x_loc + (self.width / 2)), self.y_loc,
                                         pygame.draw.circle(surface, color, (round(self.x_loc + self.width / 2),
                                                            self.y_loc), 8), "up"))
        elif round(self.walkcount) % 3 == 0 and len(shoot_list) < shot_num and self.direction == 3:
            if self.x_loc < target.x_loc:
                shoot_list.append(Kamahamaha(shooter, (self.x_loc + self.width), round(self.y_loc + self.height/2),
                                             pygame.draw.circle(surface, color,
                                             (self.x_loc + self.width, round(self.y_loc + self.height/2)), 8), "right"))
        elif round(self.walkcount) % 3 == 0 and len(shoot_list) < shot_num and self.direction == 4:
            if self.x_loc > target.x_loc:
                shoot_list.append(Kamahamaha(shooter, self.x_loc, round(self.y_loc + self.height/2),
                                             pygame.draw.circle(surface, color,
                                             (self.x_loc, round(self.y_loc + self.height/2)), 8), "left"))
        return shoot_list

    def which_direction(self):
        if self.walkcount >= 9:
            self.walkcount = 3
        if self.reached:
            self.direction = random.choice([1, 2, 3, 4])
        else:
            pass

    def move_blit(self, surface):
        if self.direction == 1:
            surface.blit(self.down_sprite[round(self.walkcount) % 3], (self.x_loc, self.y_loc))
        elif self.direction == 2:
            surface.blit(self.up_sprite[round(self.walkcount) % 3], (self.x_loc, self.y_loc))
        elif self.direction == 3:
            surface.blit(self.right_sprite[round(self.walkcount) % 3], (self.x_loc, self.y_loc))
        elif self.direction == 4:
            surface.blit(self.left_sprite[round(self.walkcount) % 3], (self.x_loc, self.y_loc))

    def move(self):
        self.reached = False
        if self.direction == 1:
            self.y_loc += self.movement_y
            self.walkcount += 1
            if self.y_loc >= self.bot_dest:
                self.bot_dest = random.randint(300, 500)
                self.reached = True
        elif self.direction == 2:
            self.y_loc -= self.movement_y
            self.walkcount += 1
            if self.y_loc <= self.top_dest:
                self.top_dest = random.randint(50, 200)
                self.reached = True
        elif self.direction == 3:
            self.x_loc += self.movement_x
            self.walkcount += 1
            if self.x_loc >= self.right_dest:
                self.right_dest = random.randint(200, 390)
                self.reached = True
        elif self.direction == 4:
            self.x_loc -= self.movement_x
            self.walkcount += 1
            if self.x_loc <= self.left_dest:
                self.left_dest = random.randint(100, 199)
                self.reached = True
        self.hitbox = (self.x_loc, self.y_loc, self.width, self.height)

    def teleport(self):
        self.reached = False
        if self.direction == 1:
            self.x_loc = 410
            self.y_loc = 115
            self.walkcount += .1
            if self.walkcount >= 9:
                self.reached = True
        elif self.direction == 2:
            self.x_loc = 410
            self.y_loc = 495
            self.walkcount += .1
            if self.walkcount >= 9:
                self.reached = True
        elif self.direction == 3:
            self.x_loc = 150
            self.y_loc = 330
            self.walkcount += .1
            if self.walkcount >= 9:
                self.reached = True
        elif self.direction == 4:
            self.x_loc = 690
            self.y_loc = 330
            self.walkcount += .1
            if self.walkcount >= 9:
                self.reached = True
        self.hitbox = (self.x_loc, self.y_loc, self.width, self.height)

    def slide(self):
        if self.movement_x > 0:
            self.x_loc += self.movement_x
            self.walkcount += 1
            if self.x_loc >= 700:
                self.movement_x = self.movement_x * -1
        elif self.movement_x < 0:
            self.x_loc += self.movement_x
            self.walkcount += 1
            if self.x_loc <= 200:
                self.movement_x = self.movement_x * -1
        self.hitbox = (self.x_loc, self.y_loc, self.width, self.height)

    def side_lazer(self, shooter, surface, shoot_list, color, shot_num, target):
        if round(self.walkcount) % 10 == 0 and len(shoot_list) < shot_num:
            if self.x_loc < target.x_loc:
                shoot_list.append(Kamahamaha(shooter, (self.x_loc + self.width), round(self.y_loc + self.height/2),
                                             pygame.draw.circle(surface, color,
                                             (self.x_loc + self.width, round(self.y_loc + self.height/2)), 30), "right"))
            elif self.x_loc >= target.x_loc:
                shoot_list.append(Kamahamaha(shooter, self.x_loc, round(self.y_loc + self.height / 2),
                                             pygame.draw.circle(surface, color,
                                             (self.x_loc, round(self.y_loc + self.height / 2)), 30), "left"))


class TextBox(object):

    def __init__(self, color, x, y, width, height, bordersize=0):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bordersize = bordersize

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), self.bordersize)


class Button(TextBox):

    def clickable(self, position):
        if self.x <= position[0] <= (self.x + self.width) and self.y <= position[1] <= (self.y + self.height):
            return True
        else:
            return False


class Scenery(object):

    def __init__(self, name, x_loc, y_loc, width, height, image):
        self.name = name
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.width = width
        self.height = height
        self.image = image
        self.hitbox = (self.x_loc, self.y_loc, self.width, self.height)
        self.opened = False
        self.observed = False

    @classmethod
    def tree(cls, x_loc, y_loc):
        return cls("A tree", x_loc, y_loc, 64, 64, Sprite_Animation.random_tree)

    @classmethod
    def wall(cls, x_loc, y_loc):
        return cls("A rock wall", x_loc, y_loc, 64, 64, Sprite_Animation.random_rock_wall)

    @classmethod
    def stairs(cls, x_loc, y_loc):
        return cls("A stairwell", x_loc, y_loc, 64, 64, Sprite_Animation.stairwell)

    @classmethod
    def pillar(cls, x_loc, y_loc):
        return cls("A pillar", x_loc, y_loc, 80, 161, Sprite_Animation.random_pillar)

    @classmethod
    def sign(cls, x_loc, y_loc):
        return cls("A sign", x_loc, y_loc, 64, 64, Sprite_Animation.the_sign)

    @classmethod
    def treasure(cls, x_loc, y_loc):
        return cls("A box of treasure", x_loc, y_loc, 128, 128, Sprite_Animation.treasure_closed)

    def end_game(self):
        if self.observed:
            pass


class Kamahamaha(object):

    def __init__(self, shooter, x, y, image, facing):
        self.shooter = shooter
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.velocity = 30
        self.image = image
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.damage = 1
        self.facing = facing




class HealthBar(object):

    def __init__(self, x, y, height, width, totalhp, currenthp):
        self.x = x
        self.y = y
        self. height = height
        self.width = width
        self.totalhp = totalhp
        self.currenthp = currenthp
