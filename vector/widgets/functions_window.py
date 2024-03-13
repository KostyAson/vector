from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QListWidget, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
import vector.variables as variables


class FunctionLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.commands_label = QLabel()
        self.commands_label.setText('Команды для вызова')
        self.commands = QListWidget()
        self.commands.setFixedWidth(350)
        self.commands.setStyleSheet(variables.list_skills_style)
        self.commands.setEnabled(False)
        self.commands_label.setStyleSheet(variables.settings_label_style)
        
        self.required_words_label = QLabel()
        self.required_words_label.setText('Слова триггеры')
        self.required_words_label.setStyleSheet(variables.settings_label_style)
        self.required_words = QListWidget()
        self.required_words.setFixedWidth(350)
        self.required_words.setStyleSheet(variables.list_skills_style)
        self.required_words.setEnabled(False)

        self.required_number_of_matches_label = QLabel()
        self.required_number_of_matches_label.setStyleSheet(variables.settings_label_style)
        self.required_number_of_matches_label.setText('Обязательное количество слов триггеров')

        self.required_number_of_matches = QLabel()
        self.required_number_of_matches.setStyleSheet(variables.settings_label_style)

        self.addWidget(self.commands_label, 0, 0, alignment=Qt.AlignCenter)
        self.addWidget(self.commands, 0, 1, alignment=Qt.AlignCenter)

        self.addWidget(self.required_words_label, 1, 0, alignment=Qt.AlignCenter)
        self.addWidget(self.required_words, 1, 1, alignment=Qt.AlignCenter)

        self.addWidget(self.required_number_of_matches_label, 2, 0, alignment=Qt.AlignCenter)
        self.addWidget(self.required_number_of_matches, 2, 1, alignment=Qt.AlignCenter)

        self.setSpacing(50)


class FunctionsWindowLayout(QHBoxLayout):
    def __init__(self, s, vec, app):
        super().__init__(s)
        self.vec = vec
        self.app = app
        self.list_skills = QListWidget()
        self.list_skills.addItems(self.vec.skills.keys())
        self.list_skills.setFixedSize(250, 650)
        self.list_skills.setStyleSheet(variables.list_skills_style)
        self.list_skills.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_skills.currentTextChanged.connect(self.set_new_skill)
        self.function_layout = FunctionLayout()
        self.addWidget(self.list_skills, alignment=Qt.AlignCenter)
        self.addLayout(self.function_layout)

    def set_new_skill(self, e):
        text = self.list_skills.currentItem().text()
        skill = self.vec.skills[text]
        self.function_layout.commands.clear()
        self.function_layout.commands.addItems(skill.calling_the_command)

        self.function_layout.required_words.clear()
        self.function_layout.required_words.addItems(skill.required_words)

        self.function_layout.required_number_of_matches.setText(str(skill.required_number_of_matches))

        self.function_layout.commands.setFixedHeight(45 * len(skill.calling_the_command))
        self.function_layout.required_words.setFixedHeight(45 * len(skill.required_words))


class FunctionsWindow(QWidget):
    def __init__(self, vec, app):
        super().__init__()
        FunctionsWindowLayout(self, vec, app)
        funcions_button = QPushButton(self)
        funcions_button.clicked.connect(self.set_functions_window)
        funcions_button.setStyleSheet(variables.back_button_style)
        funcions_button.setFixedSize(70, 70)
        funcions_button.setText('<-')
        self.app = app

    def set_functions_window(self, e):
        self.app.set_new_widget('main window')
