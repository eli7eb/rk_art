import requests
import json
# TODO only for the text
import random
import datetime
from kivy import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image as Kimage
from random import randrange
from src.GameConsts.game_consts import PORTRAIT, LANDSCAPE, MOOD_IDEAS
from Controller.utils import RkLogger
from PIL import Image

GLOBAL_TILE_SIZE = 512

# TODO add try catch for all interactions with the API
# explained https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python


kv = Builder.load_string('''
#:kivy 1.11.0

<RootLayout>:
    WindowManager:
        ImageScreen:
            BoxLayout:
                orientation:'vertical'
                name:"ImageScreen"
                id:image_screen
                Image:
                    id:img
                    pos_hint:{"left":1, 'bottom':1}
                    size_hint:1,1
                    allow_stretch:True
                BoxLayout:
                    orientation:'horizontal'
                    size_hint:1.,0.15
                    Button:
                        id:show_image
                        text:"show image"
                        on_release: app.show_image()
                        size_hint:0.2,1.0
                    BoxLayout:
                        orientation:'horizontal'
                        id:tiles_grid_id
                        MoveableImage:
                            id:tile_image
                            pos_hint:{"left":1, 'bottom':1}
                            size_hint:1,1
                            allow_stretch:True
                
                    
''')


class MoveableImage(Kimage, DragBehavior):
    __metaclass__ = DragBehavior


class SearchArt:

    # from the list of web images returned choose only the portrait or landscape ones
    def get_matched_list(self, art_list, mode):
        returned_list = []
        for item in art_list:
            print('item {}'.format(item['title']))
            # print('w {} h {}'.format(str(item['webImage']['width']), str(item['webImage']['height'])))
            if (item['webImage'] == None):
                continue
            if mode == PORTRAIT and (item['webImage']['height'] > item['webImage']['width']):
                returned_list.append(item)
            elif mode == LANDSCAPE and (item['webImage']['width'] > item['webImage']['height']):
                returned_list.append(item)
        return returned_list

    def get_image_list(self):
        rk_api_token = 'aTcoXoCh'
        rk_url_postfix = '&q='

        format_json = 'json'
        rk_type_paint = 'painting'
        rk_type_material = 'canvas'
        rk_url_call_end = '\''
        rk_api_url_base_prefix = 'https://www.rijksmuseum.nl/api/en/collection?key=' + rk_api_token
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(rk_api_token)}

        query_params = {"q": self.search_value, "format": format_json, "object_type": rk_type_paint,
                        "material": rk_type_material}
        try:
            response = requests.request("GET", rk_api_url_base_prefix, headers=headers, params=query_params)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as c_err:
            self.logger.error(c_err)
            raise SystemExit(c_err)
        except requests.exceptions.HTTPError as err:  # This is the correct syntax
            self.logger.error(err)
            raise SystemExit(err)

        if response.status_code == 200:
            print('success')
            print(response.text)

            json_obj = json.loads(response.content.decode('utf-8'))
            print('json objects {}'.format(json_obj['artObjects']))
            art_list = json_obj['artObjects']
            art_portrait_list = self.get_matched_list(json_obj['artObjects'], PORTRAIT)
            art_index = 0
            if len(art_portrait_list) > 0:
                art_index = randrange(len(art_portrait_list))
                return art_portrait_list[art_index]
            # here I return a blank list so take what you have
            return art_list[0]
        else:
            # TODO errormsgto user to check network etc
            print('error ' + response.status_code)

    def __init__(self, mood_str):
        self.currentState = None
        self.search_value = mood_str
        self.logger = RkLogger.__call__().get_logger()


class GetArtTiles:
    print('get the one')

    def __init__(self, art_dict):
        self.currentState = None
        self.art_dict = art_dict
        self.logger = RkLogger.__call__().get_logger()

    def get_art_image(self):
        rk_api_token = 'aTcoXoCh'
        rk_url_postfix = '&q='
        # get random of list
        # String prefix = "https://www.rijksmuseum.nl/api/en/collection/"+params[0].get_object_number()+"/tiles?format=json&key=";
        format_json = 'json'
        object_number = self.art_dict.get("objectNumber", "")
        rk_type_paint = 'painting'
        rk_type_material = 'canvas'
        rk_url_call_end = '\''
        rk_api_url_base_prefix = 'https://www.rijksmuseum.nl/api/en/collection/' + object_number + '/tiles' + '?key=' + rk_api_token
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(rk_api_token)}

        query_params = {"format": format_json}

        try:
            response = requests.request("GET", rk_api_url_base_prefix, headers=headers, params=query_params)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as c_err:
            self.logger.error(c_err)
            raise SystemExit(c_err)
        except requests.exceptions.HTTPError as err:
            self.logger.error(err)
            raise SystemExit(err)
        if response.status_code == 200:
            self.logger.info('success')
            self.logger.info(response.text)
            json_obj = json.loads(response.content.decode('utf-8'))
            self.logger.info(json_obj)
            return (json_obj)
        else:
            self.logger.error('error ' + response.status_code + ' ' + response.text)


