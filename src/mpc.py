import os
from mpd import MPDClient
from init import *

class mpc:

    def __init__(self):
        CON_ID = {'host':HOST, 'port':PORT}
        self.client = MPDClient()
        self.client.connect(**CON_ID)

        self.nowPlaying = self.client.currentsong()
        self.file = MUSIK_DIR + '/' + self.nowPlaying['file']
        self.getPlaylist()

    def __del__(self):
        self.client.disconnect()


    def update(self):
        tmp =  self.client.currentsong()
        self.nowPlaying = tmp
        self.file = MUSIK_DIR + '/' + self.nowPlaying['file']
        self.getPlaylist()

    def getCover(self):
        cover = os.path.dirname(self.file) + '/cover.jpg'
        if os.path.exists(cover):
            return cover
        else:
            return ''

    def next(self):
        self.client.next()

    def play(self):
        self.client.play()
        
    def getTime(self):
        return self.client.status()['time']
        

    def getPlaylist(self):
        tmp = self.client.playlistinfo()
        pl = []
        for i in tmp:
            pl.append(i['title']+' - '+i['artist'])
        self.playlist = pl
