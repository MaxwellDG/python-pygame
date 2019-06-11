import pygame
import random
from Character_Classes import Characters
from Sprites import Sprite_Animation

pygame.init()
reso_x = 1000
reso_y = 700
screen = pygame.display.set_mode((reso_x, reso_y))
title = pygame.display.set_caption("JRPG Game", "JRPG Game")
intro_background = pygame.image.load('../Sprites/Parchment_Background.png')

textbox_color = (209, 176, 99)
textbox_border_color = (0, 0, 0)
textbox_y = (reso_y / 1.7)
textbox_x = reso_x / 10
textbox_width = (reso_x - (textbox_x * 2))
textbox_height = (reso_y / 3)
health_x = reso_x - 200
health_y = reso_y - 80


def create_text(surface, text, textbox, border, text2=None):
    textbox.draw(screen)
    border.draw(screen)
    if text2 is None:
        rect = text.get_rect(center=(textbox.x + textbox.width/2, textbox.y + textbox.height/2))
        surface.blit(text, rect)
    elif text2 is not None:
        rect = text.get_rect(center=(textbox.x + textbox.width / 2, textbox.y + textbox.height / 3))
        rect2 = text.get_rect(center=(textbox.x + textbox.width / 2, textbox.y + textbox.height / 1.5))
        surface.blit(text, rect)
        surface.blit(text2, rect2)


def char_select(select):
    if select == "girl":
        char = Characters.Character("Martha", (reso_x / 2), (reso_y / 2), 20, 20, Sprite_Animation.mar_up_sprite,
                                    Sprite_Animation.mar_down_sprite,
                                    Sprite_Animation.mar_left_sprite, Sprite_Animation.mar_right_sprite, 10)
        return char
    elif select == "boy":
        char = Characters.Character("Jeremy", (reso_y / 2), (reso_y / 2), 20, 20, Sprite_Animation.jer_up_sprite,
                                    Sprite_Animation.jer_down_sprite,
                                    Sprite_Animation.jer_left_sprite, Sprite_Animation.jer_right_sprite, 10)
        return char


def cursor(position, x_start, x_width, y_start, y_width, x2start, x2_width, y2_start, y2_width):
    if x_start <= position[0] <= (x_start + x_width) and y_start <= position[1] <= (y_start + y_width) or (x2start <= position[0] <= (x2start + x2_width) and y2_start <= position[1] <= (y2_start + y2_width)):
        return pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    else:
        return pygame.mouse.set_cursor(*pygame.cursors.arrow)


# ---------------- Prepping font types and renderings -------------------- #
intro_font = pygame.font.SysFont('litosscript', 90, True, False)
intro_font_lower = pygame.font.SysFont('eightbitdragon', 30)
greeting = intro_font.render("Welcome!", 1, (0, 0, 0))
sex_question = intro_font_lower.render("Are you a boy or a girl?", 1, (0, 0, 0))
health_text = intro_font_lower.render("Health:", 1, (0, 0, 0))


# --------------- Initializing text-boxes and buttons -------------------- #
textbox1 = Characters.TextBox(textbox_color, textbox_x, textbox_y, textbox_width, textbox_height)
textbox1border = Characters.TextBox(textbox_border_color, textbox_x, textbox_y, textbox_width, textbox_height, 5)

boy_button_x = (reso_x / 4 + 50)
boy_button_y = textbox1.y + textbox1.height - 128 - 15
girl_button_x = (reso_x * .55)
girl_button_y = textbox1.y + textbox1.height - 128 - 15
boy_button = Characters.Button((0, 0, 0), boy_button_x, boy_button_y, 128, 128, 5)
girl_button = Characters.Button((0, 0, 0), girl_button_x, girl_button_y, 128, 128, 5)

# --------------- Start of IntroScreen While Loop ------------------------ #
intro_run = True
animate_walk_count = 3

