from src.GameScreens.game_level import Level


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
TILE_ON_BOARD_TEST = 0
TILE_INVISIBLE = 1
TILE_IN_TILES_BANK = 2
TILE_IN_PLACE = 3
TILE_DRAGGED = 4
TILE_DROPPED = 5

LEVEL_NEWBIE = 1
LEVEL_BEGIN = 2
LEVEL_INTER = 3
LEVEL_MASTER = 5
LEVEL_CHAMPION = 6
LEVEL_NOVICE = 7
local_art = { \
    'vermeer': {'file':"../assets/milkmaid.png",'title':'Johannes Vermeer, The Milkmaid, c. 1660','long_title':'Johannes Vermeer, The Milkmaid, c. 1660'},
    'van-goch': {'file':"../assets/portrait.jpg",'title':'Vincent van Gogh, Self-portrait, 1887.','long_title':'Vincent van Gogh, Self-portrait, 1887.'}
    }

levels = { \
    LEVEL_NEWBIE: Level(LEVEL_NEWBIE, 'newbie', True,4,6,True,0,True,0),
    LEVEL_BEGIN: Level(LEVEL_BEGIN, 'begin', True,4,6,True,0,True,0),
    LEVEL_INTER: Level(LEVEL_INTER, 'inter', True,5,7,True,0,True,0),
    LEVEL_MASTER: Level(LEVEL_MASTER, 'master', True,6,8, True,0,True,0),
    LEVEL_CHAMPION: Level(LEVEL_CHAMPION, 'champion', True,6,8, True,0,True,0),
    LEVEL_NOVICE: Level(LEVEL_NOVICE, 'novice', True,7,9, True,0,True,0)
}

PORTRAIT = 'portrait'
LANDSCAPE = 'landscape'

MOOD_IDEAS = ['lion', 'glass', 'book', 'money', 'chair', 'garden', 'flower', 'tree', 'snow', 'carpet', 'wall', 'art', 'spring', 'summer', 'winter', 'cat', 'dog', 'farm', 'king', 'prince', 'happy', 'castle', 'bread', 'flower', 'war', 'library']