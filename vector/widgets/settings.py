from PyQt5.QtWidgets import QCheckBox, QLabel, QComboBox, QGridLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
import vector.variables as variables
import vector.settings as settings


class SettingsLayout(QGridLayout):
    def __init__(self, vec, app):
        super().__init__()
        self.change = False
        tts = settings.get('tts')
        self.vec = vec
        self.app = app

        self.speaker_label = QLabel()
        self.speaker_label.setStyleSheet(variables.settings_label_style)
        self.speaker_label.setText('Спикер')
        self.speaker = QComboBox()
        self.speaker.currentIndexChanged.connect(self.change_speaker)
        self.speaker.setStyleSheet(variables.settings_combo_box_style)
        self.speaker.addItems(['russian'] if tts == 'pyttsx3' else variables.yandex_speakers)
        self.speaker.setMinimumWidth(120)

        self.stt_label = QLabel()
        self.stt_label.setText('Распознавание')
        self.stt_label.setStyleSheet(variables.settings_label_style)
        self.stt_types = QComboBox()
        self.stt_types.currentIndexChanged.connect(self.change_stt)
        self.stt_types.setMinimumWidth(80)
        self.stt_types.setStyleSheet(variables.settings_combo_box_style)
        self.stt_types.addItems(variables.stt_types)

        self.tts_label = QLabel()
        self.tts_label.setText('Озвучка')
        self.tts_label.setStyleSheet(variables.settings_label_style)
        self.tts_types = QComboBox()
        self.tts_types.currentIndexChanged.connect(self.change_tts)
        self.tts_types.setMinimumWidth(100)
        self.tts_types.setStyleSheet(variables.settings_combo_box_style)
        self.tts_types.addItems(variables.tts_types)

        self.notifications_label = QLabel()
        self.notifications_label.setStyleSheet(variables.settings_label_style)
        self.notifications_label.setText('Уведомления')
        self.notifications = QCheckBox()
        self.notifications.setStyleSheet(variables.settings_check_box_style)
        self.notifications.setChecked(settings.get('notifications'))
        self.notifications.stateChanged.connect(self.change_notifications)

        self.voice_answer_label = QLabel()
        self.voice_answer_label.setStyleSheet(variables.settings_label_style)
        self.voice_answer_label.setText('Голосовой ответ')
        self.voice_answer = QCheckBox()
        self.voice_answer.setStyleSheet(variables.settings_check_box_style)
        self.voice_answer.setChecked(settings.get('voice_answer'))
        self.voice_answer.stateChanged.connect(self.change_voice_answer)

        self.microphone_label = QLabel()
        self.microphone_label.setStyleSheet(variables.settings_label_style)
        self.microphone_label.setText('Микрофон')
        self.microphone = QCheckBox()
        self.microphone.setStyleSheet(variables.settings_check_box_style)
        self.microphone.stateChanged.connect(self.change_microphone)
        self.microphone.setChecked(True)

        self.addWidget(self.stt_label, 0, 0)
        self.addWidget(self.stt_types, 1, 0)
        self.addWidget(self.tts_label, 0, 1, alignment=Qt.AlignCenter)
        self.addWidget(self.tts_types, 1, 1)
        self.addWidget(self.speaker_label, 0, 2, alignment=Qt.AlignCenter)
        self.addWidget(self.speaker, 1, 2)
        self.addWidget(self.notifications_label, 0, 3)
        self.addWidget(self.notifications, 1, 3, alignment=Qt.AlignCenter)
        self.addWidget(self.voice_answer_label, 0, 4)
        self.addWidget(self.voice_answer, 1, 4, alignment=Qt.AlignCenter)
        self.addWidget(self.microphone_label, 0, 5)
        self.addWidget(self.microphone, 1, 5, alignment=Qt.AlignCenter)
        self.setSpacing(20)

        self.change = True

        self.speaker.setCurrentText(settings.get('yandex_speaker' if tts == 'yandex' else 'pyttsx3_speaker'))
        self.stt_types.setCurrentText(settings.get('stt'))
        self.tts_types.setCurrentText(settings.get('tts'))
    
    def change_microphone(self, e):
        if self.microphone.isChecked():
            self.vec.start_stream()
        else:
            self.vec.stop_stream()
    
    def change_speaker(self, e):
        if self.change:
            s = 'yandex_speaker' if settings.get('tts') == 'yandex' else 'pyttsx3_speaker'
            settings.set(s, self.speaker.currentText())
    
    def change_stt(self, e):
        if self.change:
            settings.set('stt', self.stt_types.currentText())
    
    def change_tts(self, e):
        if not self.change:
            return
        settings.set('tts', self.tts_types.currentText())
        if self.tts_types.currentText() == 'pyttsx3':
            self.speaker.clear()
            self.speaker.addItems(variables.pyttsx3_speakers)
            self.speaker.setCurrentText(settings.get('pyttsx3_speaker'))
        else:
            self.speaker.clear()
            self.speaker.addItems(variables.yandex_speakers)
            self.speaker.setCurrentText(settings.get('yandex_speaker'))
    
    def change_voice_answer(self, e):
        settings.set('voice_answer', self.voice_answer.isChecked())
    
    def change_notifications(self, e):
        settings.set('notifications', self.notifications.isChecked())


class Settings(QWidget):
    def __init__(self, vec, app):
        super().__init__()
        self.setLayout(SettingsLayout(vec, app))
        self.setStyleSheet(variables.settings_widget_style)
        self.setFixedWidth(900)