while intro_run:

    if animate_walk_count > 20:
        animate_walk_count = 1

    for event in pygame.event.get():
        position = pygame.mouse.get_pos()
        print(position)
        if event == pygame.QUIT:
            intro_run = False
            pygame.quit()

        # this is why the cursor stays retarded
        cursor(position, girl_button.x, girl_button.width, girl_button.y, girl_button.height,
               boy_button_x, boy_button.width, boy_button_y, boy_button.height)

        if event.type == pygame.MOUSEBUTTONDOWN:
            girl_button.clickable(position)
            if girl_button.clickable(position):
                char = char_select("girl")
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                intro_run = False
            boy_button.clickable(position)
            if boy_button.clickable(position):
                char = char_select("boy")
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                intro_run = False

    screen.blit(intro_background, (0, 0))
    greeting_rect = greeting.get_rect()
    screen.blit(greeting, (reso_x/2 - greeting_rect[2]/2, reso_y/8))
    textbox1.draw(screen)
    textbox1border.draw(screen)
    sex_rect = sex_question.get_rect(center=(textbox1.x + textbox1.width/2, textbox1.y + textbox1.height/5))
    screen.blit(sex_question, sex_rect)
    boy_button.draw(screen)
    girl_button.draw(screen)
    screen.blit(Sprite_Animation.jer_selector[animate_walk_count % 3], (boy_button_x, boy_button_y))
    screen.blit(Sprite_Animation.mar_selector[animate_walk_count % 3], (girl_button_x, girl_button_y))
    animate_walk_count += 1

    pygame.display.update()
    pygame.time.delay(500)

# ------------------ End of IntroScreen While Loop ------------ #

# ------------------ Initializations and object creation------------- #
toon = char

stairs1 = Characters.Scenery.stairs(25, 280)
stairs2 = Characters.Scenery.stairs(890, 280)
stairs3 = Characters.Scenery.stairs(475, 15)
stair_list_hitboxes = [stairs1.hitbox, stairs2.hitbox, stairs3.hitbox]

beams_tracker = []
bullet_tracker = []
bullet_min_tracker = []

textbox2 = Characters.TextBox(textbox_color, textbox_x + 32, textbox_y + 50, textbox_width, (textbox_height - 50))
textbox2border = Characters.TextBox(textbox_border_color, textbox_x + 32, textbox_y + 50, textbox_width, (textbox_height - 50), 5)
textbox4 = Characters.TextBox(textbox_color, textbox_x - 32, textbox_y + 50, textbox_width, (textbox_height - 50))
textbox4border = Characters.TextBox(textbox_border_color, textbox_x - 32, textbox_y + 50, textbox_width, (textbox_height - 50), 5)
textbox3 = Characters.TextBox(textbox_color, textbox_x, (reso_y / 11), textbox_width, textbox_height)
textbox3border = Characters.TextBox(textbox_border_color, textbox_x, (reso_y / 11), textbox_width, textbox_height, 5)

mission_statement = intro_font_lower.render("Your mission: Defeat Mecha-Boss C++9000.", 1, (0, 0, 0))
mission_statement2 = intro_font_lower.render("He will only fight those he deems worthy.", 1, (0, 0, 0))

mech_denied = intro_font_lower.render("You are not pretty enough.", 1, (0, 0, 0))
mech_denied2 = intro_font_lower.render("You are not wise enough.", 1, (0, 0, 0))

goblin_chirp = intro_font_lower.render("I am Cpt.SS. Defeat me and I will", 1, (0, 0, 0))
goblin_chirp2 = intro_font_lower.render("make you the prettiest.", 1, (0, 0, 0))

ninja_chirp = intro_font_lower.render("Crouching Python stance. Hyehhhhhhh!", 1, (0, 0, 0))

mech_chirp = intro_font_lower.render("You will never defeat C++9000.", 1, (0, 0, 0))

get_item1 = intro_font_lower.render("You are now the prettiest.", 1, (0, 0, 0))
get_item2 = intro_font_lower.render("You are now the wisest.", 1, (0, 0, 0,))
get_item3 = intro_font_lower.render("You mastered C++ and are the", 1, (0, 0, 0))
get_item3_2 = intro_font_lower.render("most powerful-est.", 1, (0, 0, 0))


normal_run = True
left_room = False
top_room = False
right_room = False

enter_left = False
enter_right = False
enter_top = False

goblin = Characters.Boss("Goblin", 150, 290, 10, 10, Sprite_Animation.gob_up_sprite, Sprite_Animation.gob_down_sprite,
                         Sprite_Animation.gob_left_sprite, Sprite_Animation.gob_right_sprite, 10, 64, 128)
goblin_min1 = Characters.Boss("Goblin minion", 150, 380, 5, 5, Sprite_Animation.nin_up_sprite, Sprite_Animation.nin_down_sprite,
                         Sprite_Animation.nin_left_sprite, Sprite_Animation.nin_right_sprite, 1000, 32, 32)
