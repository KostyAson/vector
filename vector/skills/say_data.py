import datetime as dt
from vector import variables


class SayDataSkill:
    def __init__(self):
        self.calling_the_command = (
            'скажи дату',
            'какое сегодня число',
            'какая сегодня дата',
        )
        self.required_words = {'дата', 'число'}
        self.required_number_of_matches = 1
        self.dates = variables.dates

    def result(self, text):
        data = dt.date.today().day
        if data < 20 or data % 10 == 0:
            return f'сегодня {self.dates[str(data)]} число'
        s = 'двадцать' if str(data)[0] == '2' else 'тридцать'
        return f'сегодня {s} {self.dates[str(data)[1]]} число'
