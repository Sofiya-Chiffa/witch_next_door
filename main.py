import os
import sys
import pygame
import sqlite3
import random
from itertools import product

t_s = 2
DIS_SIZE = (1920 / t_s + 100, 1080 / t_s)
FPS = 50
pygame.init()
conn = sqlite3.connect("witches.sqlite3")
screen = pygame.display.set_mode(DIS_SIZE)
pygame.display.set_caption('Witch Next Door')
clock = pygame.time.Clock()


# Загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def give_text(place, num):
    return ["Хоши", "недавно мне пришло поручение от гильдии. говрят в одной квартире одинокий мужчина умер от сердечного приступа, но соседи продолжают слышать его шаги."]


# Рисование текста для заставки игры
def draw_text(text, color, place, size):
    lines = [""]
    i = 0
    for word in text.split():
        if len(word) + i > 70:
            i = 0
            lines.append("")
        i += len(word) + 1
        lines[-1] += word + " "
    for line in lines:
        font = pygame.font.SysFont('comicsansms', size)
        string_rendered = font.render(line, True, color)
        text_rect = string_rendered.get_rect()
        text_rect.top = place[1]
        place[1] += 20
        text_rect.x = place[0]
        screen.blit(string_rendered, text_rect)



def dialogue(text):
    pygame.draw.rect(screen, 'grey', (130, DIS_SIZE[1] - 150, DIS_SIZE[0] - 260, 100))
    draw_text(text[0], 'black', [130, DIS_SIZE[1] - 185], 30)
    draw_text(text[1], 'black', [145, DIS_SIZE[1] - 145], 20)


# Заставка игры и её начало
def intro(num):
    intro_text = give_text("intro", num)
    if 0 <= num <= 2:
        im = 'двор.png'
    elif 3 <= num <= 6:
        im = 'лестница.png'
    elif 7 <= num:
        im = 'лестница.png'
    fon = pygame.transform.scale(load_image(im), (DIS_SIZE[0], DIS_SIZE[1]))
    screen.blit(fon, (0, 0))
    if 7 <= num:
        neir = pygame.transform.scale(load_image('сосед.png'), (DIS_SIZE[0], DIS_SIZE[1]))
        screen.blit(neir, (0, 0))
    dialogue(intro_text)
    return


# Меню игры
def menu():
    print("this is menu")
    print("1 start")
    print("2 exit")
    a = int(input())
    if a == 1:
        return True
    else:
        return False

class Inventory:
    def __init__(self):
        self.width = 100
        self.height = 1080 // t_s
        self.board = [0] * 6
        self.left = 1920 // t_s
        self.top = 0
        self.cs = self.height // 6
        self.objs = []
        self.active_obj = ""

    def render(self, surface):
        for i in range(6):
            pygame.draw.rect(surface, 'grey', (self.left, self.top + self.cs*i, 100, self.cs))
            pygame.draw.rect(surface, 'white', (self.left, self.top + self.cs*i, 100, self.cs), 6)
            if len(self.objs) > i:
                image = pygame.transform.scale(load_image(self.objs[i] + ".png"), (
                (conn.cursor().execute("""SELECT x1 FROM obj WHERE name = ?""", (self.objs[i],)).fetchall()[0][0]) / t_s / 1.5,
                (conn.cursor().execute("""SELECT y1 FROM obj WHERE name = ?""", (self.objs[i],)).fetchall()[0][0]) / t_s / 1.5))
                screen.blit(image, (self.left + 15, self.top + self.cs*i))
                if self.board[i] == 1:
                    draw_surface = pygame.Surface(DIS_SIZE, pygame.SRCALPHA)
                    pygame.draw.rect(draw_surface, (255, 255, 100, 100), (self.left, self.top + self.cs * i, 100, self.cs))
                    screen.blit(draw_surface, (0, 0))

    def add_obj(self, name):
        self.objs.append(name)

    def del_obj(self, name):
        pass

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos) is not None:
            if self.board[self.get_cell(mouse_pos)] == 0:
                self.board = [0] * 6
                if len(self.objs) > self.get_cell(mouse_pos):
                    self.active_obj = self.objs[self.get_cell(mouse_pos)]
            else:
                self.active_obj = ""
            self.board[self.get_cell(mouse_pos)] = (self.board[self.get_cell(mouse_pos)] + 1) % 2

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + self.width and \
                self.top <= mouse_pos[1] <= self.top + self.height:
            y = (mouse_pos[1] - self.top) // self.cs
            return y
        else:
            return None

    def get_active_obj(self):
        return self.active_obj


codes = []
class Code():

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.num = 0
        print(0)
        draw_text(str(self.num), 'black', [self.x, self.y], 50)

    def update(self):
        draw_text(str(self.num), 'black', [self.x, self.y], 50)

    def get_click(self, mouse_pos):
        if self.x - 20 <= mouse_pos[0] <= self.x + 70 and \
                self.y - 20 <= mouse_pos[1] <= self.y + 70:
            self.num = (self.num + 1) % 10
            return True

    def get_num(self):
        return self.num

