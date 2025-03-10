import os
import sys
import pygame
import sqlite3
import random
from itertools import product

DIS_SIZE = (1000, 600)
FPS = 50
pygame.init()
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



class objects():

    def __init__(self, name):
        # example
        name = "knife"
        place = "kitchen"
        pos = (0, 0)
        invent = False

    def take(self):
        print()
        # todo

    def use(self):
        print()
        # todo

    def combine(self):
        print()
        # todo


class interactions():

    def __init__(self, name):
        # example
        name = "box"
        place = "under bed"
        pos = (0, 0)
        done = False
        need_object = "knife"


class room():

    def __init__(self, name):
        # example
        name = ""


# Цикл игры
def game():
    return

def give_text(place, num):
    return ["Хоши", "недавно мне пришо поручение от гильдии. говрят в одной квартире одинокий мужчина умер от сердечного приступа, но соседи продолжают слышать его шаги."]


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
    print(num)
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


run_game = True
intro_flag = -1
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if -1 <= intro_flag <= 10:
                intro_flag += 1
            else:
                intro_flag = -2
    if intro_flag >= 0:
        intro(intro_flag)
    else:
        screen.fill((192, 192, 192))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
