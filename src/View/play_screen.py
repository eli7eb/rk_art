import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from src.GameUtils.rk_http_requests import GetArtImage
from src.GameUtils.game_logger import RkLogger

Builder.load_file("View/play_screen.kv")


class PlayScreen(Screen):
    title = StringProperty()
    play_mood_str = ''

    def on_enter(self, **kwargs):
        self.logger = RkLogger.__call__().get_logger()
        Clock.schedule_once(self.get_art_work,5)

    # get the art work file
    # for testing use remote = false
    def get_art_work(self, dt):
        artImage = GetArtImage()
        art_image = artImage.get_art_image(self.play_mood_str)
        self.logger.info("")