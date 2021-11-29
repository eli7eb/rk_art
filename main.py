

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
Config.set('graphics', 'multisamples', '0')

class RkMainApp(App):
    def build(self):
        self.root = Builder.load_file('rk.kv')

    def process(self):
        mood_text = self.root.ids.mood
        print(mood_text)


class MainWindow(Screen):
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