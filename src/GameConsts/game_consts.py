from src.game_level import Level


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
# frame around the display edges
OUTER_BORDER_SIZE = 20
# space between grid dashboard and grid scroller
INNER_BORDER_SIZE = 4

VIEW_STATE_SPLASH = 0
VIEW_STATE_MENU = 1
VIEW_STATE_LOADING = 2
VIEW_STATE_GAME_A = 3
VIEW_STATE_GAME_B = 4
VIEW_STATE_OPTIONS = 5
VIEW_STATE_QUITTING = 6
VIEW_STATE_QUIT = 7

HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT / 2

# all level parameters are a calculation of LEVEL
# log levels to write into the log file:
# all print statement will go there
# log has ID = level message and params
LOG_LEVEL = 1
SCREEN_SPACER_SIZE = 5
FADE_DURATION = 5
# status of the tile in the game
# when all in place - game is finished
TILE_IN_SHUFFLE_BOARD = 0
TILE_ON_BOARD_TEST = 1
TILE_INVISIBLE = 2
TILE_IN_TILES_BANK = 3
TILE_IN_PLACE = 4
TILE_DRAGGED = 5
TILE_DROPPED = 6

LEVEL_NEWBIE = 1
LEVEL_BEGIN = 2
LEVEL_INTER = 3
LEVEL_MASTER = 5
LEVEL_CHAMPION = 6
LEVEL_NOVICE = 7
local_art = { \
    'vermeer': {'file':"local_images_assets/milkmaid.png",'title':'Johannes Vermeer, The Milkmaid, c. 1660','long_title':'Johannes Vermeer, The Milkmaid, c. 1660'},
    'van-goch': {'file':"local_images_assets/portrait.jpg",'title':'Vincent van Gogh, Self-portrait, 1887.','long_title':'Vincent van Gogh, Self-portrait, 1887.'}
    }

GAME_LEVELS = { \
    LEVEL_NEWBIE: Level(LEVEL_NEWBIE, 'newbie', True,      5, 3, 4,  4, 4, True,0),
    LEVEL_BEGIN: Level(LEVEL_BEGIN, 'begin', False,        5, 3, 4,  4, 4, True,0),
    LEVEL_INTER: Level(LEVEL_INTER, 'inter', True,         2, 6, 8,  3, 6, True,0),
    LEVEL_MASTER: Level(LEVEL_MASTER, 'master', True,      2, 6, 8,  2, 6, True,0),
    LEVEL_CHAMPION: Level(LEVEL_CHAMPION, 'champion', True,1, 12,16, 2, 8, True,0),
    LEVEL_NOVICE: Level(LEVEL_NOVICE, 'novice', True,      1, 12,16, 1, 8, True,0),
}

PORTRAIT = 'portrait'
LANDSCAPE = 'landscape'

MOOD_IDEAS = ['lion', 'glass', 'book', 'money', 'chair', 'garden', 'flower', 'tree', 'snow', 'carpet', 'wall', 'art', 'spring', 'summer', 'winter', 'cat', 'dog', 'farm', 'king', 'prince', 'happy', 'castle', 'bread', 'flower', 'war', 'library']