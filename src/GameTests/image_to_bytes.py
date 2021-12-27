import random
from pathlib import Path
from io import BytesIO

from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
# NOTE this import is important to ensure kivy is ready to load an image from memory
from kivy.core.window import Window
from PIL import Image as PillowImage, ImageDraw

WIDTH = 1000
local_art = { \
    'vermeer': {'file':"../assets/milkmaid.png",'title':'Johannes Vermeer, The Milkmaid, c. 1660','long_title':'Johannes Vermeer, The Milkmaid, c. 1660'},
    'van-goch': {'file':"../assets/portrait.jpg",'title':'Vincent van Gogh, Self-portrait, 1887.','long_title':'Vincent van Gogh, Self-portrait, 1887.'}
    }
class Application(App):
    def build(self):
        # create a pillow image
        remote = False
        if remote:
            pillow_image = PillowImage.new(mode='RGBA', size=(WIDTH, WIDTH))
        else:
            local_art_key = random.choice(list(local_art.keys()))
            local_art_object = local_art[local_art_key]
            base_path = Path(__file__).parent.resolve()
            file_path = (base_path / local_art_object['file']).resolve()
            pillow_image = PillowImage.open(file_path)

        draw = ImageDraw.Draw(pillow_image)
        # for x in range(0, WIDTH, 5):
        #     draw.line((0, x, x, WIDTH), fill=(x, x, x, 255))
        #     draw.line((x, WIDTH, WIDTH, WIDTH - x), fill=(x, x, x, 255))
        #
        #     draw.line((WIDTH, WIDTH - x, WIDTH - x, 0), fill=(x, x, x, 255))
        #     draw.line((WIDTH - x, 0, 0, x), fill=(x, x, x, 255))

        # create bytes from the image data
        image_bytes = BytesIO()
        pillow_image.save(image_bytes, format='png')
        image_bytes.seek(0)

        # load image data in a kivy texture
        core_image = CoreImage(image_bytes, ext='png')
        texture = core_image.texture
        img = Image(texture=texture)
        return img


if __name__ == "__main__":
    Application().run()