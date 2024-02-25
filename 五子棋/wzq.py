"""
这里主要实现了人人对战的功能，单独运行play函数也可以直接开始人人对战
"""
import pygame
import numpy as np
from pygame.locals import QUIT, KEYDOWN
import datetime

a = datetime.datetime.now()
a = str(a)
time = a[:10] + '_' + a[11:13] + '.' + a[14:16]
screen_color = [205, 186, 150]
line_color = black = [0, 0, 0]
red = [255, 0, 0]
blue = [0, 0, 255, 0]
white = [255, 255, 255]
grey = [150, 150, 150]
green = pygame.Color("green")
beenpos = []
tim = 0


###############
def setpos(x, y):
    boo = True
    for I in range(27, 670, 44):
        for J in range(27, 670, 44):
            L1 = I - 22
            L2 = I + 22
            R1 = J - 22
            R2 = J + 22
            if L1 <= x <= L2 and R1 <= y <= R2:
                return I, J, boo
    boo = False
    return x, y, boo


def check(x, y, over_pos):
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return False
    return True


def win(over_pos):
    mp = np.zeros([15, 15], dtype=int)
    for val in over_pos:
        x = int((val[0][0] - 27) / 44)
        y = int((val[0][1] - 27) / 44)
        if val[1] == white:
            mp[x][y] = 2
        else:
            mp[x][y] = 1
    for i in range(15):
        pos1 = []
        pos2 = []
        for j in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]
    for j in range(15):
        pos1 = []
        pos2 = []
        for i in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i + k >= 15 or j + k >= 15:
                    break
                if mp[i + k][j + k] == 1:
                    pos1.append([i + k, j + k])
                else:
                    pos1 = []
                if mp[i + k][j + k] == 2:
                    pos2.append([i + k, j + k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i + k >= 15 or j - k < 0:
                    break
                if mp[i + k][j - k] == 1:
                    pos1.append([i + k, j - k])
                else:
                    pos1 = []
                if mp[i + k][j - k] == 2:
                    pos2.append([i + k, j - k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    return [False, []]


# 这部分是基于教程修改的
##################

def play():
    kaishi = 0
    Time = 0
    boo1 = True
    pygame.init()
    screen = pygame.display.set_mode([670, 670])
    pygame.display.set_caption('五子棋')
    while True:
        res = win(beenpos)
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                fname = "History/" + str(time) + ".png"
                pygame.image.save(screen, fname)
                print("file {} has been saved".format(fname))
                pygame.quit()
                beenpos.clear()
                return res[0]
        screen.fill(screen_color)
        ###################
        for i in range(27, 670, 44):
            if i == 27 or i == 670 - 27:
                pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 4)
            else:
                pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 2)
            if i == 27 or i == 670 - 27:
                pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 4)
            else:
                pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 2)
            for ii in range(4, 13, 3):
                for j in range(4, 13, 3):
                    if ii == 7 or j == 7:
                        pass
                    else:
                        pygame.draw.circle(screen, line_color, [27 + 44 * ii, 27 + 44 * j], 6, 0)
        # 这部分是基于教程修改的
        ####################
        pygame.draw.circle(screen, line_color, [27 + 44 * 7, 27 + 44 * 7], 8, 0)
        x, y = pygame.mouse.get_pos()
        x, y, boo = setpos(x, y)
        if boo1 is True:
            if boo is True:
                pygame.draw.rect(screen, [0, 229, 238], [x - 22, y - 22, 44, 44], 2, 1)
            else:
                pygame.draw.rect(screen, [255, 0, 0], [x - 22, y - 22, 44, 44], 2, 1)
        keys_pressed = pygame.mouse.get_pressed()
        for val in beenpos:
            pygame.draw.circle(screen, val[1], val[0], 20, 0)
        if res[0] is not False:
            for pos in res[1]:
                pygame.draw.rect(screen, [238, 48, 167], [pos[0] * 44 + 27 - 22, pos[1] * 44 + 27 - 22, 44, 44], 2, 1)
            pygame.display.update()
            boo1 = False
            ft = pygame.font.Font("C:/Windows/Fonts/LCALLIG.TTF", 80)
            if res[0] == 1:
                text = ft.render("BLACK WIN", True, [255, 50, 30])
            else:
                text = ft.render("WHITE WIN", True, [255, 50, 30])
            screen.blit(text, (60, 0))
            pygame.display.update()
            continue
        if keys_pressed[0] and Time == 0 and kaishi > 10:
            boo = True
            if check(x, y, beenpos):
                if len(beenpos) % 2 == 0:
                    pygame.draw.circle(screen, black, [27 + 44 * x, 27 + 44 * y], 18, 0)
                    beenpos.append([[x, y], black])
                elif len(beenpos) % 2 == 1:
                    pygame.draw.circle(screen, white, [27 + 44 * x, 27 + 44 * y], 18, 0)
                    beenpos.append([[x, y], white])
        if boo:
            Time += 1
        if Time % 20 == 0:
            Time = 0
        kaishi += 1
        pygame.display.update()
