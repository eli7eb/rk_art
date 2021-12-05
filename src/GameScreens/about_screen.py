
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("about_screen.kv")

class AboutScreen(BoxLayout):
    title = StringProperty()