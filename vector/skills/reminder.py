from vector.skills.functions_for_skills import (
    total_seconds_in_command,
    request_to_planner_server
)
import asyncio


class ReminderSkill:
    def __init__(self, vector):
        self.calling_the_command = ('напомни в', 'напомни через')
        self.required_words = {'создай', 'напомни', 'через'}
        self.required_number_of_matches = 1
        self.vector = vector

    def result(self, text):
        if ' через ' in text or ' в ' in text:
            sm = total_seconds_in_command(text)
            self.vector.event_loop.create_task(self.wait_res(sm[0], sm[1]))
            if self.vector.telegram_id is not None:
                request_to_planner_server(f'remind {sm[0]} {self.vector.telegram_id} {sm[1]}'.encode())
            return 'создал напоминание'
        return 'не распознал напоминание'

    async def wait_res(self, sm, remind):
        await asyncio.sleep(sm)
        self.vector.get_result('напоминаю ' + remind, False)
