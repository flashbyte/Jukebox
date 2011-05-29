import pygame,sys
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode((800,600),0,32)


yel=(247,244,55)
red=(157,4,6)
darkblue=(10,24,146)

def makeCover(img):
    cover=pygame.image.load(img).convert()
    ret = pygame.Surface((cover.get_width()+8,cover.get_height()+8),0,32)
    #Math foo
    steps=ret.get_height()
    dif=((yel[0]-red[0])/float(steps),(yel[1]-red[1])/float(steps),(yel[2]-red[2])/float(steps))
    #Make Box

    color=red
    i = 0
    while i < steps:
        color=(color[0]+dif[0],color[1]+dif[1],color[2]+dif[2])
        color=(color[0]%255,color[1]%255,color[2]%255)
        pygame.draw.line(ret,color,(0,i),(ret.get_width(),i))
        i+=1

    #Draw Image
    ret.blit(cover,(4,4))            
    return ret

def makeTimeline(width,height,pro):
    ret = pygame.Surface((width,height),0,32)
    #Math foo
    steps=width
    dif=((yel[0]-red[0])/float(steps),(yel[1]-red[1])/float(steps),(yel[2]-red[2])/float(steps))
    # Make outer box
    color=red
    i = 0
    while i < steps:
        color=(color[0]+dif[0],color[1]+dif[1],color[2]+dif[2])
        color=(color[0]%255,color[1]%255,color[2]%255)
        pygame.draw.line(ret,color,(i,0),(i,height))
        i+=1
    # Make inner box
    color=red
    i = width-3
    while i > 1:
        color=(color[0]+dif[0],color[1]+dif[1],color[2]+dif[2])
        color=(color[0]%255,color[1]%255,color[2]%255)
        pygame.draw.line(ret,color,(i,2),(i,height-3))
        i-=1

    pro=float(pro)/100
    pygame.draw.rect(ret,darkblue,Rect((4,4),((width-8)*pro,height-8)))

    return ret

img = makeCover("byp.jpg")
timeL = makeTimeline(500,20,76)
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(img,(50,50))
    screen.blit(timeL,(200,500))
    pygame.display.update()
