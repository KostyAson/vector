import datetime as dt
from vector.skills.functions_for_skills import word_with_digit
import cbr


class ExchangeRatesSkill:
    def __init__(self):
        self.calling_the_command = ('какой курс', 'курс')
        self.required_words = {'курс'}
        self.required_number_of_matches = 1
    
    def result(self, text):
        d = dt.date.today()
        day = str(d.day).rjust(2, '0')
        month = str(d.month).rjust(2, '0')
        v = None
        if 'доллар'in text:
            v = 'USD'
        elif 'евро' in text:
            v = 'EUR'
        elif 'юан' in text:
            v = 'CNY'
        elif 'фунт' in text:
            v = 'GBP'
        if v is None:
            return 'не поддерживаемая валюта'
        v = cbr.get_exchange_rates(f'{day}.{month}.{d.year}', symbols=[v])[0]['rate']
        d = str(v).split('.')[0]
        s = word_with_digit(['рубль', 'рубля', 'рублей'], int(d))
        return d + ' ' + s
