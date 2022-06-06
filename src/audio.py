import pygame as pg
import constants


class AudioController:
    def __init__(self):
        self.isEnabled = constants.ENABLE_AUDIO
        self.isPaused = False

    def play_music(self, audio_path, loops=-1):
        if self.isEnabled:
            pg.mixer.music.load(audio_path)
            pg.mixer.music.play(loops)
        else:
            pass

    def play_sound(self, audio_path):
        if self.isEnabled:
            pg.mixer.Sound.play(audio_path)
            pg.mixer.music.stop()
        else:
            pass

    def pause_music(self):
        if self.isEnabled:
            if self.isPaused:
                pg.mixer.music.unpause()
            else:
                pg.mixer.music.pause()
        else:
            pass
