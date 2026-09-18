from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
import random
import os

chars = '12344567890azertyuiopqsdfghjklmwxcvbn.'
SAVE_FILE = 'passwords_history.txt'

Window.clearcolor = (0.08, 0.08, 0.12, 1)

class PasswordApp(App):
    def build(self):
        self.password = ''
        self.history_visible = False
        self.history_list = []

        root = BoxLayout(orientation='vertical', padding=25, spacing=12)

        title = Label(text='[b]Password Generator[/b]', markup=True,
                       font_size=28, size_hint_y=None, height=55,
                       color=(1, 1, 1, 1))

        self.input = TextInput(hint_text='How many characters?', input_filter='int',
                                size_hint_y=None, height=55, multiline=False,
                                font_size=18, padding=[15, 15, 15, 15],
                                background_color=(0.95, 0.95, 0.95, 1))

        gen_btn = Button(text='Generate', size_hint_y=None, height=55,
                          font_size=18, bold=True,
                          background_normal='', background_color=(0.15, 0.55, 0.9, 1),
                          on_press=self.generate)

        self.result = Label(text='Your password will appear here', size_hint_y=None,
                             height=55, font_size=20, bold=True,
                             color=(0.35, 1, 0.55, 1))

        copy_btn = Button(text='Copy current password', size_hint_y=None, height=50,
                           font_size=16, background_normal='',
                           background_color=(0.25, 0.25, 0.3, 1),
                           on_press=self.copy_password)

        self.toggle_btn = Button(text='Show history', size_hint_y=None, height=50,
                                  font_size=16, background_normal='',
                                  background_color=(0.45, 0.3, 0.55, 1),
                                  on_press=self.toggle_history)

        self.history_container = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.history_container.bind(minimum_height=self.history_container.setter('height'))

        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.history_container)
        self.scroll.opacity = 0
        self.scroll.size_hint_y = None
        self.scroll.height = 0

        self.clear_btn = Button(text='Clear history', size_hint_y=None, height=0,
                                 font_size=15, background_normal='',
                                 background_color=(0.6, 0.2, 0.2, 1),
                                 on_press=self.clear_history)
        self.clear_btn.opacity = 0

        root.add_widget(title)
        root.add_widget(self.input)
        root.add_widget(gen_btn)
        root.add_widget(self.result)
        root.add_widget(copy_btn)
        root.add_widget(self.toggle_btn)
        root.add_widget(self.scroll)
        root.add_widget(self.clear_btn)

        self.load_history()
        return root

    def toggle_history(self, instance):
        self.history_visible = not self.history_visible
        if self.history_visible:
            self.scroll.opacity = 1
            self.scroll.size_hint_y = 1
            self.clear_btn.opacity = 1
            self.clear_btn.height = 45
            self.toggle_btn.text = 'Hide history'
        else:
            self.scroll.opacity = 0
            self.scroll.size_hint_y = None
            self.scroll.height = 0
            self.clear_btn.opacity = 0
            self.clear_btn.height = 0
            self.toggle_btn.text = 'Show history'

    def add_history_item(self, pwd):
        item_btn = Button(text=pwd, size_hint_y=None, height=45,
                           font_size=15, background_normal='',
                           background_color=(0.18, 0.18, 0.22, 1),
                           color=(0.8, 0.9, 1, 1))
        item_btn.bind(on_press=lambda inst, p=pwd: self.copy_from_history(p))
        self.history_container.add_widget(item_btn)
        self.history_list.append(pwd)

    def copy_from_history(self, pwd):
        Clipboard.copy(pwd)
        self.result.text = 'Copied: ' + pwd

    def load_history(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.add_history_item(line)

    def save_history(self):
        with open(SAVE_FILE, 'w') as f:
            f.write('\n'.join(self.history_list))

    def generate(self, instance):
        try:
            n = int(self.input.text)
            self.password = ''.join(random.choice(chars) for _ in range(n))
            self.result.text = self.password
            self.add_history_item(self.password)
            self.save_history()
        except ValueError:
            self.result.text = 'Enter a valid number'
            self.password = ''

    def copy_password(self, instance):
        if self.password:
            Clipboard.copy(self.password)
            self.result.text = 'Copied to clipboard!'

    def clear_history(self, instance):
        self.history_container.clear_widgets()
        self.history_list = []
        self.save_history()

PasswordApp().run()
