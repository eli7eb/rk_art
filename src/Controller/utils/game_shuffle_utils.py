import random
from Controller.utils.game_logger import RkLogger

class ShuffleUtils():

    def __init__(self, game_level):
        self.game_level = game_level
        self.tiles_on_shuffle_board_number = game_level.tiles_on_shuffle_board_number
        self.list_length = game_level.tiles_hor*game_level.tiles_ver
        self.logger = RkLogger.__call__().get_logger()

    # get x random indexes from a list of y
    # i e 4, 16 will return 1 5 7 12
    def get_random_set_from_list(self):

        return_list = random.sample(range(self.list_length), self.tiles_on_shuffle_board_number)
        random.shuffle(return_list)
        return return_list

    # get x random indexes from a list of y excluding what is in list z
    # i e 4, 16 , {2,4,5,6} will return 1 2 7 12
    def get_random_set_from_list_excluding_list(self, num_random, list_length, list_exist):
        pass