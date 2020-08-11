import pygame
import random
pygame.init()
width = 200
height = 400
boxes = []
level = 1
LV = level
spd = 1
clock = pygame.time.Clock()
font = pygame.font.SysFont('Ariel', 20, True)
class cube:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = 5
        self.negx = 1
        self.negy = 1
        self.vx = random.randint(1, 2)
        self.vy = 5
        self.color = color
        self.frictx = 1
    def drawbox(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
    def manual(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x >= 0:
            self.frictx = -1
            self.x -= self.v
        elif keys[pygame.K_RIGHT] and self.x <= width - self.w:
            self.frictx = 1
            self.x += self.v
        else:
            self.frictx = 0
    def auto(self):
        self.x += self.vx * self.negx * spd
        self.y -= self.vy * self.negy * spd
    def bounce(self):
        b = (self.x, self.x + self.w, self.y, self.y + self.h)
        for box in boxes:
            for i in range(0, 1):
                for j in range(2, 3):
                    if b[i] > box.x and b[i] < box.x + box.w:
                        if b[j] > box.y and b[j] < box.y + box.h:
                            boxes.pop(boxes.index(box))
                            self.negy *= -1
        if self.x <= 0 or self.x >= width - self.w:
            self.negx *= -1
            self.x += self.vx * self.negx
        if self.y <= 0:
            self.negy *= -1
def barriers(width, height):
    boxw, boxh = 50, 10
    bx, by = 0, 0
    for l in range(level):
        for i in range(width//boxw):
            boxes.append(cube(bx, by, boxw, boxh, (0, 255, 0)))
            bx += boxw
        bx = 0
        by += boxh * 1.1
def drawbarriers(surface):
    for box in boxes:
        box.drawbox(surface)
def ballset(surface):
    bx, by = 5, random.randint(15 * level, height * 0.75)
    ball = cube(bx, by, 10, 10, (0, 255, 0))
    return ball
def friction():
    global player, ball
    if ball.negx == player.frictx:
        ball.vx += 0.2
    elif player.frictx == 0:
        pass
    else:
        ball.vx -= 0.2
def main():
    global level, spd, LV, win, ball, player
    win = pygame.display.set_mode((width, height))
    ball = ballset(win)
    reset = True
    score = 0
    run = True
    complete = False
    player = cube(width * 0.5, height * 0.9, 50, 20, (255, 0, 0))
    while run:
        if reset:
            barriers(width, height)
            length = len(boxes)
            reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        while not(complete):
            clock.tick(30)
            win.fill((0, 0, 0))
            text = font.render('Score: ' + str(score), False, (255, 255, 255))
            text2 = font.render('Lv: ' + str(LV), False, (255, 255, 255))
            #score
            if len(boxes) < length:
                score += 10
                length = len(boxes)
            win.blit(text2, (0, height - 20))
            win.blit(text, (width * 0.5 - 30, height - 20))
            player.drawbox(win)
            player.manual()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    complete = True
            drawbarriers(win)
            ball.drawbox(win)
            ball.auto()
            ball.bounce()
            #bounce off player
            if ball.x + ball.w >= player.x and ball.x +ball.w <= player.x + player.w:
                if ball.y  >= player.y and ball.y  <= player.y + player.h:
                    ball.negy *= -1
                    friction()
            if ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w:
                if ball.y + ball.h >= player.y and ball.y + ball.h <= player.y + player.h:
                    ball.negy *= -1
                    friction()
            if ball.x >= player.x and ball.x <= player.x + player.w:
                if ball.y + ball.h >= player.y and ball.y + ball.h <= player.y + player.h:
                    ball.negy *= -1
                    friction()
            if ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w:
                if ball.y + ball.h >= player.y and ball.y + ball.h <= player.y + player.h:
                    ball.negy *= -1
                    friction()
            #fail
            if ball.y + ball.h >= height:
                complete = True
            #level passed
            if len(boxes) <= 0:
                pygame.time.delay(10)
                complete = True
            pygame.display.update()
        if complete:
            if len(boxes) == 0:
                if level <= 8:
                    level += 1
                LV += 1
                spd *= 1.1
                ball.y += 15 * level
                complete = False
                reset = True
            else:
                win.fill((0, 0, 0))
                text3 = font.render('You died :(', False, (255, 255, 255))
                win.blit(text3, (width//2, height//2))
                pygame.display.update()
    pygame.quit()
main()