from json import loads
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.settings import Settings
from kivy.uix.widget import Widget
from requests import Response

from src.client.client_kernel import ClientKernel
from src.utils.decorators import overrides


class ClientApp(App):
    response = ObjectProperty()
    _screen_manager = ScreenManager(transition=SlideTransition())
    _login_screen = None
    _register_screen = None
    _user_screen = None
    _home_screen = None
    _write_screen = None
    _post_screen = None
    _navi_down = None
    _group_down = None
    colors = {
        "back01": [7 / 255, 54 / 255, 66 / 255, 1],
        "violet": [108 / 255, 113 / 255, 196 / 255, 1],
        "cyan": [42 / 255, 161 / 255, 152 / 255, 1]
    }

    @overrides(App)
    def __init__(self, **kwargs) -> None:
        self.__events__ = ["on_reponse"]
        super(ClientApp, self).__init__(**kwargs)
        self.response_book = {
            200: self._success,
            201: self._success,
        }
        self.kernel = ClientKernel(self)

    @overrides(App)
    def build(self) -> Widget:
        Window.size = (500, 200)
        self._login_screen = LoginScreen(name="login")
        self._register_screen = RegisterScreen(name="register")
        self._user_screen = UserScreen(name="user")
        self._home_screen = HomeScreen(name="home")
        self._write_screen = WriteScreen(name="write")
        self._post_screen = PostScreen(name="post")
        self._group_down = GroupDropDown()
        self._navi_down = NaviDropDown()

        for screen in [self._home_screen, self._post_screen, self._write_screen]:
            screen.navi_drop_down.bind(on_press=self._on_navi)
            screen.group_drop_down.bind(on_press=self._on_group)

        self._screen_manager.add_widget(self._login_screen)
        self._screen_manager.add_widget(self._register_screen)
        self._screen_manager.add_widget(self._user_screen)
        self._screen_manager.add_widget(self._home_screen)
        self._screen_manager.add_widget(self._write_screen)
        self._screen_manager.add_widget(self._post_screen)
        self._login_screen.login_username.focus = True
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

    def on_response(self, instance: App, r: Response) -> None:
        if not r:
            return
        self.response_book[r.status_code](r)

    def _success(self, r: Response):
        if self._screen_manager.current_screen.name == "login":
            Clock.schedule_once(lambda dt: self._change_screen("home", self._login_screen))
            Clock.schedule_once(lambda dt: self._get_general_post())
        elif self._screen_manager.current_screen.name == "register":
            Clock.schedule_once(lambda dt: self._change_screen("login", self._register_screen))
        elif self._screen_manager.current_screen.name == "home":
            data = loads(r.content.decode(encoding="utf-8"))
            Clock.schedule_once(lambda dt: self._load_general_posts(data))
        elif self._screen_manager.current_screen.name == "post":
            data = loads(r.content.decode(encoding="utf-8"))
            Clock.schedule_once(lambda dt: self._load_single_post(data))

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
            if Window.size != (800, 700):
                Window.size = (800, 700)
            self._screen_manager.current = "user"
        elif target == "home":
            self._screen_exit(previous_screen)
            if Window.size != (800, 700):
                Window.size = (800, 700)
            self._screen_manager.current = "home"
        elif target == "write":
            self._screen_exit(previous_screen)
            if Window.size != (800, 700):
                Window.size = (800, 700)
            self._screen_manager.current = "write"
        elif target == "post":
            self._screen_exit(previous_screen)
            if Window.size != (800, 700):
                Window.size = (800, 700)
            self._screen_manager.current = "post"

    def _screen_exit(self, screen: Screen) -> None:
        if type(screen) is LoginScreen:
            screen.login_username.text = ""
            screen.login_password.text = ""
        elif type(screen) is RegisterScreen:
            screen.register_username.text = ""
            screen.register_password.text = ""
            screen.register_snd_password.text = ""

    def _load_general_posts(self, data: dict) -> None:
        for entry in data['posts']:
            new_entry = GeneralPostEntry()
            new_entry.text = entry["text"]
            new_entry.author_id = entry["author_id"]
            new_entry.author_name = entry["author_name"]
            new_entry.rating = entry["rating"]
            new_entry.id = entry["id"]
            self._home_screen.post_container.add_widget(new_entry)

    def _load_single_post(self, data: dict) -> None:
        print(data)
        pass

    def _test(self):
        return

    def _login(self, username: str, password: str):
        thread = Thread(target=self.kernel.login, args=(username, password,))
        thread.start()

    def _register(self, username: str, password: str, snd_password: str):
        if password != snd_password:
            Clock.schedule_once(lambda dt: self._alter("Inconsistent Passwords"))
        else:
            thread = Thread(target=self.kernel.register, args=(username, password,))
            thread.start()

    def _get_general_post(self):
        thread = Thread(target=self.kernel.get_general_post())
        thread.start()

    def _get_single_post(self, post_id: str):
        thread = Thread(target=self.kernel.get_single_post, args=(post_id,))
        thread.start()
        Clock.schedule_once(lambda dt: self._change_screen("post", self._screen_manager.current_screen))

    def _logoff(self) -> None:
        self.kernel.logoff()
        Clock.schedule_once(lambda dt: self._change_screen("login", self._screen_manager.current_screen))

    def _on_navi(self, instance):
        self._navi_down.open(instance)
        self._group_down.dismiss()

    def _on_group(self, instance):
        self._group_down.open(instance)
        self._navi_down.dismiss()

    def _alter(self, msg: str):
        content = Button(text=msg)
        alert = Popup(title="Alert:",
                      content=content,
                      auto_dismiss=False)
        content.bind(on_press=alert.dismiss)
        alert.open()


class UserPostEntry(BoxLayout):
    pass


class GroupDropDown(DropDown):
    pass


class NaviDropDown(DropDown):
    pass


class ClickLabel(ButtonBehavior, Label):
    pass


class ClickImage(ButtonBehavior, AsyncImage):
    pass


class GeneralPostEntry(BoxLayout):
    pass


class Header(BoxLayout):
    pass


class LoginScreen(Screen):
    pass


class RegisterScreen(Screen):
    pass


class UserScreen(Screen):
    def __init__(self, **kwargs):
        super(UserScreen, self).__init__(**kwargs)
        self.post_container.bind(minimum_height=self.post_container.setter('height'))


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.post_container.bind(minimum_height=self.post_container.setter('height'))


class WriteScreen(Screen):

    def __init__(self, **kwargs):
        super(WriteScreen, self).__init__(**kwargs)
        self.post_container.bind(minimum_height=self.post_container.setter('height'))


class PostScreen(Screen):

    def __init__(self, **kwargs):
        super(PostScreen, self).__init__(**kwargs)
        self.post_container.bind(minimum_height=self.post_container.setter('height'))


def main():
    app = ClientApp()
    app.run()


if __name__ == '__main__':
    main()
