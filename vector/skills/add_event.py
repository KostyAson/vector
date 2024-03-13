from vector import variables
import datetime as dt
from vector.skills.functions_for_skills import request_to_planner_server


class AddEventsSkill:
    def __init__(self, vector):
        self.calling_the_command = ('добавь событие в календарь', 'добавь событие', 'создай событие')
        self.required_words = {'добавь', 'событие', 'создай', 'события'}
        self.required_number_of_matches = 2
        self.vector = vector
        self.condition = None

    def result(self, text):
        self.vector.condition = self
        self.condition = 'date'
        return 'На какую дату запланировано событие?'

    def get_next_command(self, text):
        if self.condition == 'date':
            date = None
            month = None
            text = text.lower().split()
            for i in range(31, 0, -1):
                if str(i) in text or variables.dates[str(i)] in ' '.join(text):
                    date = i
                    break
            if date is None:
                return 'Введите корректную дату'
            for x in variables.monthes:
                if x in text:
                    month = x
                    break
            today = dt.datetime.today()
            if month is None:
                month = variables.monthes[today.month - 1]
            if today.month > variables.monthes.index(month) + 1:
                year = today.year + 1
            else:
                year = today.year
            self.date = date
            self.month = month
            self.year = year
            self.condition = 'text'
            return 'Опишите событие'
        self.text = text
        self.vector.condition = None
        return self.add_event()

    def add_event(self):
        self.month = variables.monthes.index(self.month) + 1
        if self.vector.telegram_id is not None:
            data = f'addevent {self.date} {self.month} {self.year} {self.vector.telegram_id} {self.text}'.encode()
            res = request_to_planner_server(data)
            if res.decode() == 'done':
                return f'добавил событие'
        return 'данная функция не доступна без входа в телеграм'
