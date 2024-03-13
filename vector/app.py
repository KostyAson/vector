from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import pyqtSignal
from vector.widgets.main_window import MainWindow
from vector.widgets.functions_window import FunctionsWindow


class App(QMainWindow):
    get_command_signal = pyqtSignal(str)
    get_answer_signal = pyqtSignal(str)

    def __init__(self, vec):
        super().__init__()
        self.setWindowTitle('Vector')
        self.vec = vec
        self.setFixedSize(1200, 800)
        self.setStyleSheet('background-color: #17191A')

        self.get_command_signal.connect(self.get_command)
        self.get_answer_signal.connect(self.get_answer)

        self.stacked_widget = QStackedWidget()
        self.main_window = MainWindow(self.vec, self)
        self.functions_window = FunctionsWindow(self.vec, self)
        self.stacked_widget.addWidget(self.functions_window)
        self.stacked_widget.addWidget(self.main_window)
        self.setCentralWidget(self.stacked_widget)

        self.set_new_widget('main window')
    
    def get_command(self, text):
        self.main_window.layout().add_command_message(text)
    
    def get_answer(self, text):
        self.main_window.layout().add_answer_message(text)
    
    def set_new_widget(self, layout):
        if layout == 'main window':
            self.stacked_widget.setCurrentWidget(self.main_window)
        else:
            self.stacked_widget.setCurrentWidget(self.functions_window)
        
    
    def keyPressEvent(self, a0):
        if a0.key() == 16777220 and self.main_window.layout().command_enter.text():
            self.main_window.layout().send_command()
