from mpd import MPDClient
from init import *

class mpc:

    def __init__(self):
        CON_ID = {'host':HOST, 'port':PORT}
        self.client = MPDClient()
        self.client.connect(**CON_ID)

        self.nowPlaying = self.client.currentsong()
    
    def __del__(self):
        self.client.disconnect()


    def update(self):
        self.nowPlaying = self.client.currentsong()

