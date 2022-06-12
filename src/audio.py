import pygame as pg
import constants


class AudioController:
    def __init__(self):
        self.isEnabled = constants.ENABLE_AUDIO
        self.isPaused = False
        self.pieces_click_sound = pg.mixer.Sound(constants.PIECES_CLICK)
        self.fit_pieces_sound = pg.mixer.Sound(constants.FIT_PIECES)
        self.wrong_fit_pieces_sound = pg.mixer.Sound(constants.WRONG_FIT_PIECES)
        self.game_over = pg.mixer.Sound(constants.GAME_OVER)

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

    def play_pickup_pieces(self):
        if self.isEnabled:
            pg.mixer.Sound.play(self.pieces_click_sound)
        else:
            pass

    def play_fit_pieces(self):
        if self.isEnabled:
            pg.mixer.Sound.play(self.fit_pieces_sound)
        else:
            pass

    def play_wrong_fit_pieces(self):
        if self.isEnabled:
            pg.mixer.Sound.play(self.wrong_fit_pieces_sound)
        else:
            pass

    def play_game_over(self):
        if self.isEnabled:
            pg.mixer.Sound.play(self.game_over)
        else:
            pass
