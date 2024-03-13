import dotenv
import os
dotenv.load_dotenv('.env')


class ChatGptSkill:
    def __init__(self, vector):
        self.calling_the_command = ('спроси',)
        self.required_words = {'спроси'}
        self.required_number_of_matches = 1
        self.vector = vector

    def result(self, text):
        text = ' '.join(text.split()[1:])
        data = {
            "modelUri": "gpt://b1gjin4pnsh2luov48ik/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "user",
                    "text": text
                }
            ]
        }
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {os.getenv('yagpt_key')}"
        }
        self.vector.event_loop.create_task(self.vector.make_http_request(False, url, data, headers, self.get_result))
        return 'Отправил запрос'

    def get_result(self, result):
        try:
            self.vector.get_result(result['result']['alternatives'][0]['message']['text'], False)
        except Exception as e:
            print('\nERROR', str(e), '\n')
