import num_to_rus

dates = {
    '1': 'первое',
    '2': 'второе',
    '3': 'третье',
    '4': 'четвертое',
    '5': 'пятое',
    '6': 'шестое',
    '7': 'седьмое',
    '8': 'восьмое',
    '9': 'девятое',
    '10': 'десятое',
    '11': 'одинадцатое',
    '12': 'двенадцатое',
    '13': 'тринадцатое',
    '14': 'четырнадцатое',
    '15': 'пятнадцатое',
    '16': 'шестнадцатое',
    '17': 'семнадцатое',
    '18': 'восемнадцатое',
    '19': 'девятнадцатое',
    '20': 'двадцатое',
    '21': 'двадцать первое',
    '22': 'двадцать второе',
    '23': 'двадцать третье',
    '24': 'двадцать четвертое',
    '25': 'двадцать пятое',
    '26': 'двадцать шестое',
    '27': 'двадцать седьмое',
    '28': 'двадцать восьмое',
    '29': 'двадцать девятое',
    '30': 'тридцатое',
    '31': 'тридцать первое'
}
dates2 = {}
for k in dates:
    dates2[dates[k]] = k


dates_r_p = {
    '1': 'первого',
    '2': 'второго',
    '3': 'третьего',
    '4': 'четвертого',
    '5': 'пятого',
    '6': 'шестого',
    '7': 'седьмого',
    '8': 'восьмого',
    '9': 'девятого',
    '10': 'десятого',
    '11': 'одинадцатого',
    '12': 'двенадцатого',
    '13': 'тринадцатого',
    '14': 'четырнадцатого',
    '15': 'пятнадцатого',
    '16': 'шестнадцатого',
    '17': 'семнадцатого',
    '18': 'восемнадцатого',
    '19': 'девятнадцатого',
    '20': 'двадцатого',
    '21': 'двадцать первого',
    '22': 'двадцать второго',
    '23': 'двадцать третьего',
    '24': 'двадцать четвертого',
    '25': 'двадцать пятого',
    '26': 'двадцать шестого',
    '27': 'двадцать седьмого',
    '28': 'двадцать восьмого',
    '29': 'двадцать девятого',
    '30': 'тридцатого',
    '31': 'тридцать первого'
}


monthes = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'октября',
    'ноября',
    'декабря'
]


conv = num_to_rus.Converter()
digits = [conv.convert(i) for i in range(61)]

work_button_style = '''
    background-color: white;
    color: black;
    border: none;
    border-radius: 10px;
    font-size: 25px;
'''

other_button_style = '''
    QPushButton {
        color: white;
        border: 1px solid #42aaff;
        border-radius: 10px;
        font-size: 25px;
    }
    QPushButton::hover {
        background-color: #42aaff;
    }
'''

chat_style = '''
    background-color: #17191A;
    border: 1px solid white;
    border-radius: 10px;
    font-size: 25px;
    color: "white";
    margin: 60px;
'''

command_enter_style = '''
    border: 1px solid white;
    border-radius: 5px;
    color: white;
    font-size: 20px;
'''

send_command_button_style = '''
    background-color: "white";
    color: "black";
    border: none;
    border-radius: 25px;
    font-size: 35px;
'''

command_message_style = '''
    color: white;
    background-color: none;
    padding: 5px;
    margin: 5px;
    font-size: 20px;
    border: 1px solid #ac7434;
'''

answer_message_style = '''
    background-color: none;
    border: 1px solid #42aaff;
    color: white;
    padding: 5px;
    margin: 5px;
    font-size: 20px;
'''

settings_label_style = '''
    color: white;
    font-size: 20px;
    border: none;
'''

settings_check_box_style = '''
    QCheckBox {
        border: none;
    }
    QCheckBox::indicator {
        width: 25px;
        height: 25px;
        border: 1px solid white;
        border-radius: 0px;
    }
    QCheckBox::indicator:checked {
        background-color: white;
    }
'''

settings_combo_box_style = '''
    color: white;
    font-size: 20px;
    background-color: #17191A;
    border: 1px solid white;
    selection-background-color: white;
    selection-color: black;
    border-radius: 0px;
'''

back_button_style = '''
    border: 2px solid #e8c39b;
    border-radius: 25px;
    color: white;
    font-size: 35px;
    margin-left: 20px;
    margin-top: 20px;
'''

settings_widget_style = '''
    background-color: #17191A;
    border: 2px solid #e8c39b;
    border-radius: 10px;
'''

list_skills_style = '''
    QListWidget {
        background-color: #17191A;
        border: 2px solid #e8c39b;
        border-radius: 10px;
        color: white;
        font-size: 20px;
        selection-background-color: #e8c39b;
        selection-color: black;
    }
    QListWidget::item {
        color: white;
        margin-bottom: 10px;
        height: 30px;
    }
'''

yandex_speakers = ['kirill', 'filipp', 'ermil', 'madirus', 'zahar', 'alexander', 'anton']

pyttsx3_speakers = ['russian']

stt_types = ['yandex', 'vosk', 'google']

tts_types = ['yandex', 'pyttsx3']
