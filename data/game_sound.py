import pygame as pg
from . import setup
from . import constants as c


class Music(object):

    def __init__(self):
        self.music_dict = setup.MUSIC

    def play_music(self):
        pg.mixer.music.load(self.music_dict['main_theme'])
        pg.mixer.music.play()

    def stop_music(self):
        pg.mixer.music.stop()
