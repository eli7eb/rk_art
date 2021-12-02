from src.game_consts.game_constants import *

class Level:
    def __init__(self, id, name, bg_trans, tiles_hor,tiles_ver,tiles_on_board_number,show_bg_then_fade,
                 show_correct_position, count_steps):
        self.id = id
        self.name = name
        self.bg_trans = bg_trans  # Boolean how the initial bg is shown, True for all half tran, False only a few
        self.tiles_hor = tiles_hor
        self.tiles_ver = tiles_ver
        self.tiles_on_board_number = tiles_on_board_number
        self.show_bg_then_fade = show_bg_then_fade
        self.show_correct_position = show_correct_position # Boolean while drag show correct position
        self.count_steps = count_steps  # number of steps to solve - challenge mode