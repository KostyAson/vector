import asyncio
import datetime as dt
from vector.skills.functions_for_skills import total_seconds_in_command


class TimerSkill:
    def __init__(self, vector):
        self.calling_the_command = ('поставь таймер на',)
        self.required_words = {'поставь', 'включи', 'запусти', 'таймер'}
        self.required_number_of_matches = 2
        self.is_running = False
        self.start = False
        self.vector = vector

    def result(self, text):
        if not self.start:
            self.start = True
            self.start_time = dt.datetime.now()
            self.calling_the_command = ('сколько времени осталось', 'выключи таймер')
            self.required_words = {'сколько', 'времени', 'время', 'выключи', 'отключи', 'останови', 'таймер'}
            ans = text.split(' на ')[1]
            ans = 'поставил таймер на ' + ans
            self.sm = total_seconds_in_command(text)[0]
            self.vector.event_loop.create_task(self.wait_timer())
            return ans
        if 'выключи' in text or 'останови' in text or 'отключи' in text:
            self.start = False
            self.calling_the_command = ('поставь таймер', 'включи таймер')
            self.required_words = {'поставь', 'включи', 'запусти', 'таймер'}
            return 'Отключил таймер'

    async def wait_timer(self):
        await asyncio.sleep(self.sm)
        self.vector.get_result('Таймер закончился')
        self.start = False
        self.calling_the_command = ('поставь таймер', 'включи таймер')
        self.required_words = {'поставь', 'включи', 'запусти', 'таймер'}
