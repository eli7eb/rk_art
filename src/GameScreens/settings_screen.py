
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("settings_screen.kv")

class Settingscreen(BoxLayout):
    title = StringProperty()