import pygame,sys
from init import *
from pygame.locals import *


class PlayScreen:

    def __init__(self,mpc):
        self.myfont=pygame.font.Font(pygame.font.match_font('freeserif'),30)
        self.mpc = mpc
        self.screen = pygame.Surface(SCREEN_SIZE,0,32)

        self.makeBackground(SCREEN_SIZE)
        self.makeTitle(mpc.nowPlaying['artist'],mpc.nowPlaying['title'])
        self.makeCover(mpc.getCover())
        self.makeMirror(mpc.getCover())
        self.makeTimeline(500,20,(0,100))
        self.makePlaylist(self.mpc.playlist)
        self.blitScreen()
    
    def update(self):
        self.makeTitle(self.mpc.nowPlaying['artist'],self.mpc.nowPlaying['title'])
        self.makeCover(self.mpc.getCover())
        self.makeMirror(self.mpc.getCover())
            #Timeline
        tmp = self.mpc.getTime().split(':')
        self.makeTimeline(500,20,(int(tmp[0]),int(tmp[1])))
        self.makePlaylist(self.mpc.playlist)
        self.blitScreen()
        
    def blitScreen(self):
        self.screen.blit(self.bg,(0,0))            
        self.screen.blit(self.img,(50,50))
        self.screen.blit(self.mirror,(50+4,50+self.img.get_height()+4))

        x = int(self.screen.get_width()/3.0*2 - self.timeL.get_width() / 2)
        self.screen.blit(self.timeL,(x,250))

        # Math Foo
        x = int(self.screen.get_width()/3.0*2 - self.title.get_width() / 2)
        self.screen.blit(self.title,(x,100))

        self.screen.blit(self.playlist,(600,500))

    def makeCover(self,img):
        cover=pygame.image.load(img)
        cover=pygame.transform.scale(cover,THUMB_SIZE)
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
        self.img = ret

    def blendOut(self,img):
        height = img.get_height()
        grad = 255.0 / height
        for row in range(height):
            for col in range(img.get_width()):
                color = img.get_at((col,row))
                color.a = int(255-(grad*row))
                img.set_at((col,row), color)

#            sub.set_alpha(255-(grad*rows))

    def makeMirror(self,img):
        
        cover=pygame.image.load(img)
        cover=pygame.transform.scale(cover,THUMB_SIZE)
        cover=pygame.transform.flip(cover,False,True)

        tmp = pygame.Surface((cover.get_width(),cover.get_height()),pygame.SRCALPHA,32)
        tmp.blit(cover,(0,0))

        self.blendOut(tmp)
        
        # Math foo
        width=cover.get_height()+cover.get_width()
        ret = pygame.Surface((width,cover.get_height()),pygame.SRCALPHA,32)
        ret.set_alpha(0)
        ret.blit(tmp,(0,0))
    
        # Shift
        div = 0
        for line in range(ret.get_height()):
            tmp = range(ret.get_width())
            tmp.reverse()
            for i in tmp:
                ret.set_at((i+div,line),ret.get_at((i,line)))
                ret.set_at((i,line),pygame.Color(0,0,0,0))
            if (line%2)!=0:
                div+=1  
                   
        self.mirror=ret
         
    # Transparacy
    #tmpPic = pygame.Surface((width,cover.get_height()),pygame.SRCALPHA,32)
    #lines = 1
    #while lines < ret.get_height():
    #    for x in range(ret.get_width()):
    #        if (x%(cover.get_height()-lines))==0:
    #            tmpPic.set_at((x,lines),ret.get_at((x,lines)))
    #    lines += 1
    #ret = tmpPic
        

    def makeTimeline(self,width,height,t):
        time=self.myfont.render(str(t[0])+':'+str(t[1]),2,white)
        pro = int(int(t[0])/float(int(t[1]))*100)
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

        tmp = pygame.Surface((max(ret.get_width(),time.get_width()),ret.get_height()+time.get_height()+10),pygame.SRCALPHA,32)
        x = tmp.get_width()/2-time.get_width()/2
        tmp.blit(time,(x,0))
        x = tmp.get_width()/2-ret.get_width()/2
        tmp.blit(ret,(x,time.get_height()+10))

        self.timeL = tmp

    def makeTitle(self,title,artist):
        title=self.myfont.render("Title: "+title,2,white)
        artist=self.myfont.render("Artist: "+artist,2,white)
        width=0
        if title.get_width()>artist.get_width():
            width = title.get_width()
        else:
            width = artist.get_width()
    
        ret = pygame.Surface((width,artist.get_height()+title.get_height()+5),pygame.SRCALPHA,32)
    
        x = 0
        if ret.get_width()> title.get_width():
            x =  (ret.get_width() - title.get_width())/2
        ret.blit(title,(x,0))
        x=0
        if ret.get_width()> artist.get_width():
            x =  (ret.get_width() - title.get_width())/2
        ret.blit(artist,(x,title.get_height()+5))
        self.title = ret         

    def makeBackground(self,(width,height)):
        ret = pygame.Surface((width,height),0,32)       
    # Math foo
        dif = ((darkblue[0])/float(width),(darkblue[1])/float(width),(darkblue[2])/float(width))
        color=(0,0,0)
        x = 0
        while x < width:
            pygame.draw.line(ret,color,(x,0),(x,height))
            color = (color[0]+dif[0],color[1]+dif[1],color[2]+dif[2])
            x+=1
        self.bg = ret


    def makePlaylist(self,pl):
        i = 0
        maxi = min(30,len(pl))
        tmp=[]
        while i < maxi:
            tmp.append(self.myfont.render(pl[i],2,white))
            i += 1
        width = []
        height = []
        for i in tmp:
            width.append(i.get_width())
            height.append(i.get_height())
        width = max(width)
        height = sum(height)

        tmpS = pygame.Surface((width,height),pygame.SRCALPHA,32)

        i = 0
        y = 0
        while i < len(tmp):
            tmpS.blit(tmp[i],(0,y))
            y += tmp[i].get_height()
            i += 1
        self.playlist = tmpS