goblin_min2 = Characters.Boss("Goblin minion", 150, 200, 5, 5, Sprite_Animation.nin_up_sprite, Sprite_Animation.nin_down_sprite,
                         Sprite_Animation.nin_left_sprite, Sprite_Animation.nin_right_sprite, 1000, 32, 32)


mech = Characters.Boss("Mech", 450, 200, 5, 5, Sprite_Animation.mech_up_sprite,
                       Sprite_Animation.mech_down_sprite, Sprite_Animation.mech_left_sprite,
                       Sprite_Animation.mech_right_sprite, 10, 128, 128)

ninja = Characters.Boss("Ninja", (reso_x * .75), (reso_y / 2), 10, 10, Sprite_Animation.nin_up_sprite,
                        Sprite_Animation.nin_down_sprite,
                        Sprite_Animation.nin_left_sprite, Sprite_Animation.nin_right_sprite, 5, 32, 64)

treasure_box1 = Characters.Scenery.treasure((reso_x / 2.2), (reso_y / 6))
treasure_box2 = Characters.Scenery.treasure((reso_x - 275), (reso_y - 600))
treasure_box3 = Characters.Scenery.treasure(mech.x_loc, mech.y_loc)

blue_fire = Characters.Kamahamaha("me", 200, 200, Sprite_Animation.blueshot, 1)
violet_fire = Characters.Kamahamaha("me2", 700, 300, Sprite_Animation.violetshot, 1)
yellow_fire = Characters.Kamahamaha("me3", 500, 500, Sprite_Animation.yellowshot, 1)

# -------------------- F is for Functions -----------------------#

length = Sprite_Animation.lost_health.get_rect().width
health_barr = Sprite_Animation.healthbar.get_rect()
health_text_rect = health_text.get_rect()


def finished():
    screen.blit(Sprite_Animation.blueshot[int(blue_fire.velocity % 8)], (200, 200))
    screen.blit(Sprite_Animation.violetshot[int(violet_fire.velocity % 8)], (700, 300))
    screen.blit(Sprite_Animation.yellowshot[int(yellow_fire.velocity % 8)], (500, 500))

    blue_fire.velocity += .3
    yellow_fire.velocity += .3
    violet_fire.velocity += .3



def the_standard():
    screen.blit(Sprite_Animation.healthbar, (health_x, health_y))
    screen.blit(health_text, (health_x, health_y + health_text_rect.height))
    for i in range((toon.total_hp - 10) * -1):
        screen.blit(Sprite_Animation.lost_health, (health_x + health_barr.width + ((-i -1) * length) + 2, health_y + 3))

    if toon.up:
        screen.blit(toon.up_sprite[toon.walkcount % 3], (toon.x_loc, toon.y_loc))
    elif toon.left:
        screen.blit(toon.left_sprite[toon.walkcount % 3], (toon.x_loc, toon.y_loc))
    elif toon.right:
        screen.blit(toon.right_sprite[toon.walkcount % 3], (toon.x_loc, toon.y_loc))
    elif toon.down:
        screen.blit(toon.down_sprite[toon.walkcount % 3], (toon.x_loc, toon.y_loc))
    else:
        screen.blit(toon.down_sprite[toon.walkcount % 3], (toon.x_loc, toon.y_loc))

    toon.hitbox = (toon.x_loc, toon.y_loc, toon.width, toon.height)  # IMPORTANT #

    for beam in beams_tracker:
        beam.hitbox = (beam.x, beam.y, beam.width, beam.height)
        screen.blit(beam.image, (beam.x, beam.y))

    for bullet in bullet_tracker:
        bullet.hitbox = (bullet.x, bullet.y, bullet.width, bullet.height)
        if bullet.shooter == goblin:
            pygame.draw.circle(screen, (128, 200, 0), (bullet.x, bullet.y), 8)
        elif bullet.shooter == ninja:
            pygame.draw.circle(screen, (224, 224, 224), (bullet.x, bullet.y), 8)
        elif bullet.shooter == mech and bullet.y > mech.y_loc + mech.height:
            pygame.draw.circle(screen, (224, 0, 224), (bullet.x, bullet.y), 11)
        elif bullet.shooter == mech and bullet.y < mech.y_loc + mech.height:
            pygame.draw.circle(screen, (224, 0, 224), (bullet.x, bullet.y), 30)

    for bullet_min in bullet_min_tracker:
        bullet_min.hitbox = (bullet_min.x, bullet_min.y, bullet_min.width, bullet_min.height)
        pygame.draw.circle(screen, (255, 255, 102), (bullet_min.x, bullet_min.y), 4)

