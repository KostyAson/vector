import webbrowser


class OpenYoutubeSkill:
    def __init__(self):
        self.calling_the_command = ('включи ютуб', 'открой ютуб', 'запусти ютуб')
        self.required_words = {'включи', 'открой', 'запусти', 'ютуб'}
        self.required_number_of_matches = 2
        self.is_running = False
        self.start = False
    
    def result(self, text):
        webbrowser.open_new_tab('https://youtube.com')
        return 'открываю'