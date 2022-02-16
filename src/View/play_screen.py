from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation
from Controller.utils.game_get_image import GetArtImage
from Controller.utils.game_logger import RkLogger
from src.GameConsts.game_consts import LEVEL_NEWBIE, GAME_LEVELS

Builder.load_file("View/play_screen.kv")


class PlayScreen(Screen):
    title = StringProperty()
    play_mood_str = ''

    def on_enter(self, **kwargs):
        self.logger = RkLogger.__call__().get_logger()
        Clock.schedule_once(self.get_art_work,1)

    # get the art work file
    # for testing use remote = false
    def get_art_work(self, dt):
        game_level = GAME_LEVELS[LEVEL_NEWBIE]
        artImage = GetArtImage(game_level)

        tiles_grid, title, long_title = artImage.get_art_image(self.play_mood_str)
        self.ids.image_on_button_1.texture = tiles_grid[15]['texture']
        #tiles_grid[0]
        self.logger.info("title "+title+ " long " + long_title)

class ImageButton(Image):
   def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

class DragButton(DragBehavior, Button):
    dragging = BooleanProperty(False)
    size = (200,200)
    original_pos = ListProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            #logger.info('on touch down')
            self.original_pos = self.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.opacity = 0.4
            self.dragging = True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        app = App.get_running_app()
        if self.dragging:
            self.opacity = 1
            self.dragging = False
            #if self.collide_widget(app.root.ids.remove_zone):
            #    self.parent.remove_widget(self)
            #else:
            #anim = Animation(pos=self.original_pos, duration=1)
            #anim.start(self)
        return super().on_touch_up(touch)