def beams_color(up, down, left, right):
    if 0 <= thing.x <= reso_x and 0 <= thing.y <= reso_y:
        if thing.image == up:
            thing.y -= thing.velocity
        elif thing.image == down:
            thing.y += thing.velocity
        elif thing.image == left:
            thing.x -= thing.velocity
        elif thing.image == right:
            thing.x += thing.velocity
    else:
        beams_tracker.pop(beams_tracker.index(thing))


def beam_creation(up_image, down_image, left_image, right_image):
    if toon.up:
        beams_tracker.append(Characters.Kamahamaha(toon, toon.x_loc + (toon.width / 2.5), toon.y_loc,
                                                   up_image, "up"))
    elif toon.down:
        beams_tracker.append(Characters.Kamahamaha(toon, toon.x_loc + (toon.width / 2.5), (toon.y_loc + toon.height / 2),
                                                   down_image, "down"))
    elif toon.left:
        beams_tracker.append(Characters.Kamahamaha(toon, toon.x_loc, toon.y_loc + (toon.height / 2),
                                                   left_image, "left"))
    elif toon.right:
        beams_tracker.append(Characters.Kamahamaha(toon, (toon.x_loc + toon.width / 2), toon.y_loc + (toon.height / 2),
                                                   right_image, "right"))

tree_objects = []
for i in range(10):
    tree_objects.append(Characters.Scenery.tree(random.randint(1, reso_x), random.randint(1, reso_y)))
for tree in tree_objects:
    if (0 <= tree.x_loc <= 180) or (420 <= tree.x_loc <= 480) or (800 <= tree.x_loc <= 970):
        tree_objects.pop(tree_objects.index(tree))

signs = [Characters.Scenery.sign(reso_x / 2 - toon.width, 600)]
def the_standard_scenery():

    for trees in tree_objects:
        pygame.draw.rect(screen, (255, 255, 255), trees.hitbox, 1)

    screen.blit(Sprite_Animation.background_start, (0, 0))

    for trees in tree_objects:
        screen.blit(trees.image, (trees.x_loc, trees.y_loc))

    screen.blit(Sprite_Animation.the_sign, (signs[0].x_loc, signs[0].y_loc))

    collision_course(tree_objects)
    collision_course(signs)
    get_close_sign()


wall_list_hor = []
for i in range(int(reso_x / 64) + 1):
    wall_list_hor.append(Characters.Scenery.wall((i * 64), 0))
wall_list_hor2 = []
for n in range(int(reso_x / 64) + 1):
    wall_list_hor2.append(Characters.Scenery.wall((n * 64), (reso_y - 64)))
wall_list_ver = []
for j in range(int(reso_y / 64) + 1):
    wall_list_ver.append(Characters.Scenery.wall(0, (j * 64)))
def left_room_scenery():
    screen.blit(Sprite_Animation.background_left, (0, 0))

    for k in range(int(reso_x / 64) + 1):
        screen.blit(Sprite_Animation.random_rock_wall, ((k * 64), 0))
    for l in range(int(reso_x / 64) + 1):
        screen.blit(Sprite_Animation.random_rock_wall, ((l * 64), (reso_y - 62)))
    for m in range(int(reso_y / 64) + 1):
        screen.blit(Sprite_Animation.random_rock_wall_vert, (0, (64 * m)))

    collision_course(wall_list_hor)
    collision_course(wall_list_ver)
    collision_course(wall_list_hor2)

pillar1 = Characters.Scenery.pillar(280, 90)
pillar2 = Characters.Scenery.pillar(280, 400)
pillar3 = Characters.Scenery.pillar(560, 90)
pillar4 = Characters.Scenery.pillar(560, 400)
pillar_list = [pillar1, pillar2, pillar3, pillar4]

right_wall_list_hor = []
for i in range(int(reso_x / 64) + 1):
    right_wall_list_hor.append(Characters.Scenery.wall((i * 64), 0))
