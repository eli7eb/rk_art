import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

path=os.getcwd()
project_path=path+"\\"+"src"+"\\"+"GameScreens"+"\\"
Builder.load_file(project_path+"\\"+"play_screen.kv")


class PlayScreen(BoxLayout):
    title = StringProperty()