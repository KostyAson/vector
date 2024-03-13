import webbrowser


class OpenTelegramSkill:
    def __init__(self):
        self.calling_the_command = ('открой телеграмм',)
        self.required_words = {'открой', 'телеграмм', 'телегу', 'тг', 'телеграм'}
        self.required_number_of_matches = 2
    
    def result(self, text):
        print(1)
        webbrowser.open_new_tab('https://web.telegram.org')
        return 'открываю'
