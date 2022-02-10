import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

Builder.load_file("View/settings_screen.kv")

class SettingsScreen(Screen):
    title = StringProperty()