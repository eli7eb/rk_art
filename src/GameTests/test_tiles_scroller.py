import requests
import json
import math
# TODO only for the text
import random
import datetime
from kivy import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.image import Image as KImage, AsyncImage as KAsyncImage
from kivy.core.image import Image as CoreImage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from random import randrange
from src.GameConsts.game_consts import PORTRAIT, LANDSCAPE, MOOD_IDEAS, TILE_INVISIBLE
from src.GameUtils.game_logger import RkLogger
from src.GameElements.game_tile import Tile

GLOBAL_TILE_SIZE = 512

# TODO add try catch for all interactions with the API
# explained https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python


kv = Builder.load_string('''
#:kivy 1.11.0

<RootLayout>:
    WindowManager:
        ImageScreen:
        
            name:"ImageScreen"
            id:image_screen
            Image:
                id:img
                pos_hint:{"left":1, 'bottom':1}
                size_hint:1,1
                allow_stretch:True    
            BoxLayout:
                orientation:'vertical'
                id:layout_id
                Button:
                    id:show_image
                    text:"show image"
                    size_hint:0.15,0.15
                    on_release: app.show_image()
  
''')

# count number of spaces in grid is calculated as number of tiles horizontally -1
# count number of spaces in grid is calculated as number of tiles vertically -1
# function to validate the cropsize
# values are first 2 are row,col on the left side
# last 2 are bottom right on the right side
# TODO if error exit game ? or find new image ?
# TODO rethink it mean while return OK
def validate_crop_size(image, tile_size):
    #w = abs(image.width - tile_size)
    #h = abs(image.height - tile_size)
    #if w > 5 or h > 5:
    #    return False
    return True

# from box and image size get the x y coodinates in the grid
def getXYCoordinatesFromBox(box, tile_size):
    logger = RkLogger.__call__().get_logger()
    logger.info("box {}".format(box))

    # find the middle point
    x = box[0] + tile_size/2
    y = box[1] + tile_size/2
    x_index = int(x/tile_size)
    y_index = int(y/tile_size)
    return  x_index, y_index


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

    def getImageList(self):
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
            art_portrait_list = self.get_matched_list(json_obj['artObjects'],PORTRAIT)
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

    def getArtImage(self):
        rk_api_token = 'aTcoXoCh'
        rk_url_postfix = '&q='
        # get random of list
        # String prefix = "https://www.rijksmuseum.nl/api/en/collection/"+params[0].get_object_number()+"/tiles?format=json&key=";
        format_json = 'json'
        object_number = self.art_dict.get("objectNumber","")
        rk_type_paint = 'painting'
        rk_type_material = 'canvas'
        rk_url_call_end = '\''
        rk_api_url_base_prefix = 'https://www.rijksmuseum.nl/api/en/collection/'+object_number+'/tiles'+'?key=' + rk_api_token
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(rk_api_token)}

        query_params = { "format": format_json }

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
            self.logger.error ('error '+response.status_code + ' '+response.text)



