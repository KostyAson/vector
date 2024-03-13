import webbrowser


class OpenVKSkill:
    def __init__(self):
        self.calling_the_command = ('открой вк', 'открой вконтакте')
        self.required_words = {'открой', 'вк', 'вконтакте'}
        self.required_number_of_matches = 2
    
    def result(self, text):
        webbrowser.open_new_tab('https://vk.com')
        return 'открываю'
