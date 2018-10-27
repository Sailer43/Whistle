from kivy.app import App
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.settings import Settings
from kivy.uix.widget import Widget

from src.utils.decorators import overrides


class ClientApp(App):
    _screen_manager = ScreenManager(transition=SlideTransition())
    _login_screen = None
    _register_screen = None
    _user_screen = None

    @overrides(App)
    def __init__(self, **kwargs) -> None:
        super(ClientApp, self).__init__(**kwargs)

    @overrides(App)
    def build(self) -> Widget:
        Window.size = (500, 200)
        Builder.load_file("client.kv")
        self._login_screen = LoginScreen(name="login")
        self._register_screen = RegisterScreen(name="register")
        self._user_screen = UserScreen(name="user")
        self._screen_manager.add_widget(self._login_screen)
        self._screen_manager.add_widget(self._register_screen)
        self._screen_manager.add_widget(self._user_screen)
        return self._screen_manager

    @overrides(App)
    def build_config(self, config: ConfigParser) -> None:
        pass

    @overrides(App)
    def build_settings(self, settings: Settings) -> None:
        pass

    @overrides(App)
    def on_config_change(self,
                         config: ConfigParser,
                         section: str,
                         key: str,
                         value: str) -> None:
        pass

    @overrides(App)
    def on_stop(self) -> None:
        pass

    def _change_screen(self, target: str, previous_screen: Screen) -> None:
        if target == "login":
            if type(previous_screen) is RegisterScreen:
                self._login_screen.login_username.text = previous_screen.register_username.text
            else:
                pass
            self._screen_exit(previous_screen)
            Window.size = (500, 200)
            self._screen_manager.current = "login"
        elif target == "register":
            self._screen_exit(previous_screen)
            Window.size = (500, 250)
            self._screen_manager.current = "register"
        elif target == "user":
            self._screen_exit(previous_screen)
            Window.size = (800, 1000)
            self._screen_manager.current = "user"

    def _screen_exit(self, screen: Screen) -> None:
        if type(screen) is LoginScreen:
            screen.login_username.text = ""
            screen.login_password.text = ""
        elif type(screen) is RegisterScreen:
            screen.register_username.text = ""
            screen.register_password.text = ""
            screen.register_snd_password.text = ""


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class UserScreen(Screen):
    pass


def main():
    app = ClientApp()
    app.run()


if __name__ == '__main__':
    main()