right_wall_list_hor2 = []
for n in range(int(reso_x / 64) + 1):
    right_wall_list_hor2.append(Characters.Scenery.wall((n * 64), (reso_y - 64)))
right_wall_list_ver = []
for j in range(int(reso_y / 64) + 1):
    right_wall_list_ver.append(Characters.Scenery.wall(reso_x - 64, (j * 64)))
def right_room_scenery():
    screen.blit(Sprite_Animation.background_right, (0, 0))
    screen.blit(pillar1.image, (280, 90))
    screen.blit(pillar1.image, (280, 400))
    screen.blit(pillar1.image, (560, 90))
    screen.blit(pillar1.image, (560, 400))

    collision_course(pillar_list)
    collision_course(right_wall_list_hor)
    collision_course(right_wall_list_hor2)
    collision_course(right_wall_list_ver)


nothingness_list = []
for i in range(int(reso_x / 64) + 1):
    nothingness_list.append(Characters.Scenery.wall((i * 64), (150 - 64)))
for n in range(int(reso_y / 64) + 1):
    nothingness_list.append(Characters.Scenery.wall((150 - 64), (n * 64)))
for g in range(int(reso_y / 64) + 1):
    nothingness_list.append(Characters.Scenery.wall(850, (g * 64)))
def top_room_scenery():
    screen.blit(Sprite_Animation.background_top, (0, 0))

    collision_course(nothingness_list)


def top_room_denied():
    if pygame.Rect((toon.x_loc, toon.y_loc, toon.width + 32, toon.height + 32)).colliderect(stairs3.hitbox):
        if not toon.inventory.__contains__("Bootcamp") and not toon.inventory.__contains__("Make-up kit"):
            create_text(screen, mech_denied, textbox1, textbox1border, mech_denied2)
        elif not toon.inventory.__contains__("Bootcamp") and toon.inventory.__contains__("Make-up kit"):
            create_text(screen, mech_denied2, textbox1, textbox1border)
        elif toon.inventory.__contains__("Bootcamp") and not toon.inventory.__contains__("Make-up kit"):
            create_text(screen, mech_denied, textbox1, textbox1border)


def collision_course(scene_objects):
    for obj in Characters.gc.get_objects():
        if isinstance(obj, Characters.Scenery) and obj in scene_objects:
            if pygame.Rect(toon.hitbox).colliderect(obj.hitbox):
                if toon.movement_x != 0 and toon.movement_y == 0:
                    if toon.hitbox[0] < obj.hitbox[0]:
                        toon.x_loc -= toon.movement_x
                    elif toon.hitbox[0] > obj.hitbox[0]:
                        toon.x_loc += toon.movement_x
                elif toon.movement_y != 0:
                    if toon.hitbox[1] < obj.hitbox[1]:
                        toon.y_loc -= toon.movement_y
                    elif toon.hitbox[1] > obj.hitbox[1]:
                        toon.y_loc += toon.movement_y


def get_collide_stairs(stairs):
    if pygame.Rect(toon.hitbox).colliderect(stairs.hitbox):
        return True


def get_shot(person, shot_list, facing):
        for shot in shot_list:
            if pygame.Rect(person.hitbox).colliderect(shot.hitbox):
                if toon.inventory.__contains__("Bootcamp") and person != toon:
                    person.total_hp -= 2
                else:
                    person.total_hp -= 1
                shot_list.pop(shot_list.index(shot))
                if person.total_hp <= 0:
                    if person == mech:
                        mech.walkcount = 7
                        while person.walkcount < 30:
                            mech.walkcount += .2
                            top_room_scenery()
                            the_standard()
                            screen.blit(Sprite_Animation.mech_dead_sprite[round(person.walkcount) % 7], (person.x_loc,
                                                                                                         person.y_loc))
                            pygame.display.update()
                    person.alive = False
                    return person.alive


def get_close_sign():
    if not signs[0].observed:
        arrow = Sprite_Animation.the_sign.get_rect(topleft=(signs[0].x_loc, signs[0].y_loc - 64))
        screen.blit(Sprite_Animation.the_arrow, arrow)
    if pygame.Rect((toon.x_loc, toon.y_loc, toon.width + 32, toon.height + 32)).colliderect(signs[0].hitbox):
        create_text(screen, mission_statement, textbox3, textbox3border, mission_statement2)
        signs[0].observed = True


