import asyncio
from vector.app import App
from PyQt5.QtWidgets import QApplication
import fuzzywuzzy.process
import sys
from vector.skills.add_event import AddEventsSkill
from vector.skills.chatgpt import ChatGptSkill
from vector.skills.coin_flip import CoinFlipSkill
from vector.skills.exchange_rates import ExchangeRatesSkill
from vector.skills.get_event import SayEventSkill
from vector.skills.open_telegram import OpenTelegramSkill
from vector.skills.open_vk import OpenVKSkill
from vector.skills.open_youtube import OpenYoutubeSkill
from vector.skills.reminder import ReminderSkill
from vector.skills.say_data import SayDataSkill
from vector.skills.say_time import SayTimeSkill
from vector.skills.say_weather import SayWeatherSkill
from vector.skills.stopwatch import StopwatchSkill
from vector.skills.telegram import TelegramSkill
from vector.skills.timer import TimerSkill
from vector.skills.guess_song import GuessSongSkill
from vector.tts import Tts
from vector.stt import Stt
import pyaudio
import aiohttp
import pvporcupine
import struct
import playsound
import dotenv
import vector.settings as settings
import platform

dotenv.load_dotenv('.env')


class Vector:
    def __init__(self):
        self.tts = Tts()
        self.skill_on_command = {}
        self.skills = {
            'Текущее время': SayTimeSkill(),
            'Текущая погода': SayWeatherSkill(),
            'Телеграмм': TelegramSkill(self),
            'Текущая дата': SayDataSkill(),
            'Секундомер': StopwatchSkill(),
            'Открыть Ютуб': OpenYoutubeSkill(),
            'YaGPT': ChatGptSkill(self),
            'Добавить событие': AddEventsSkill(self),
            'Таймер': TimerSkill(self),
            'Назвать события': SayEventSkill(self),
            'Напомнить': ReminderSkill(self),
            'Открыть Телеграмм': OpenTelegramSkill(),
            'Открыть ВК': OpenVKSkill(),
            'Подбросить Монетку': CoinFlipSkill(),
            'Курсы валют': ExchangeRatesSkill(),
            'Назвать песню': GuessSongSkill(self)
        }
        self.update_available_commands()
        self.is_work = False
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.condition = None
        self.telegram_enter = False
        self.telegram_id = None
        self.start_listen = False
        s1 = f'models/wake_word_{platform.system().lower()}.ppn'
        s2 = f'models/porcupine_params_ru_{platform.system().lower()}.pv'
        self.porcupine = pvporcupine.create(keyword_paths=[s1],
                            access_key="MQ/MUU2o0b6AItZAaa2AApPpjiNeQFOEJ1LsuyqYcosZs47NEolzJQ==",
                            model_path=s2,
                            sensitivities=[0.7])
        self.event_loop = asyncio.get_event_loop()
        self.trigger_words = [
            ('спроси', 0, self.skills['YaGPT']),
            ('напиши', 0, self.skills['Телеграмм']),
            ('напомни', 0, self.skills['Напомнить'])
        ]

    async def make_http_request(self, is_get, url, data, headers, f):
        async with aiohttp.ClientSession() as session:
            if not is_get:
                async with session.post(url, json=data, headers=headers) as response:
                    result = await response.json()
                    f(result)

    def get_event_loop(self):
        return asyncio.get_event_loop()

    def run_qt_loop(self):
        application = QApplication(sys.argv)
        self.app = App(self)
        self.app.show()
        application.exec_()
        exit()

    def update_available_commands(self):
        for x in self.skills:
            for y in self.skills[x].calling_the_command:
                self.skill_on_command[y] = self.skills[x]

    async def start_working(self):
        loop = asyncio.get_event_loop()
        qt_task = loop.run_in_executor(None, self.run_qt_loop)
        tg = self.skills['Телеграмм']
        await tg.client.connect()
        if await tg.client.is_user_authorized():
            me = await tg.client.get_me()
            tg.user_id = me.id
            self.telegram_id = me.id
            await tg.get_user_contacts()
            await asyncio.gather(
                tg.client.start(),
                self.start_cycle(),
                qt_task
            )
        else:
            await asyncio.gather(
                self.start_cycle(),
                qt_task
            )
    
    def vector_wake_word(self, indata):
        keyword_index = self.porcupine.process(indata)
        if keyword_index >= 0:
            print('start listen')
        return keyword_index >= 0

    async def start_cycle(self):
        while True:
            self.event_loop = asyncio.get_event_loop()
            if self.telegram_enter:
                self.telegram_enter = False
                res = await self.skills['Телеграмм'].enter()
                self.get_result(res, True)
            if self.stream is not None:
                data = self.stream.read(512, exception_on_overflow=False)
                if self.start_listen:
                    self.stop_stream()
                    stt = Stt()
                    text = stt.convert()
                    self.start_stream()
                    if text != 'nothing':
                        self.get_text(text)
                    if self.condition is None:
                        self.start_listen = False
                        print('end listen')
                    else:
                        print('condition')
                else:
                    pcm = struct.unpack_from("h" * 512, data)
                    self.start_listen = self.vector_wake_word(pcm)
                    if self.start_listen:
                        playsound.playsound('sounds/start_listen.mp3', False)
            await asyncio.sleep(0)

    def get_text(self, text, from_app=False):
        self.update_available_commands()
        if not from_app:
            self.app.get_command_signal.emit(text)
        if self.condition is not None:
            res = self.condition.get_next_command(text)
            self.get_result(res, from_app)
            return
        spli = text.split()
        for x in self.trigger_words:
            if x[0] in spli and (spli.index(x[0]) == x[1] or x[1] == -1):
                res = x[2].result(text)
                self.get_result(res, from_app)
                return
        commands = fuzzywuzzy.process.extract(
            text, self.skill_on_command.keys()
        )
        for x in commands:
            skill = self.skill_on_command[x[0]]
            if (
                len(skill.required_words & set(text.split()))
                >= skill.required_number_of_matches
            ):
                res = skill.result(text)
                self.get_result(res)
                break

    def get_result(self, text, from_app=None):
        if text:
            self.app.get_answer_signal.emit(text.replace('+', ''))
            if settings.get('voice_answer'):
                self.stop_stream()
                self.tts.talk(text)
                self.start_stream()

    def stop_stream(self):
        self.stream = None

    def start_stream(self):
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=512
        )
