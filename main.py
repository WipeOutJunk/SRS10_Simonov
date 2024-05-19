from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from passlib.hash import pbkdf2_sha256

# Определение кода KV в строке для стилизации интерфейса
kv_code = '''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        pos_hint: {'top': 1.2}  # Сдвиг всего содержимого вверх

        Label:
            text: 'Login'
            font_size: 36
            size_hint_y: None
            height: self.texture_size[1]

        TextInput:
            id: username_input
            hint_text: 'Username'
            size_hint_y: None
            height: 100
            multiline: False

        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: 100
            multiline: False

        Button:
            text: 'Login'
            size_hint_y: None
            height: 90
            on_press: root.login()
            background_normal: ''
            background_color: 0, 0.5, 1, 1
            canvas.before:
                Color:
                    rgba: 0, 0.5, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    

        Label:
            id: login_status
            text: ''
            font_size: 24
            size_hint_y: None
            height: self.texture_size[1]

<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        pos_hint: {'top': 1.2}  # Сдвиг всего содержимого вверх

        Label:
            text: 'Register'
            font_size: 36
            size_hint_y: None
            height: self.texture_size[1]

        TextInput:
            id: username_input
            hint_text: 'Username'
            size_hint_y: None
            height: 100
            multiline: False

        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: 100
            multiline: False

        Button:
            text: 'Register'
            size_hint_y: None
            height: 90
            on_press: root.register()
            background_normal: ''
            background_color: 0, 0.5, 1, 1
            canvas.before:
                Color:
                    rgba: 0, 0.5, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    
'''

# Загрузка KV кода
Builder.load_string(kv_code)

# Переменные для хранения зарегистрированных данных
registered_users = {}
current_username = ''

# Определение экранов
class RegisterScreen(Screen):
    def register(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        if username and password:
            # Хэширование пароля и сохранение пользовательских данных
            hashed_password = pbkdf2_sha256.hash(password)
            registered_users[username] = hashed_password
            print(f"Registered: {username}, {hashed_password}")

            # Сброс данных в полях ввода
            self.reset_fields()

            # Переход на экран входа
            self.manager.current = 'login'
    
    def reset_fields(self):
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        if username and password:
            print(f"Logging in: {username}, {password}")
            if username in registered_users and pbkdf2_sha256.verify(password, registered_users[username]):
                self.ids.login_status.text = f"Welcome, {username}!"
                self.ids.login_status.color = (0, 1, 0, 1)  # Зеленый цвет
            else:
                self.ids.login_status.text = "Invalid username or password"
                self.ids.login_status.color = (1, 0, 0, 1)  # Красный цвет
        else:
            self.ids.login_status.text = "Please enter both username and password"
            self.ids.login_status.color = (1, 0, 0, 1)  # Красный цвет


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LoginScreen(name='login'))
        return sm

if __name__ == "__main__":
    MainApp().run()
