
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("play_screen.kv")

class PlayScreen(BoxLayout):
    title = StringProperty()