class GetArtImage:

    def __init__(self, art_obj, width, height):
        self.currentState = None
        self.art_obj = art_obj
        self.width = width
        self.height = height
        self.logger = RkLogger.__call__().get_logger()

    # TODO add assert for error here
    def search_for_level(self, image_levels):
        for l in image_levels:
            if l['name'] == 'z3':
                return l
        return image_levels[0]


    # crop function
    # Set the cropping area with box=(left, upper, right, lower).
    # an_array = [[1, 2], [3, 4]]
    # rows = len(an_array) Find row and column length.
    # columns = len(an_array[0])
    # total_length = rows * columns. Compute total length.
    # print(total_length)
    # cut the image to tiles and return them as two dimentianal array
    # im_crop = im.crop((100, 75, 300, 150))
    # calculate # tiles : regular and level specific
    # calculate per col and per line
    # validate that I am not out side the image size
    # calculate where I am on the grid by dividing the box to the grid
    # create the tile object with image and image_transparent
    # Note that the matrix is "y" address major, in other words, the "y index" comes before the "x index".
    def crop_image_to_array(self, tile_size, num_cols, num_rows, image, title):
        im = image
        width = int(im.width)
        height = int(im.height)
        cols = num_cols
        rows = num_rows
        file_title = title
        index_row = 0
        index_colum = 0
        left = 0
        top = 0
        right = width / cols
        bottom = 0
        tile_matrix = [[1] * num_rows for n in range(num_cols)]

        while right <= width:

            bottom = height / rows
            top = 0
            while top < height:
                print(f"h : {height}, w : {width}, left : {left},top : {top},right : {right}, bottom   :  {bottom}")
                crop_img = im.crop((left, top, right, bottom))
                try:
                    tile_matrix[index_colum][index_row] = crop_img
                except IndexError as error:
                    print("Index error %s" + error)
                except Exception as exception:
                    print("Exception %s" + exception)
                now = datetime.datetime.now()
                crop_img.save("images/art_row_" + str(index_row) + "_col_" +str(index_colum) + "_" + file_title + now.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg")
                top = bottom
                index_row += 1
                bottom += height / rows

            index_colum += 1
            index_row = 0
            left = right
            right += width / cols

        return tile_matrix

    # image is returned in tiles which need to be pasted into one image
    def get_bitmap_from_tiles(self):

        # choose the level by name z0 is the largest resolution z6 is the lowest resolution
        # look for z3 or z4
        image_levels = self.art_obj['levels']
        art_level = self.search_for_level(image_levels)
        # PIL image
        canvas_image = Image.new('RGB', (art_level['width'], art_level['height']), color=(255, 255, 255))
        # final_image = image.resize((width, height))

        for i in art_level['tiles']:
            tmp_image = Image.open(requests.get(i['url'], stream=True).raw)
            tmp_x = i['x'] * GLOBAL_TILE_SIZE
            tmp_y = i['y'] * GLOBAL_TILE_SIZE
            # print('image w h')
            # print(final_image.width)
            # print(final_image.height)
            canvas_image.paste(tmp_image, (tmp_x, tmp_y))

        # I have the final image: 2 considerations:
        # need to resize and keep aspect ratio - i have a maximum of size I can use
        # the width is setting the size of the resizing
        # the height sets the number and size of each tile
        # need to resize so that tile size is going to fit
        # TILES can be 100 150 200 and 50 so I need to resize accordigly
        grid_image = canvas_image.resize((int(self.width), int(self.height)), Image.LANCZOS)
        mode = grid_image.mode
        size = grid_image.size
        # bytes_data = grid_image.tobytes()

        return grid_image
        # grid_image.show()
        # TODO py_image = pygame.image.fromstring(data, size, mode)
        # TODO return py_image, grid_image


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2

levels = {
    "beginner": {
        "width": 600,
        "height": 800,
        "cols": 3,
        "rows": 4,
        "tile_size": 200
    },
    "beginner_1": {
        "width": 600,
        "height": 800,
        "cols": 6,
        "rows": 8,
        "tile_size": 100
    },
    "intermid": {
        "width": 600,
        "height": 800,
        "cols": 12,
        "rows": 16,
        "tile_size": 50
    }
}

Config.set('graphics', 'multisamples', '0')


class RootLayout(FloatLayout):
    pass


class ImageScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class DrawGrid:
    # 2 dimentional array of lines

    pass


class TilesApp(App):
    img_file = ObjectProperty()
    img_src = StringProperty()
    level = levels['beginner']

    # show the tiles to drag in the hor boxlayout
    def show_tiles(self, img):
        self.root.ids.tile_image.source = img

    # show the loaded entire image in the screen
    # for test purposes
    def show_image(self):
        mood = random.choice(MOOD_IDEAS)
        img_src = StringProperty()
        searchArtObj = SearchArt(mood)

        art_dict = searchArtObj.get_image_list()

        get_art_tiles = GetArtTiles(art_dict)
        title = art_dict['title']
        long_title = art_dict['longTitle']
        print('title ' + title + ' long title ' + long_title)
        print('getArtTiles')
        art_title_obj = get_art_tiles.get_art_image()

        print('getArtTiles done')
        print('get_art_image_by_object_number')
        art_image = GetArtImage(art_title_obj, SCREEN_WIDTH, SCREEN_HEIGHT)
        print('getBitMapFromTiles')
        canvas_img = art_image.get_bitmap_from_tiles()

        tile_size = self.level['tile_size']
        num_cols = self.level['cols']
        num_rows = self.level['rows']
        # locations_matrix = [[1] * num_cols for n in range(num_rows)]
        print('crop_image_to_array')
        tiles_grid = art_image.crop_image_to_array(tile_size, num_cols, num_rows, canvas_img, title)
        # data = CoreImage(bytes_data,ext="RGB").texture
        now = datetime.datetime.now()
        image_to_save_file_name = "images/image_" + title + now.strftime("%Y-%m-%d-%H-%M-%S") + ".RGB"
        canvas_img.save(image_to_save_file_name)
        self.root.ids.img.source = image_to_save_file_name
        # draw grid for the tiles
        self.show_tiles(tiles_grid[0][0])
        # draw_grid_lines(self)

        # crop to tiles

        # show tiles in random order in a horizontal box layout

    def build(self):
        return RootLayout()


if __name__ == "__main__":
    TilesApp().run()
