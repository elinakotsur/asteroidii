import pygame
import math
import random


pygame.init()

sw = 800
sh = 800

bg = pygame.image.load('asteroidsPics/starbg.png')
alienImg = pygame.image.load('asteroidsPics/alienShip.png')
rocket = pygame.image.load('asteroidsPics/spaceRocket.png')
star = pygame.image.load('asteroidsPics/star.png')
asteroid50 = pygame.image.load('asteroidsPics/asteroid50.png')
asteroid100 = pygame.image.load('asteroidsPics/asteroid100.png')

pygame.display.set_caption("Asteroidiki")
win = pygame.display.set_mode((sw, sh))

gameover=False
lives = 5



class Player(object):
    def __init__(self):
        self.img=rocket
        self.w=self.img.get_width()
        self.h=self.img.get_height()
        self.x=sw//2
        self.y=sh//2
        
        self.angle=0
        self.rotate=pygame.transform.rotate(self.img,self.angle)
        self.rotateRect=self.rotate.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle+90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
        
    def draw(self, win):
        #win.blit(self.img, [self.x, self.y,self.w,self.h])
        win.blit(self.rotate, self.rotateRect)
        
    def turnLeft(self):
        self.angle += 5
        self.rotate = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotate.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turnRight(self):
        self.angle -= 5
        self.rotate = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotate.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotate = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotate.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)
        
    def moveBackward(self):
        self.x -= self.cosine * 6
        self.y += self.sine * 6
        self.rotate = pygame.transform.rotate(self.img, self.angle)
        self.rotateRect = self.rotate.get_rect()
        self.rotateRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)
        
    def tpLocation(self):
        if self.x > sw + 50:
            self.x =0
        elif self.x <0-self.w:
            self.x=sw
        elif self.y < -50:
            self.y=sh
        elif self.y >sh+50:
            self.y=0
class Asteroid(object):
    def __init__(self, rank):
        self.rank=rank
        if self.rank ==1:
            self.img=asteroid50
        elif self.rank ==2:
            self.img=asteroid100
        else:
            self.img=asteroid50
        self.w=50*rank
        self.h=50*rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x,self.y=self.ranPoint
        if self.x<sw//2:
            self.xdir=1
        else:
            self.xdir=-1
            
        if self.y<sh//2:
            self.ydir=1
        else:
            self.ydir=-1
            
        self.xv=self.xdir * random.randrange(1,3)
        self.yv=self.ydir * random.randrange(1,3)
        
    def draw(self,win):
        win.blit(self.img, (self.x,self.y))

class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.speed = 10
        
    def move(self):
        self.x += self.c * self.speed
        self.y -= self.s * self.speed
        
    def draw(self, win):
        pygame.draw.rect(win,(255,255,255),[self.x,self.y,self.w,self.h])




def gamewindow():
    win.blit(bg, (0, 0))
    font =pygame.font.SysFont('arial', 30)
    font2 =pygame.font.SysFont('arial', 70)
    livesText = font.render('lives: ' + str(lives),1,(255,255,255))
    gameoverText=font2.render('GAME OVER',1,(255,255,255))
    playAgainText=font.render('Press space to play again',1,(255,255,255))
    
    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    win.blit(livesText, (30,30))
    
    if gameover:
        win.blit(gameoverText, (230,300))
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2,sh//2-playAgainText.get_width()//2))    
    pygame.display.update()
    
    
    
player=Player()
playerBullets=[]
asteroids=[]
count=0
    
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    count+=1
    if not gameover:
        if count%50==0:
            ran = random.choice([1,1,1,1,2,2])
            asteroids.append(Asteroid(ran))
        
        player.tpLocation()
        for b in playerBullets:
            b.move()
               
        for a in asteroids:
            a.x+=a.xv
            a.y+=a.yv
            
            if (player.x>=a.x and player.x<= a.x+a.w) or (player.x + player.w>=a.x and player.x + player.w <=a.x + a.w):
                if (player.y >= a.y and player.y <= a.y + a.h) or (player.y+ player.h >= a.y and player.y + player.h <= a.y +a.h):
                    lives-=1
                    asteroids.pop(asteroids.index(a))
                    break
            
            
            for b in playerBullets:
                if b.x>=a.x and b.x <=a.x+a.w or b.x + b.w >=a.x and b.x + b.w <=a.x+a.w:
                    if b.y>=a.y and b.y <= a.y+a.h or b.y+b.h>=a.y and b.y+b.h<=a.y+a.h:
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        

                    
        if lives <=0:
            gameover=True
            
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
            
        if keys[pygame.K_RIGHT]:
            player.turnRight()
            
        if keys[pygame.K_UP]:
            player.moveForward()
            
        if keys[pygame.K_DOWN]:
            player.moveBackward()
            
        if keys[pygame.K_a]:
            player.turnLeft()
            
        if keys[pygame.K_d]:
            player.turnRight()
            
        if keys[pygame.K_w]:
            player.moveForward()
            
        if keys[pygame.K_s]:
            player.moveBackward()
            
            
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            run=False
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if not gameover:
                    playerBullets.append(Bullet())
                else:
                    gameover = False
                    lives = 5
                    asteroids.clear()
            
    gamewindow()        
pygame.quit()