import num_to_rus
import requests
from vector.skills.functions_for_skills import word_with_digit
import dotenv
import os
dotenv.load_dotenv('.env')


class SayWeatherSkill:
    def __init__(self):
        self.calling_the_command = (
            'какая сейчас погода',
            'какая погода',
            'что по погоде',
        )
        self.required_words = {'погода'}
        self.required_number_of_matches = 1
        self.num_to_rus = num_to_rus.Converter()

    def result(self, text):
        try:
            data = requests.get(
                'http://api.openweathermap.org/data/2.5/weather',
                params={
                    'q': 'Moscow',
                    'units': 'metric',
                    'lang': 'ru',
                    'APPID': os.getenv('openweathermap'),
                },
                timeout=5).json()
        except requests.exceptions.ReadTimeout:
            return 'сервер с погодой в данный момент не доступен'
        temp = int(data['main']['temp'])
        temp_feels_like = int(data['main']['feels_like'])
        temp_word = self.num_to_rus.convert(temp)
        temp_feels_like_word = self.num_to_rus.convert(temp_feels_like)

        wind = int(data['wind']['speed'])
        wind_word = self.num_to_rus.convert(wind)
        gradus_word = word_with_digit(['градус', 'градуса', 'градусов'], temp)
        gradus_feels_like_word = word_with_digit(['градус', 'градуса', 'градусов'], temp_feels_like)
        metr_word = word_with_digit(['метр', 'метра', 'метров'], wind)

        return (
            f'сейчас в Москве {temp_word} {gradus_word},'
            f' ощущается как {temp_feels_like_word} {gradus_feels_like_word[:2] + "+" + gradus_feels_like_word[2:]},'
            f' {data["weather"][0]["description"]}, скорость в+етра {wind_word} {metr_word} в секунду'
        )
