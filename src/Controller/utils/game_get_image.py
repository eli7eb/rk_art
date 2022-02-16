import random
import datetime
from pathlib import Path
import requests
import json
from kivy.uix.image import Image as KImage
from kivy.core.image import Image as CoreImage
from PIL import Image
from io import BytesIO
from array import *
from kivy.properties import StringProperty
from random import randrange
from src.GameConsts.game_consts import PORTRAIT, LANDSCAPE, MOOD_IDEAS, SCREEN_WIDTH, SCREEN_HEIGHT, local_art
from Controller.utils.game_logger import RkLogger
from Controller.utils.rk_http_requests import HttpRequestInfo


GLOBAL_TILE_SIZE = 512

# TODO add try catch for all interactions with the API
# explained https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python
file_ext = 'jpg'
file_mode = 'RGB'

class GetArtImage():

    def __init__(self, game_level):
        self.game_level = game_level

        self.logger = RkLogger.__call__().get_logger()



    # box=(left, upper, right, lower).
    # prepare a 2 dim array for the image as PIL and for the texture
    def crop_pil_image(self, pillow_image,title):
        # resize to 600 800

        # prepare a grid for the texture too
        # load image data in a kivy texture


        self.pil_image = pillow_image
        self.title = title
        tile_size = self.game_level.tile_size
        tiles_hor = self.game_level.tiles_hor
        tiles_ver = self.game_level.tiles_ver
        index = 0
        tiles_grid_dict = []
        # tiles_grid_dict = [dict() for i in range(tiles_hor*tiles_ver)]
        self.logger.info(self.title)
        for i in range(tiles_ver):
            col = []
            for j in range(tiles_hor):
                box = (tile_size*j,tile_size*i,tile_size*j+tile_size,tile_size*i+tile_size)
                print(box)
                crop_tile = self.pil_image.crop(box)
                k_crop_tile = crop_tile.copy()
                # get the texture and kimage from pil image
                k_image_bytes = BytesIO()
                try:
                    k_crop_tile.save(k_image_bytes, format='png')
                    k_image_bytes.seek(0)
                except Exception as e:
                    self.logger.error("e "+e)
                finally:
                    core_image = CoreImage(k_image_bytes, ext='png')
                texture = core_image.texture
                k_image = KImage()
                k_image.texture = texture
                # add unique identifier for the cropped save
                # TODO in the end delete this
                now = datetime.datetime.now()
                now_str = now.strftime("%Y-%m-%d-%H-%M-%S")
                crop_name = "assets/cropped_"+str(index)+"_"+str(i)+"_"+str(j)+"_image_"+now_str+".png"
                try :
                    crop_tile.save(crop_name)
                except Exception as e:
                    self.logger.error(e + " " + self.title)
                finally:
                    try:
                        tiles_grid_dict.append({'tile_x':j,'tile_y':i,'pil_tile':crop_tile,'texture': texture,'k_image':k_image})
                        index+=1
                    except Exception as ae:
                        self.logger.error(ae)
                        raise SystemExit(ae)

        return tiles_grid_dict

    def resize_image(self, pil_image):
        pass

    def get_art_image(self,mood_str):
        remote = False
        if (mood_str == '' and remote is True):
            mood = random.choice(MOOD_IDEAS)
        else:
            mood = mood_str
        img_src = StringProperty()


        if remote:

            art_info_obj = ArtInfo()
            # get list of possible works of art
            art_info = art_info_obj.get_image_list(mood)

            art_tiles = ArtTiles()
            self.title = art_info['title']
            self.long_title = art_info['longTitle']
            art_title_obj = art_tiles.get_art_image_by_object_number(art_info['objectNumber'])
            art_image = ArtImage(art_title_obj, SCREEN_WIDTH, SCREEN_HEIGHT)
            image_to_display = art_image.get_bitmap_from_tiles()

            pillow_image = art_image.get_bitmap_from_tiles()

            now = datetime.datetime.now()
            #image_to_save_file_name = "images/image_" + title + "_" + now.strftime("%Y-%m-%d-%H-%M-%S") + "." + file_ext
            #pillow_image.save(image_to_save_file_name)
        else:
            local_art_key = random.choice(list(local_art.keys()))

            local_art_object = local_art[local_art_key]
            base_path = Path(__file__).parent.resolve()
            file_path =  local_art_object['file']
            grid_image = Image.open(base_path/file_path)

            self.title = local_art_object['title']
            self.long_title = local_art_object['long_title']
            pillow_image = grid_image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)


        # before return - create a grid of tiles
        tiles_grid = self.crop_pil_image(pillow_image,self.title)



        return tiles_grid, self.title, self.long_title
        #self.root.ids.img.texture = texture


class ArtInfo:

    def get_image_list(self,search_mood):
        rk_request = HttpRequestInfo()
        art_list = rk_request.get_image_list_by_search_value(search_mood)
        return art_list

class SearchArt:

    def __init__(self, mood_str):
        self.currentState = None
        self.search_value = mood_str
        self.logger = RkLogger.__call__().get_logger()





class ArtTiles:
    print('get the one')

    def __init__(self):
        self.currentState = None
        self.logger = RkLogger.__call__().get_logger()

    def get_art_image_by_object_number(self, object_number):
        self.object_number = object_number
        rk_request = HttpRequestInfo()
        json_obj = rk_request.get_image_list_by_object_number(self.object_number)
        return json_obj


# handle cropped image
# take the texture and divide it to grid tiles
# return grid of tiles
class GetCroppedImage:
    def __init__(self, **kwargs):
        pass



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
