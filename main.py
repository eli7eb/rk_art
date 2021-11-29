

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
from kivy.uix.widget import Widget

Config.set('graphics', 'multisamples', '0')


class RkMainApp(App):
    def build(self):
        self.root = Builder.load_file('rk.kv')


class MainWindow(Screen):

    def process(self):
        print(self.ids.mood.text)

    def go_play(self):
        mood_text = self.ids.mood.text
    pass


class OptionsWindow(Screen):
    pass

class PlayWindow(Screen):
    pass

class AboutWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

if __name__ == "__main__":
    RkMainApp().run()