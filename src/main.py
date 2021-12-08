from kivy.app import App
from kivy import Config
from kivy.properties import ObjectProperty
from navigation_screen_manager import NavigationScreenManager


# from kivy.uix.widget import Widget

Config.set('graphics', 'multisamples', '0')


class RkScreenManager(NavigationScreenManager):
    pass


class RkMainApp(App):
    manager = ObjectProperty(None)

    def build(self):
        self.manager = RkScreenManager()
        return self.manager


RkMainApp().run()
