from kivy.uix.screenmanager import ScreenManager


class NavigationScreenManager (ScreenManager):
    screen_stack = []
    mood_str = ''

    def push(self, screen_name, mood_string='default'):
        if screen_name not in self.screen_stack:
            # in the case we switch from main to play - get the mood

            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name
            if screen_name == 'PlayScreen':
                self.mood_str = mood_string
                self.current_screen.play_mood_str = mood_string

    def pop(self):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name

    def pass_play_mood(self, mood):
        # self.mood_str = self.s
        pass
