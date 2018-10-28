from json import loads
from threading import Thread
from time import time

from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
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
    general_count = True
    username = StringProperty()
    current_group = StringProperty("World")
    post_history = dict()
    group_to_window = dict()
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

        self._user_screen.group_drop_down.bind(on_press=self._group_down.open)
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
            Clock.schedule_once(lambda dt: self._update_group_to_window())
        elif self._screen_manager.current_screen.name == "register":
            Clock.schedule_once(lambda dt: self._change_screen("login", self._register_screen))
        elif self._screen_manager.current_screen.name == "home":
            data = loads(r.content.decode(encoding="utf-8"))
            Clock.schedule_once(lambda dt: self._load_general_posts(data))
        elif self._screen_manager.current_screen.name == "post":
            data = loads(r.content.decode(encoding="utf-8"))
            Clock.schedule_once(lambda dt: self._load_single_post(data))
        elif self._screen_manager.current_screen.name == "user":
            data = loads(r.content.decode(encoding="utf-8"))
            Clock.schedule_once(lambda dt: self._load_user_page(data))
        elif self._screen_manager.current_screen.name == "write":
            data = loads(r.content.decode(encoding="utf-8"))
            Clock.schedule_once(lambda dt: self._get_single_post(data["post_id"]))

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
            self._group_down.width = Window.size[0] - 230
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
            Clock.schedule_interval(self._update_count_down, 1)
        elif target == "post":
            self._screen_exit(previous_screen)
            if Window.size != (800, 700):
                Window.size = (800, 700)
            self._screen_manager.current = "post"

    def _screen_exit(self, screen: Screen) -> None:
        self._group_down.dismiss()
        self._navi_down.dismiss()
        if type(screen) is LoginScreen:
            screen.login_username.text = ""
            screen.login_password.text = ""
        elif type(screen) is RegisterScreen:
            screen.register_username.text = ""
            screen.register_password.text = ""
            screen.register_snd_password.text = ""
        elif type(screen) is UserScreen:
            self._group_down.width = Window.size[0] - 150
        elif type(screen) is WriteScreen:
            self.post_history[self.current_group] = self._write_screen.input.text

    def _load_general_posts(self, data: dict) -> None:
        self._home_screen.post_container.clear_widgets()
        for entry in data['posts']:
            new_entry = GeneralPostEntry()
            new_entry.text = entry["text"]
            new_entry.author_id = entry["author_id"]
            new_entry.author_name = entry["author_name"]
            new_entry.rating = entry["rating"]
            new_entry.post_id = entry["post_id"]
            new_entry.published = entry["published"]
            self._home_screen.post_container.add_widget(new_entry)

    def _load_single_post(self, data: dict) -> None:
        self._post_screen.title = data["text"]
        self._post_screen.author = data["author_name"]
        self._post_screen.author_id = data["author_id"]
        self._post_screen.rating = data["rating"]
        self._post_screen.post_id = data["post_id"]
        self._post_screen.published = data["published"]
        self._post_screen.window_id = data["window_id"]

    def _load_user_page(self, data: dict) -> None:
        self._user_screen.username = data["username"]
        self._user_screen.avatar_url = data["avatar_url"]
        self._user_screen.rating = data["rating"]
        self._user_screen.user_id = data["user_id"]
        self._user_screen.posts = data["posts"]
        self._user_screen.groups = data["groups"]
        self._user_screen.post_container.clear_widgets()
        self._write_screen.post_container.clear_widgets()
        count = 0
        for window in data["windows"]:
            count += 1
            new_entry = WindowEntry()
            new_entry.group = window["group"]
            new_entry.start_time = window["start_time"]
            new_entry.duration = window["duration"]
            new_entry.window_id = window["window_id"]
            self._write_screen.post_container.add_widget(new_entry, 0)
        if count > 0:
            self._user_screen.write.background_color = [0, 1, 0, 1]
        for entry in data["posts"]:
            new_entry = GeneralPostEntry()
            new_entry.text = entry["text"]
            new_entry.author_id = entry["author_id"]
            new_entry.author_name = entry["author_name"]
            new_entry.rating = entry["rating"]
            new_entry.post_id = entry["post_id"]
            new_entry.published = entry["published"]
            self._user_screen.post_container.add_widget(new_entry)
        self._update_group_down(data["groups"])

    def _update_group_down(self, data: list):
        self._group_down.clear_widgets()
        for entry in data:
            new_entry = GroupEntry()
            new_entry.group = entry["name"]
            new_entry.group_id = entry["group_id"]
            self._group_down.add_widget(new_entry)

    def _update_count_down(self, arg):
        if self._screen_manager.current_screen.name != "write":
            return False
        for window in self._write_screen.post_container.children:
            if type(window) is WindowEntry:
                remaining_time = window.start_time + window.duration - time()
                window.count_down.text = "{}:{}:{}".format(int(remaining_time / 3600),
                                                           int((remaining_time % 3600) / 60),
                                                           int(remaining_time % 60))
        return True

    def _update_post_history(self, next_group):
        self.post_history[self.current_group] = self._write_screen.input.text
        try:
            self._write_screen.input.text = self.post_history[next_group]
        except KeyError:
            self._write_screen.input.text = ""

    def _update_timer(self, data):
        self._write_screen.post_container.clear_widgets()
        count = 0
        for window in data["windows"]:
            count += 1
            new_entry = WindowEntry()
            new_entry.group = window["group"]
            new_entry.start_time = window["start_time"]
            new_entry.duration = window["duration"]
            new_entry.window_id = window["window_id"]
            self._write_screen.post_container.add_widget(new_entry, 0)
        if count > 0:
            self._user_screen.write.background_color = [0, 1, 0, 1]

    def _update_group_to_window(self):
        r = self.kernel.fetch_user()
        if self._screen_manager.current_screen.name == "home":
            data = loads(r.content.decode(encoding="utf-8"))
            for entry in data["windows"]:
                self.group_to_window[entry["group"]] = entry["window_id"]
        self._update_group_down(data["groups"])
        self._update_timer(data)

    def _test(self):
        return

    def _login(self, username: str, password: str):
        thread = Thread(target=self.kernel.login, args=(username, password,))
        thread.start()
        self.username = username

    def _register(self, username: str, password: str, snd_password: str):
        if password != snd_password:
            Clock.schedule_once(lambda dt: self._alter("Inconsistent Passwords"))
        else:
            thread = Thread(target=self.kernel.register, args=(username, password,))
            thread.start()

    def _get_general_post(self):
        if self.general_count:
            thread = Thread(target=self.kernel.get_general_post())
            thread.start()
            self.general_count = False
        else:
            Clock.schedule_once(lambda dt: self._change_screen("home", self._screen_manager.current_screen))
            group_id = "0"
            for entry in self._group_down.children[0].children:
                if entry.text == self.current_group:
                    group_id = entry.group_id
                    break
            self._update_posts(group_id)

    def _get_single_post(self, post_id: str):
        thread = Thread(target=self.kernel.get_single_post, args=(post_id,))
        thread.start()
        Clock.schedule_once(lambda dt: self._change_screen("post", self._screen_manager.current_screen))

    def _get_own_page(self):
        thread = Thread(target=self.kernel.get_own_page)
        thread.start()
        Clock.schedule_once(lambda dt: self._change_screen("user", self._screen_manager.current_screen))

    def _publish_post(self, text: str):
        try:
            thread = Thread(target=self.kernel.publish_post, args=(text, self.group_to_window[self.current_group],))
            thread.start()
        except KeyError:
            self._alter("No open window for Group " + self.current_group)

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

    def _update_posts(self, group_id):
        if self._screen_manager.current_screen.name == "home":
            Clock.schedule_once(lambda dt: self.kernel.get_conditional_post(group_id))


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


class WindowEntry(BoxLayout):
    pass


class GroupEntry(Button):
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