def get_close_treasure(treasure, item, sprite):
    whatt = pygame.time.Clock()
    upcount = 1
    box_opening = True
    if pygame.Rect(toon.hitbox).colliderect(treasure.hitbox):
        if keys[pygame.K_a]:
            treasure.opened = True
            if not toon.inventory.__contains__(item):
                if item == "Make-up kit":
                    while box_opening:
                        left_room_scenery()
                        the_standard()
                        create_treasure(treasure, (reso_x / 2.2), (reso_y / 6))
                        screen.blit(Sprite_Animation.gob_dead_sprite, (goblin.x_loc, goblin.y_loc))
                        create_text(screen, get_item1, textbox2, textbox2border)
                        screen.blit(sprite, ((treasure.x_loc + treasure.width / 3.5), treasure.y_loc - upcount))
                        if upcount <= 30:
                            upcount += 1
                        pygame.display.update()
                        whatt.tick(15)
                        for events in pygame.event.get():
                            if events.type == pygame.KEYDOWN:
                                box_opening = False
                elif item == "Bootcamp":
                    while box_opening:
                        right_room_scenery()
                        the_standard()
                        create_treasure(treasure,  (reso_x - 275), (reso_y - 600))
                        screen.blit(Sprite_Animation.nin_dead_sprite, (ninja.x_loc, ninja.y_loc))
                        create_text(screen, get_item2, textbox4, textbox4border)
                        pygame.display.update()
                        screen.blit(sprite, ((treasure.x_loc + treasure.width / 4), treasure.y_loc - upcount))
                        if upcount <= 30:
                            upcount += 1
                        pygame.display.update()
                        whatt.tick(15)
                        for events in pygame.event.get():
                            if events.type == pygame.KEYDOWN:
                                box_opening = False
                elif item == "Computer":
                    while box_opening:
                        top_room_scenery()
                        the_standard()
                        create_treasure(treasure,  mech.x_loc, mech.y_loc)
                        create_text(screen, get_item3, textbox1, textbox1border, get_item3_2)
                        pygame.display.update()
                        screen.blit(sprite, ((mech.x_loc + treasure.width / 4), mech.y_loc - upcount))
                        if upcount <= 30:
                            upcount += 1
                        pygame.display.update()
                        whatt.tick(15)
                        for events in pygame.event.get():
                            if events.type == pygame.KEYDOWN:
                                box_opening = False
            toon.inventory.append(item)


def check_change_room(stairs):
    if pygame.Rect(toon.hitbox).colliderect(stairs):
        return True


def get_leave_room(room):
    if room == "left":
        if toon.hitbox[0] + toon.width + 10 > reso_x:
            return True
    elif room == "right":
        if toon.hitbox[0] - 10 < 0:
            return True
    elif room == "top":
        if toon.hitbox[1] + toon.hitbox[3] + 10 > reso_y:
            return True


def create_treasure(treasure_box, x, y):
    collision_course([treasure_box])
    if not treasure_box.opened:
        screen.blit(Sprite_Animation.treasure_closed, (x, y))
    elif treasure_box.opened:
        screen.blit(Sprite_Animation.treasure_open, (x, y))


