from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from Controller.utils.game_get_image import GetArtImage
from Controller.utils.game_logger import RkLogger
from src.GameConsts.game_consts import LEVEL_NEWBIE, GAME_LEVELS

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
        game_level = GAME_LEVELS[LEVEL_NEWBIE]
        artImage = GetArtImage(game_level)

        art_image_texture, title, long_title = artImage.get_art_image(self.play_mood_str)
        self.logger.info("title "+title+ " long " + long_title)