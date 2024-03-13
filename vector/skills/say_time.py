import num_to_rus
import time
from vector.skills.functions_for_skills import word_with_digit


class SayTimeSkill:
    def __init__(self):
        self.calling_the_command = (
            'Какое сейчас время',
            'сколько времени',
            'который час',
        )
        self.required_words = {'времени', 'время', 'час'}
        self.required_number_of_matches = 1
        self.num_to_words = num_to_rus.Converter()

    def result(self, text):
        hours = time.localtime().tm_hour
        minutes = time.localtime().tm_min
        hours_word = word_with_digit(['час', 'часа', 'часов'], hours)
        minutes_word = word_with_digit(['минута', 'минуты', 'минут'], minutes)
        minutes_digit_word = self.num_to_words.convert(minutes)
        if minutes % 10 in [1, 2] and (minutes < 10 or minutes > 19):
            s = 'одна' if minutes % 10 == 1 else 'две'
            if minutes > 2:
                minutes_digit_word = minutes_digit_word.split()[0] + ' ' + s
            else:
                minutes_digit_word = s
        return (
            f'{self.num_to_words.convert(hours)} {hours_word} '
            f'{minutes_digit_word} {minutes_word}'
        )
