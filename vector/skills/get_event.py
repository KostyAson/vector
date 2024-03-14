from vector import variables
import datetime as dt
from vector.skills.functions_for_skills import request_to_planner_server


class SayEventSkill:
    def __init__(self, vector):
        self.calling_the_command = ('назови события на', 'скажи события на', 'прочитай события на')
        self.required_words = {'назови', 'скажи', 'прочитай', 'события', 'событие'}
        self.required_number_of_matches = 2
        self.vector = vector

    def result(self, text):
        self.date = None
        for i in range(31, 0, -1):
            if str(i) in text or variables.dates[str(i)] in text or variables.dates_r_p[str(i)] in text:
                self.date = i
                break
        if self.date is None:
            return 'Не корректная дата'
        self.month = None
        today = dt.datetime.today()
        for x in variables.monthes:
            if x in text:
                self.month = x
                break
        if self.month is None:
            self.month = variables.monthes[today.month - 1]
        if today.month > variables.monthes.index(self.month) + 1:
            self.year = today.year + 1
        else:
            self.year = today.year
        return self.get_event()

    def get_event(self):
        self.month = variables.monthes.index(self.month) + 1
        if self.vector.telegram_id is not None:
            data = f'getevent {self.date} {self.month} {self.year} {self.vector.telegram_id}'.encode()
            res = request_to_planner_server(data)
            ans = ''
            for i, x in enumerate(res.decode().split('\n')):
                if x:
                    ans += f'{i + 1}) {x}.\n'
            return ans[:-1]
        return 'данная функция не доступна без входа в телеграм'
