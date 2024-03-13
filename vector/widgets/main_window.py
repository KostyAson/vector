from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QLabel, QLayout, QSizePolicy
from PyQt5.QtCore import Qt
import vector.variables as variables
import vector.widgets.settings

class MainWindowLayout(QVBoxLayout):
    def __init__(self, a, vec, app):
        super().__init__(a)
        self.vec = vec

        self.chat = Chat()
        self.chat.setStyleSheet(variables.chat_style)
        self.chat.setFixedSize(1000, 500)

        self.command_enter = QLineEdit()
        self.command_enter.setStyleSheet(variables.command_enter_style)
        self.command_enter.setFixedSize(300, 50)

        self.send_command_button = QPushButton(text='->')
        self.send_command_button.setStyleSheet(variables.send_command_button_style)
        self.send_command_button.setFixedSize(50, 50)
        self.send_command_button.clicked.connect(self.send_command)

        self.send_command_form = QHBoxLayout()
        self.send_command_form.addWidget(self.command_enter)
        self.send_command_form.addWidget(self.send_command_button)
        self.send_command_form.setAlignment(Qt.AlignCenter)

        settings = QWidget()
        settings.setStyleSheet(variables.settings_widget_style)
        settings.setLayout(vector.widgets.settings.SettingsLayout(vec, app))
        self.addWidget(settings, alignment=Qt.AlignCenter)
        self.addWidget(self.chat, alignment=Qt.AlignCenter)
        self.addLayout(self.send_command_form)
        self.setAlignment(Qt.AlignCenter)

        self.is_work = False

        self.app = app

    def work_button_event(self, event):
        self.app.set_new_widget('off')
    
    def settings_button_event(self, event):
        self.app.set_new_widget('settings')

    def send_command(self):
        text = self.command_enter.text()
        self.add_command_message(text)
        self.command_enter.setText('')
        self.update()
        self.vec.get_text(text, from_app=True)
    
    def add_command_message(self, text):
        if text in ['отключись', 'выключись']:
            self.work_button_event(None)
        self.chat.add_message(text, False)

    def add_answer_message(self, text):
        self.chat.add_message(text, True)


class Chat(QScrollArea):
    def __init__(self):
        super().__init__()
        self.w = QWidget()
        self.w.setStyleSheet('border: none;')
        self.l = QVBoxLayout()
        self.l.setAlignment(Qt.AlignTop)
        self.l.setSizeConstraint(QLayout.SetMinimumSize)
        self.w.setLayout(self.l)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setWidget(self.w)

        self.vbar = self.verticalScrollBar()
        self.vbar.setFixedSize(0, 0)
        self.vbar.rangeChanged.connect(self.scroll_to_end)

    def add_message(self, text, answer):
        message = QLabel()
        message.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        message.setWordWrap(True)
        message.setFixedWidth(min((len(text)) * 10 + 60, 600))
        message.setText(text)
        if answer:
            message.setStyleSheet(variables.answer_message_style)
        else:
            message.setStyleSheet(variables.command_message_style)
        self.l.addWidget(message, alignment=Qt.AlignLeft if answer else Qt.AlignRight)
        message.adjustSize()
        message.setFixedHeight(message.height() if message.width() >= 600 else 43)

    def scroll_to_end(self, _min, _max):
        self.vbar.setValue(_max)


class MainWindow(QWidget):
    def __init__(self, vec, app):
        super().__init__()
        MainWindowLayout(self, vec, app)
        funcions_button = QPushButton(self)
        funcions_button.clicked.connect(self.set_functions_window)
        funcions_button.setStyleSheet(variables.back_button_style)
        funcions_button.setFixedSize(70, 70)
        funcions_button.setText('F')
        self.app = app
    
    def set_functions_window(self, e):
        self.app.set_new_widget('functions')
