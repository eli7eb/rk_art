from functools import partial

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation
from Controller.utils.game_get_image import GetArtImage
from Controller.utils.game_shuffle_utils import ShuffleUtils
from Controller.utils.game_logger import RkLogger
from src.GameConsts.game_consts import LEVEL_NEWBIE, LEVEL_NEWBIE, LEVEL_BEGIN, GAME_LEVELS, FADE_DURATION
from src.GameConsts.game_consts import TILE_IN_SHUFFLE_BOARD, TILE_ON_BOARD_TEST, TILE_INVISIBLE, TILE_IN_TILES_BANK
from src.GameConsts.game_consts import TILE_IN_PLACE, TILE_DRAGGED, TILE_DROPPED
Builder.load_file("View/play_screen.kv")


class PlayScreen(Screen):
    title = ''
    long_title = ''
    play_mood_str = ''
    game_level = 0
    tiles_grid = []
    grid_layout = ObjectProperty()
    logger = RkLogger.__call__().get_logger()

    def on_enter(self, **kwargs):
        Clock.schedule_once(self.init_play_screen,1)

    def init_play_screen(self, dt):
        self.get_art_work()
        self.init_grid_layout()
        self.shuffle_utils = ShuffleUtils(self.game_level)
        self.reshuffle()
        self.init_board_based_on_level()
        self.set_titles_and_links()
        #self.ids.shuffle_button.disabled = True

    # TODO level controls:
    # do I show the image before and then hide it
    # do I leave a half transpaent image
    # do I have a number of tiles on the board how many per level
    def init_board_based_on_level(self):
        if self.game_level.bg_trans == True:
            self.init_grid_before_play()
        pass

    # based on level decide if to show , half transparent or blank it out
    # leave tiles as hints
    def init_grid_before_play(self):
        # show the image than disappear

        for i in self.tiles_grid:
            k_image = i['k_image']
            k_image.size = (self.ids.image_button_1.width,self.ids.image_button_1.height)
            k_image.size_hint = (None, None)
            #k_image.allow_stretch = True
            #image.pos = (x_pos, y_pos)
            self.grid_layout.add_widget(k_image)
        Clock.schedule_once(self.hide_bg, self.game_level.show_time_seconds)


    # remove widgets from layout
    def hide_bg(self, dt):
        if self.game_level.id == LEVEL_BEGIN or self.game_level.id == LEVEL_NEWBIE:
            fade_opacity = 0.3
        else:
            fade_opacity = 0
            Clock.schedule_once(self.remove_layout_children, FADE_DURATION + 1)

        if self.grid_layout.children:
            for child in [child for child in self.grid_layout.children]:
                anim = Animation(opacity=fade_opacity, duration=FADE_DURATION)
                anim.start(child)

    def remove_layout_children(self):
        if self.grid_layout.children:
            for child in [child for child in self.grid_layout.children]:
                self.grid_layout.remove_widget(child)

    # create the grid layout for the tiles
    def init_grid_layout(self):
        self.grid_layout = GridLayout(cols=self.game_level.tiles_hor,rows=self.game_level.tiles_ver,spacing=2)

        self.ids.game_canvas.add_widget(self.grid_layout)
        self.grid_layout.x = self.ids.game_canvas.x+50
        self.grid_layout.y = self.ids.game_canvas.y+self.ids.game_canvas.height - 150

    # get the art work file
    # for testing use remote = false
    def get_art_work(self):
        self.game_level = GAME_LEVELS[LEVEL_NEWBIE]
        artImage = GetArtImage(self.game_level,(self.ids.game_canvas.width,self.ids.game_canvas.height))

        self.bg_trans = self.game_level.bg_trans  # Boolean how the initial bg is shown, True for all half tran, False only a few
        self.show_time_seconds = self.game_level.show_time_seconds  # if not 0 show for number of seconds else leave all the time
        self.tiles_on_board_number = self.game_level.tiles_on_board_number

        self.tiles_grid, title, long_title = artImage.get_art_image(self.play_mood_str)
        self.title = title
        self.long_title = long_title

        #tiles_grid[0]
        self.logger.info("title "+title+ " long " + long_title)

    # TODO style the labels
    def set_titles_and_links(self):
        self.ids.art_info_label.text = ''
        self.ids.game_score_label.text = ''
        self.ids.game_stats_label.text = ''
        self.ids.art_info_label.text = self.title


    def reshuffle(self):

        shuffle_arr = self.shuffle_utils.get_random_set_from_list()
        self.ids.image_button_1.texture = self.tiles_grid[shuffle_arr[0]]['texture']
        self.ids.image_button_2.texture = self.tiles_grid[shuffle_arr[1]]['texture']
        self.ids.image_button_3.texture = self.tiles_grid[shuffle_arr[2]]['texture']
        self.ids.image_button_4.texture = self.tiles_grid[shuffle_arr[3]]['texture']


class DragImage(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DragImage, self).__init__(**kwargs)
        self.drag_timeout = 10000000
        self.drag_distance = 0
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    dragging = BooleanProperty(False)
    # size = (200,200)
    original_pos = ListProperty()

    def on_pos(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_size(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('on touch down')
            self.original_pos = self.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.opacity = 0.4
            self.dragging = True
            print('on touch move')
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        app = App.get_running_app()
        if self.dragging:
            self.opacity = 1
            self.dragging = False
            print('on touch up')
            #if self.collide_widget(app.root.ids.remove_zone):
            #    self.parent.remove_widget(self)
            #else:
            #anim = Animation(pos=self.original_pos, duration=1)
            #anim.start(self)
        return super().on_touch_up(touch)
