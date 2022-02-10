import requests
import json
# TODO only for the text
import random
import datetime
import io
from pathlib import Path

from kivy import Config
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.image import Image as KImage, AsyncImage as KAsyncImage
from kivy.core.image import Image as CoreImage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from random import randrange
from src.GameConsts.game_consts import PORTRAIT, LANDSCAPE, MOOD_IDEAS
from src.GameUtils.game_logger import RkLogger

GLOBAL_TILE_SIZE = 512

# TODO add try catch for all interactions with the API
# explained https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python
file_ext = 'jpg'
file_mode = 'RGB'
local_art = { \
    'vermeer': {'file':"../assets/milkmaid.png",'title':'Johannes Vermeer, The Milkmaid, c. 1660','long_title':'Johannes Vermeer, The Milkmaid, c. 1660'},
    'van-goch': {'file':"../assets/portrait.jpg",'title':'Vincent van Gogh, Self-portrait, 1887.','long_title':'Vincent van Gogh, Self-portrait, 1887.'}
    }
kv = Builder.load_string('''
#:kivy 1.11.0
<Picture>:
    # each time a picture is created, the image can delay the loading
    # as soon as the image is loaded, ensure that the center is changed
    # to the center of the screen.
    on_size: self.center = win.Window.center
    size: image.size
    size_hint: None, None

    Image:
        id: image
        source: root.source

        # create initial image to be 400 pixels width
        size: 400, 400 / self.image_ratio

        # add shadow background
        canvas.before:
        Color:
            rgba: 1,1,1,1
        BorderImage:
            source: 'shadow32.png'
            border: (36,36,36,36)
            size:(self.width+72, self.height+72)
            pos: (-36,-36)
            
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
                    on_release:
                        app.show_image()

  
''')




class ArtInfo:

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
    def get_art_level(self, image_levels):
        for l in image_levels:
            if l['name'] == 'z3':
                return l
        return image_levels[0]

    # I have image from RK
    # I have the level which sets the number of tiles
    # I have the window which limit
    # so find the desired image size which will suit all these
    # TODO
    def calculate_desired_image_size(w,h):
        return 0

    # image is returned in tiles which need to be pasted into one image
    def get_bitmap_from_tiles(self):

        # choose the level by name z0 is the largest resolution z6 is the lowest resolution
        # look for z3 or z4
        image_levels = self.art_obj['levels']
        art_level = self.get_art_level(image_levels)
        # PIL image
        canvas_image = Image.new(file_mode, (art_level['width'], art_level['height']), color=(255,255,255))
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
        # need to resize so that tile size is going to fit  !!!!!!!!!!
        # need to resize and keep aspect ratio - i have a maximum of size I can use
        # the width is setting the size of the resizing
        # the height sets the number and size of each tile

        image_size = self.calculate_desired_image_size((canvas_image.size))
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

Config.set('graphics', 'multisamples', '0')

class RootLayout(FloatLayout):
    pass

class ImageScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)

# ImageApp
# gets the image by mood hint from the RK api
# steps are:
# get the available options by the mood string
# choose appropriate (portrait, size)
# get the tiles of the image
# combine the tiles to one image
# return this image


class ImageApp(App):
    img_file = ObjectProperty()
    img_src = StringProperty()

    # show image is called when the user clicks the show_image button
    def show_image(self):
        mood = random.choice(MOOD_IDEAS)
        img_src = StringProperty()
        remote = True

        if remote:

            mood = random.choice(MOOD_IDEAS)
            img_src = StringProperty()
            artObj = ArtInfo(mood)

            art_info = artObj.get_image_list()

            art_tiles = ArtTiles(art_info)
            title = art_info['title']
            long_title = art_info['longTitle']
            art_title_obj = art_tiles.get_art_image()
            art_image = ArtImage(art_title_obj, SCREEN_WIDTH, SCREEN_HEIGHT)
            image_to_display = art_image.get_bitmap_from_tiles()

            # data = CoreImage(bytes_data,ext="RGB").texture
            now = datetime.datetime.now()
            image_to_save_file_name = "images/image_" + title + "_" + now.strftime("%Y-%m-%d-%H-%M-%S") + "."+file_ext
            image_to_display.save(image_to_save_file_name)
            self.root.ids.img.source = image_to_save_file_name
        else:
            local_art_key = random.choice(list(local_art.keys()))
            local_art_object = local_art[local_art_key]
            base_path = Path(__file__).parent.resolve()
            file_path = (base_path / local_art_object['file']).resolve()
            # local_pil_image = Image.open(file_path)
            root = self.root
            try:
                # load the image
                picture = Picture(source="phase.jpg")
                # add to the main field
                # root.add_widget(picture)
            except Exception as e:
                logger = RkLogger.__call__().get_logger()
                logger.info('Pictures: Unable to load <%s>' % file_path)
            # self.title = local_art_object['title']
            # self.long_title = local_art_object['long_title']
            # local_pil_image = local_pil_image.convert(file_ext)
            # local_pil_image = local_pil_image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
            # data = local_pil_image.getdata()  # you'll get a list of tuples
            # newData = []
            # for a in data:
            #     a = a[:3]  # you'll get your tuple shorten to RGB
            #     a = a + (100,)  # change the 100 to any transparency number you like between (0,255)
            #     newData.append(a)
            # local_pil_image.putdata(newData)  # you'll get your new img ready
            # mode = local_pil_image.mode
            # size = local_pil_image.size
            # bytes_data = local_pil_image.tobytes()
            # data = io.BytesIO(bytes_data)
            # data.seek(0)
            # cim = CoreImage(data, ext=file_ext).texture
            # self.root.ids.img.source = cim


    def build(self):
        return RootLayout()


if __name__ == "__main__":
    ImageApp().run()
