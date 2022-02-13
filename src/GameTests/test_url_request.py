import requests
import json
# TODO only for the text
import random
import datetime
from kivy.uix.image import Image as Kimage
from PIL import Image
from random import randrange
from src.GameConsts.game_consts import PORTRAIT, LANDSCAPE, MOOD_IDEAS
from Controller.utils import RkLogger

GLOBAL_TILE_SIZE = 512

# TODO add try catch for all interactions with the API
# explained https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python

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

class ArtTiles:
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



class ArtImage:

    def __init__(self, art_obj,width,height):
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

    # image is returned in tiles which need to be pasted into one image
    def get_bitmap_from_tiles(self):

        # choose the level by name z0 is the largest resolution z6 is the lowest resolution
        # look for z3 or z4
        image_levels = self.art_obj['levels']
        art_level = self.search_for_level(image_levels)
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

        grid_image = Kimage(canvas_image.resize((int(self.width), int(self.height)),Image.LANCZOS))
        mode = grid_image.mode
        size = grid_image.size
        data = grid_image.tobytes()
        now = datetime.datetime.now()
        image_to_save_file_name = "images/image_"+now.strftime("%Y-%m-%d-%H-%M-%S")+".RGB"
        grid_image.save (image_to_save_file_name)
        grid_image.show()
        # TODO py_image = pygame.image.fromstring(data, size, mode)
        # TODO return py_image, grid_image

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
HALF_SCREEN_WIDTH = SCREEN_WIDTH / 2

mood = random.choice(MOOD_IDEAS)


searchArtObj = SearchArt(mood)


art_dict = searchArtObj.get_image_list()

get_art_tiles = ArtTiles(art_dict)
title = art_dict['title']
long_title = art_dict['longTitle']
art_title_obj = get_art_tiles.get_art_image()
art_image = ArtImage(art_title_obj, SCREEN_WIDTH, SCREEN_HEIGHT)
art_image.get_bitmap_from_tiles()