# ------------------ Start of MainGame While Loop ------------- #
while normal_run or left_room or right_room or top_room:

    if not toon.alive:
        normal_run = False
        left_room = False
        right_room = False
        top_room = False

    if toon.inventory.__contains__("Make-up kit"):
        toon.up_sprite = Sprite_Animation.say_up_sprite
        toon.down_sprite = Sprite_Animation.say_down_sprite
        toon.left_sprite = Sprite_Animation.say_left_sprite
        toon.right_sprite = Sprite_Animation.say_right_sprite

    for event in pygame.event.get():
        print(pygame.mouse.get_pos())

    if toon.walkcount >= 20:
        toon.walkcount = 3
    pygame.time.delay(35)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            normal_run = False
            left_room = False
            right_room = False
            top_room = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if len(beams_tracker) < 7:
            if toon.inventory.__contains__("Bootcamp"):
                beam_creation(Sprite_Animation.purp_beam_up, Sprite_Animation.purp_beam_down,
                              Sprite_Animation.purp_beam_left, Sprite_Animation.purp_beam_right)
            else:
                beam_creation(Sprite_Animation.blue_beam_up, Sprite_Animation.blue_beam_down,
                              Sprite_Animation.blue_beam_left, Sprite_Animation.blue_beam_right)
    for thing in beams_tracker:
        if toon.inventory.__contains__("Bootcamp"):
            beams_color(Sprite_Animation.purp_beam_up, Sprite_Animation.purp_beam_down, Sprite_Animation.purp_beam_left,
                        Sprite_Animation.purp_beam_right)
        else:
            beams_color(Sprite_Animation.blue_beam_up, Sprite_Animation.blue_beam_down, Sprite_Animation.blue_beam_left,
                        Sprite_Animation.blue_beam_right)

    for bullet in bullet_tracker:
        if 0 <= bullet.x <= reso_x and 0 <= bullet.y <= reso_y:
            if bullet.facing == "up":
                bullet.y -= bullet.velocity
            elif bullet.facing == "down":
                bullet.y += bullet.velocity
            elif bullet.facing == "right":
                bullet.x += bullet.velocity
            else:
                bullet.x -= bullet.velocity
        else:
            bullet_tracker.pop(bullet_tracker.index(bullet))

    for bullet_min in bullet_min_tracker:
        if 0 <= bullet_min.x <= reso_x and 0 <= bullet_min.y <= reso_y:
            if bullet_min.facing == "up":
                bullet_min.y -= bullet_min.velocity
            elif bullet_min.facing == "down":
                bullet_min.y += bullet_min.velocity
            elif bullet_min.facing == "right":
                bullet_min.x += bullet_min.velocity
            else:
                bullet_min.x -= bullet_min.velocity
        else:
            bullet_min_tracker.pop(bullet_min_tracker.index(bullet_min))

    if keys[pygame.K_UP] and toon.y_loc > 4:
        toon.movement_y = 20
        toon.movement_x = 0
        toon.y_loc -= toon.movement_y
        toon.walkcount += 1
        toon.up = True
        toon.left = False
        toon.right = False
        toon.down = False
    elif keys[pygame.K_DOWN] and toon.y_loc < (reso_y - 64):
        toon.movement_y = 20
        toon.movement_x = 0
        toon.y_loc += toon.movement_y
        toon.walkcount += 1
        toon.down = True
        toon.up = False
        toon.right = False
        toon.left = False
    elif keys[pygame.K_LEFT] and toon.x_loc > 4:
        toon.movement_x = 20
        toon.movement_y = 0
        toon.left = True
        toon.right = False
        toon.up = False
        toon.down = False
        toon.walkcount += 1
        toon.x_loc -= toon.movement_x
    elif keys[pygame.K_RIGHT] and toon.x_loc < (reso_x - 64):
        toon.movement_x = 20
        toon.movement_y = 0
        toon.right = True
        toon.left = False
        toon.down = False
        toon.up = False
        toon.walkcount += 1
        toon.x_loc += toon.movement_x

    if normal_run:
        for bullet in bullet_tracker:
            bullet_tracker.pop()
        the_standard_scenery()
        if toon.inventory.__contains__("Computer"):
            finished()
        the_standard()
        # the below can be changed into a nice DRY function
        if get_collide_stairs(stairs1):
            toon.x_loc = reso_x/1.3
            toon.y_loc = reso_y/2
            left_room = True
            normal_run = False
            if goblin.alive:
                enter_left = True
        elif get_collide_stairs(stairs2):
            toon.x_loc = 420
            toon.y_loc = 310
            right_room = True
            normal_run = False
            if ninja.alive:
                enter_right = True
        elif get_collide_stairs(stairs3):
            if goblin.alive or ninja.alive:
                top_room_denied()
            elif not goblin.alive and not ninja.alive:
                toon.y_loc = 600
                toon.x_loc = (reso_x / 2) - (toon.width / 2)
                top_room = True
                normal_run = False
                if mech.alive:
                    enter_top = True

    elif left_room:
        while enter_left:
            left_room_scenery()
            screen.blit(Sprite_Animation.gob_right_sprite[(int(goblin.walkcount % 3))], (goblin.x_loc, goblin.y_loc))
            the_standard()
            create_text(screen, goblin_chirp, textbox2, textbox2border, goblin_chirp2)
            pygame.display.update()
            pygame.time.delay(2000)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    enter_left = False
        left_room_scenery()
        the_standard()
        if goblin.alive:
            goblin_min1.which_direction()
            goblin_min2.which_direction()
            goblin_min1.move()
            goblin_min2.move()
            goblin_min1.move_blit(screen)
            goblin_min2.move_blit(screen)
            goblin_min1.shoot(goblin_min1, screen, bullet_min_tracker, (255, 255, 102), 4, toon)
            goblin_min2.shoot(goblin_min1, screen, bullet_min_tracker, (255, 255, 102), 4, toon)
            goblin.which_direction()
            goblin.move()
            goblin.move_blit(screen)
            goblin.shoot(goblin, screen, bullet_tracker, (128, 200, 0), 5, toon)
            get_shot(goblin, beams_tracker, goblin.direction)
            get_shot(toon, bullet_tracker, toon.up)
            get_shot(toon, bullet_min_tracker, toon.up)
        else:
            screen.blit(Sprite_Animation.gob_dead_sprite, (goblin.x_loc, goblin.y_loc))
            create_treasure(treasure_box1, (reso_x / 2.2), (reso_y / 6))
            get_close_treasure(treasure_box1, "Make-up kit", Sprite_Animation.garb)
        left_leave = get_leave_room("left")
        if left_leave:
            left_room = False
            normal_run = True
            toon.x_loc = stairs1.x_loc + stairs1.width + 10
            toon.y_loc = stairs1.y_loc

    elif right_room:
        while enter_right:
            right_room_scenery()
            screen.blit(Sprite_Animation.nin_left_sprite[(int(ninja.walkcount % 3))], (ninja.x_loc, ninja.y_loc))
            the_standard()
            create_text(screen, ninja_chirp, textbox4, textbox4border)
            pygame.display.update()
            pygame.time.delay(1000)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    enter_right = False
        right_room_scenery()
        the_standard()

        if ninja.alive:
            ninja.which_direction()
            ninja.teleport()
            ninja.move_blit(screen)
            ninja.shoot(ninja, screen, bullet_tracker, (224, 224, 224), 3, toon)
            get_shot(ninja, beams_tracker, ninja.direction)
            get_shot(toon, bullet_tracker, toon.up) # this 3rd parameter needs to be changed
        else:
            screen.blit(Sprite_Animation.nin_dead_sprite, (ninja.x_loc, ninja.y_loc))
            create_treasure(treasure_box2, (reso_x - 275), (reso_y - 600))
            get_close_treasure(treasure_box2, "Bootcamp", Sprite_Animation.pewpew)
        right_leave = get_leave_room("right")
        if right_leave:
            right_room = False
            normal_run = True
            toon.x_loc = stairs2.x_loc - toon.width - 10
            toon.y_loc = stairs2.y_loc

    elif top_room:
        if not toon.inventory.__contains__("Bootcamp") or not toon.inventory.__contains__("Make-up kit"):
            top_room_denied()
        else:
            while enter_top:
                top_room_scenery()
                screen.blit(Sprite_Animation.mech_down_sprite[(int(mech.walkcount % 3))], (mech.x_loc, mech.y_loc))
                the_standard()
                create_text(screen, mech_chirp, textbox1, textbox1border)
                pygame.display.update()
                pygame.time.delay(2000)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        enter_top = False
            top_room_scenery()
            the_standard()
            if mech.alive:
                get_shot(mech, beams_tracker, 1)
                get_shot(toon, bullet_tracker, 1)
                mech.move_blit(screen)
                mech.slide()
                mech.side_lazer(mech, screen, bullet_tracker, (224, 0, 224), 7, toon)
                mech.shoot(mech, screen, bullet_tracker, (224, 0, 224), 6, toon)
            else:
                create_treasure(treasure_box3, mech.x_loc, mech.y_loc)
                treasure_box3.hitbox = mech.hitbox
                get_close_treasure(treasure_box3, "Computer", Sprite_Animation.computer)
            top_leave = get_leave_room("top")
            if top_leave:
                top_room = False
                normal_run = True
                toon.x_loc = stairs3.x_loc
                toon.y_loc = stairs3.y_loc + stairs3.height + 10

    pygame.display.update()


dead_msg = intro_font.render("You Died", 1, (0, 0, 0))
dead_rect = dead_msg.get_rect()
dead_screen = True
while dead_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead_screen = False

    screen.blit(intro_background, (0, 0))
    screen.blit(dead_msg, (reso_x / 2 - (dead_rect[2] / 2), reso_y / 2 - (dead_rect[3] / 2)))

    pygame.display.update()

pygame.display.quit()