class GetArtImage:

    def __init__(self, art_obj,width,height):
        self.currentState = None
        self.art_obj = art_obj
        self.width = width
        self.height = height
        self.logger = RkLogger.__call__().get_logger()


    # TODO add assert for error here
    def searchForLevel(self, image_levels):
        for l in image_levels:
            if l['name'] == 'z3':
                return l
        return image_levels[0]

    # the squares need to be exactly the size to fit in the array
    # we need to decide which comes first the image size or the tiles size
    # on a beginner level I have 4 - 6
    # then 5 - 7
    # then 7 - 9
    def fit_squares(self, image, number_tiles):
        logger = RkLogger.__call__().get_logger()
        logger.info("fit_squares")
        im = image
        num_tiles = number_tiles
        width = im.width
        height = im.height

        px = math.ceil(math.sqrt(num_tiles * width / height))
        if math.floor(px * height / width) * px < num_tiles:
            sx = height / math.ceil(px * height / width)
        else:
            sx = width / px
        py = math.ceil(math.sqrt(num_tiles * height / width))
        if math.floor(py * width / height) * py < num_tiles:
            sy = width / math.ceil((width * py / height))
        else:
            sy = height / py
        # TODO get the number of cols and rows by deviding the width/size and height/size
        # return all as tuple
        size = int(max(sx, sy))
        num_cols = int(width / size)
        num_rows = int(height / size)
        return size, num_cols, num_rows




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
    def crop_image_to_array(self, tile_tuple, image):
        im = image
        # TODO 4 tiles across depends on level
        width = int(im.width)
        height = int(im.height)
        chopsize = tile_tuple[0]

        num_cols = tile_tuple[1]
        num_rows = tile_tuple[2]

        tile_matrix = [[1] * num_cols for n in range(num_rows)]
        counter = 0
        x_counter = 0
        y_counter = 0
        for x0 in range(0, width, chopsize):
            for y0 in range(0, height, chopsize):
                print("x0 "+str(x0) + " y0 "+str(y0))

                box = (x0, y0,
                x0 + chopsize if x0 + chopsize < width else width - 1,
                y0 + chopsize if y0 + chopsize < height else height - 1)
                print_str = "counter {} box {}"
                print(print_str.format(counter,box))

                cropped = im.crop(box)
                if validate_crop_size(cropped, chopsize):
                    mode = cropped.mode
                    size = cropped.size
                    data = cropped.tobytes()
                    # cropped_image = pygame.image.fromstring(data, size, mode)

                    # position is set in game view when the tile is displayed
                    counter += 1
                    # coords = getXYCoordinatesFromBox(box, chopsize)
                    # print("coords {}".format(str(coords)))
                    # TODO fix this
                    py_image_t = cropped.copy()  # self.get_tile_blurred(py_image)
                    coords = (x_counter,y_counter)
                    pil_tile = Tile(cropped, chopsize, (x0, y0), coords, TILE_INVISIBLE)
                    try:
                        tile_matrix[x_counter][y_counter] = pil_tile
                    except IndexError as error:
                        print("Index error %s" + error)
                    except Exception as exception:
                        print("Exception %s"+exception)
                    # img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg', ''), x0, y0))
                else:
                    print('error on crop')
                y_counter+=1
                # PIL for transparant copy
            x_counter+=1


        return tile_matrix

    # image is returned in tiles which need to be pasted into one image
    def getBitmapFromTiles(self):

        # choose the level by name z0 is the largest resolution z6 is the lowest resolution
        # look for z3 or z4
        image_levels = self.art_obj['levels']
        art_level = self.searchForLevel(image_levels)
        # PIL image
        canvas_image = Image.new('RGB', (art_level['width'], art_level['height']), color=(255,255,255))
        # final_image = image.resize((width, height))

        for i in art_level['tiles']:
            tmp_image = Image.open(requests.get(i['url'], stream=True).raw)
            tmp_x = i['x'] * GLOBAL_TILE_SIZE
            tmp_y = i['y'] * GLOBAL_TILE_SIZE
            #print('image w h')
            #print(final_image.width)
            #print(final_image.height)
            canvas_image.paste(tmp_image,(tmp_x,tmp_y))



        # I have the final image: 2 considerations:
        # need to resize and keep aspect ratio - i have a maximum of size I can use
        # the width is setting the size of the resizing
        # the height sets the number and size of each tile
        # need to resize so that tile size is going to fit

        grid_image = canvas_image.resize((int(self.width), int(self.height)),Image.LANCZOS)
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
  "beginner" : {
    "width" : 440,
    "height" : 660,
    "num_tiles": 24
    },
  "intermid" : {
    "width" : 450,
    "height" : 630,
    "num_tiles": 35
  },
   "inter_1": {
     "width": 420,
     "height": 630,
     "num_tiles": 63
   },
   "inter_2": {
      "width": 450,
      "height": 630,
      "num_tiles": 35
   },
    "master" : {
    "width" : 450,
    "height" : 650,
    "num_tiles": 117
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

    def show_image(self):


        mood = random.choice(MOOD_IDEAS)
        img_src = StringProperty()
        searchArtObj = SearchArt(mood)

        art_dict = searchArtObj.getImageList()

        get_art_tiles = GetArtTiles(art_dict)
        title = art_dict['title']
        long_title = art_dict['longTitle']
        print('title ' + title + ' long title '+long_title)
        print ('getArtTiles')
        art_title_obj = get_art_tiles.getArtImage()

        print('getArtTiles done')
        print('getArtImage')
        art_image = GetArtImage(art_title_obj, SCREEN_WIDTH, SCREEN_HEIGHT)
        print('getBitMapFromTiles')
        canvas_img = art_image.getBitmapFromTiles()

        # get tile size
        print('fitSquares')
        tile_tuple = art_image.fit_squares(canvas_img,self.level['num_tiles'])
        tile_size = tile_tuple[0]
        num_cols = tile_tuple[1]
        num_rows = tile_tuple[2]
        locations_matrix = [[1] * num_cols for n in range(num_rows)]
        print('crop_image_to_array')
        tiles_grid = art_image.crop_image_to_array(tile_tuple, canvas_img)
        # data = CoreImage(bytes_data,ext="RGB").texture
        now = datetime.datetime.now()
        image_to_save_file_name = "images/image_" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".RGB"
        canvas_img.save(image_to_save_file_name)
        self.root.ids.img.source = image_to_save_file_name
        # draw grid for the tiles
        # draw_grid_lines(self)

        # crop to tiles

        # show tiles in random order in a horizontal box layout




    def build(self):
        return RootLayout()


if __name__ == "__main__":
    TilesApp().run()
