import random


class CoinFlipSkill:
    def __init__(self):
        self.calling_the_command = ('подбрось монетку',)
        self.required_words = {'монетку', 'монету', 'подбрось', 'брось'}
        self.required_number_of_matches = 2
    
    def result(self, text):
        res = random.randint(1, 2)
        if res == 1:
            return 'Выпала решка'
        else:
            return 'Выпал орёл'
