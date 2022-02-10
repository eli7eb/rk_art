import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

#path=os.getcwd()
#project_path=path+"\\"+"src"+"\\"+"GameScreens"+"\\"
Builder.load_file("View/about_screen.kv")

class AboutScreen(Screen):
    title = StringProperty()