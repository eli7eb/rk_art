from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from PIL import Image as Image1
from kivy.uix.image import Image

#GUI = Builder.load_file('style.kv')
Builder.load_string('''
<NotebookScreen>
    FloatLayout:
        GridLayout:
            size_hint: 1, .05
            pos_hint: {"top": 1, "left": 1}
            id: tool_bar
            cols: 1
            canvas:
                Color:
                    rgba: 0, 0, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        GridLayout:
            id: notebook_grid
            size_hint: 1, .95
            pos_hint: {"top": .95, "left": 0}
            cols: 1

            MyScrollView:
                do_scroll: (False, True)  # up and down

                BoxLayout:
                    id: notebook_images
                    orientation: 'vertical'
                    size_hint: 1, None
                    height: self.minimum_height
                    MyImage:
<MyImage>:
    source: 'images/art_row_0_col_0_The Sick Child.jpg'
    allow_stretch: True
    keep_ratio: True
    size_hint: None, None
    size: self.get_size_for_notebook()
''')

Window.size = (1000, 200)
img_size =Image1.open("images/art_row_0_col_0_The Sick Child.jpg").size


class MyImage(Image):
    def get_size_for_notebook(self, **kwargs):
        global img_size
        width, height = Window.size
        return width, (img_size[0] * height / width)


class MyScrollView(ScrollView):
    def on_scroll_y(self, instance, scroll_val):
        if scroll_val < 0.05:  # no logic for this number
            box = App.get_running_app().root.ids.notebook_images
            new_image = MyImage()
            box.add_widget(new_image)
            self.scroll_y = new_image.height / box.height  # a more careful calculation may provide smoother operation


class NotebookScreen(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super(NotebookScreen, self).__init__(**kwargs)


class MainApp(App):

    def build(self):
        return NotebookScreen()


if __name__ == "__main__":
    MainApp().run()