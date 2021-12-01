

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
from kivy.uix.widget import Widget

Config.set('graphics', 'multisamples', '0')


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):

    def process(self):
        print(self.ids.mood.text)

    def go_play(self):
        # check for no value = random art
        mood_text = self.ids.mood.text
    pass


class OptionsWindow(Screen):
    pass


class PlayWindow(Screen):
    pass


class AboutWindow(Screen):
    pass


kv = Builder.load_file('rk.kv')


class RkMainApp(App):
    def build(self):
        self.root = kv
        return kv

if __name__ == "__main__":
    RkMainApp().run()