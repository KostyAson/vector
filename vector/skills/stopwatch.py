import datetime as dt
import num_to_rus


class StopwatchSkill:
    def __init__(self):
        self.calling_the_command = ('поставь секундомер', 'включи секундомер')
        self.required_words = {'поставь', 'включи', 'запусти', 'секундомер'}
        self.required_number_of_matches = 2
        self.is_running = False
        self.start = False

    def result(self, text):
        if not self.start:
            self.start = True
            self.start_time = dt.datetime.now()
            self.calling_the_command = ('сколько времени прошло', 'выключи секундомер')
            self.required_words = {'сколько', 'времени', 'время', 'выключи', 'отключи', 'останови', 'секундомер'}
            return 'Включил секундомер'
        if 'выключи' in text or 'останови' in text or 'отключи' in text:
            self.start = False
            self.calling_the_command = ('поставь секундомер', 'включи секундомер')
            self.required_words = {'поставь', 'включи', 'запусти', 'секундомер'}
            return 'Отключил секундомер'
        delta = dt.datetime.now() - self.start_time
        hours = delta.total_seconds() / 60 // 60
        minutes = (delta.total_seconds() - (hours * 60 * 60)) // 60
        seconds = delta.total_seconds() - (hours * 60 * 60 + (minutes * 60))
        converter = num_to_rus.Converter()
        return f'Прошло {converter.convert(int(hours))} часов {converter.convert(int(minutes))} минут {converter.convert(int(seconds))} секунд'