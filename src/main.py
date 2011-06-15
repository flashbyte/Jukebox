import pygame,sys
import mpc
from init import *
from pygame.locals import *
import PlayScreen

def init():
    pygame.init()
    pygame.font.init

    pygame.time.set_timer(pygame.USEREVENT, 500)


# -------------- Main -------------

init()
mpc = mpc.mpc()
playScreen = PlayScreen.PlayScreen(mpc)
screen = None
if FULLSCREEN==True:
    screen=pygame.display.set_mode(SCREEN_SIZE,pygame.FULLSCREEN,32)
else:
    screen=pygame.display.set_mode(SCREEN_SIZE,0,32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            elif event.key == K_n:
                mpc.next()
            elif event.key == K_f:
                pygame.display.toggle_fullscreen()
            elif event.key == K_p:
                mpc.play()
        elif event.type == USEREVENT:
            mpc.update()
            playScreen.update()

    screen.blit(playScreen.screen,(0,0))
    pygame.display.update()