class Keys(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__(all_keys)
        self.name = name
        self.active = conn.cursor().execute("""SELECT key FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]
        if self.active == 0:
            self.kill()
        self.key = 0
        self.image = pygame.transform.scale(load_image(name + ".png"), ((conn.cursor().execute("""SELECT x1 FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s,
                                                                        (conn.cursor().execute("""SELECT y1 FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = ((conn.cursor().execute("""SELECT pos1_x FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s,
                                    (conn.cursor().execute("""SELECT pos1_y FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s)

    def get_click(self, mouse_pos, inv):
        print(self.name)
        conn.cursor().execute("""UPDATE obj SET key = ? WHERE name = ?""", (0, self.name,))
        inv.add_obj(self.name)
        self.kill()

    def get_name(self):
        return self.name

    def delete(self):
        self.kill()

    def update(self, dt):
        self.image = pygame.transform.scale(load_image(self.name + ".png"), (
        (conn.cursor().execute("""SELECT x1 FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s,
        (conn.cursor().execute("""SELECT y1 FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (
        (conn.cursor().execute("""SELECT pos1_x FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s,
        (conn.cursor().execute("""SELECT pos1_y FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s)


class Objects(pygame.sprite.Sprite):

    def __init__(self, name, active):
        super().__init__(all_obj)
        self.name = name
        self.active = active
        self.key = 0
        self.image = pygame.transform.scale(load_image(name + ".png"), ((conn.cursor().execute("""SELECT x1 FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s,
                                                                        (conn.cursor().execute("""SELECT y1 FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = ((conn.cursor().execute("""SELECT pos1_x FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s,
                                    (conn.cursor().execute("""SELECT pos1_y FROM obj WHERE name = ?""", (name,)).fetchall()[0][0])/t_s)




    def get_click(self, mouse_pos):
        print(self.name)
        if (conn.cursor().execute("""SELECT key FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0] == 1):
            self.active = (self.active + 1) % 2

    def get_name(self):
        return self.name

    def update(self, dt):
        if self.active == 0:

            if self.name == "шкафприхожая":
                for obj in all_obj:
                    if obj.get_name() == "ключ1":
                        obj.delete()

            self.image = pygame.transform.scale(load_image(self.name + ".png"), (
            (conn.cursor().execute("""SELECT x1 FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s,
            (conn.cursor().execute("""SELECT y1 FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = (
            (conn.cursor().execute("""SELECT pos1_x FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s,
            (conn.cursor().execute("""SELECT pos1_y FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s)
        elif self.active == 1:

            if self.name == "дверь":
                if codes:
                    for code in codes:
                        code.update()
                else:
                    for i in range(4):
                        codes.append(Code(340 + (i * 88), 260))

            if self.name == "шкафприхожая":
                k = True
                for key in all_keys:
                    if key.get_name() == "ключ1":
                        k = False
                if k:
                    Keys("ключ1")

            self.image = pygame.transform.scale(load_image(self.name + "2.png"), (
                (conn.cursor().execute("""SELECT x2 FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s,
                (conn.cursor().execute("""SELECT y2 FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][0]) / t_s))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = (
                (conn.cursor().execute("""SELECT pos2_x FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][
                    0]) / t_s,
                (conn.cursor().execute("""SELECT pos2_y FROM obj WHERE name = ?""", (self.name,)).fetchall()[0][
                    0]) / t_s)

    def delete(self):
        self.kill()


def apartment(state, time):
    if state == 0:
        im = 'прихожая.png'
    elif state == 1:
        im = 'гостиная.png'
    elif state == 2:
        im = 'дверьтуалет.png'
    if state == 0 and time == 0:
        Objects("шкафприхожая", 0)
    elif state == 1 and time == 0:
        Objects("шкаф", 0)
        Objects("шкатулка_подоконник", 0)
        Objects("шкатулка_шкаф", 0)
    elif state == 2 and time == 0:
        Objects("дверь", 0)
    fon = pygame.transform.scale(load_image(im), (DIS_SIZE[0] - 100, DIS_SIZE[1]))
    screen.blit(fon, (0, 0))



run_game = True
state_room = 0
flag = 0
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flag += 1
    if 0 <= flag <= 10:
        intro(flag)
    else:
        break
    pygame.display.flip()

run_game = True
all_obj = pygame.sprite.Group()
all_keys = pygame.sprite.Group()
t_room = 0
main_door = False
inventory = Inventory()
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            inventory.get_click(event.pos)
            c = 1
            for code in codes:
                if code.get_click(event.pos):
                    c = 0
            for key in all_keys:
                if key.rect.collidepoint(event.pos):
                    key.get_click(event.pos, inventory)
                    c = 0
            if c:
                for obj in all_obj:
                    if obj.rect.collidepoint(event.pos):
                        obj.get_click(event.pos)
            flag += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for o in all_obj:
                    o.kill()
                t_room = 0
                state_room = (state_room + 1) % 3
            if event.key == pygame.K_RIGHT:
                for o in all_obj:
                    o.kill()
                t_room = 0
                state_room = state_room - 1
                if state_room < 0:
                    state_room = 2
    if codes:
        for i in range(4):
            main_door = True
            if codes[i].get_num() != [8 , 9, 5, 5][i]:
                main_door = False
                break
    if main_door:
        print("good job")
        for o in all_obj:
            o.kill()
    dt = clock.tick()
    apartment(state_room, t_room)
    all_obj.draw(screen)
    all_obj.update(dt)
    all_keys.draw(screen)
    all_keys.update(dt)
    inventory.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
    t_room += 1
pygame.quit()
