from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, PasswordHashInvalidError
from telethon.tl.types import User
import playsound
import vector.variables as variables
import asyncio
import fuzzywuzzy.process
import dotenv
import os
import vector.settings
from vector.functions_for_skills import (
    word_with_digit
)
dotenv.load_dotenv('.env')


class TelegramSkill:
    def __init__(self, vector):
        self.calling_the_command = (
            'войди в телеграм',
            'прочитай последние n сообщений',
            'прочитай последнее сообщение',
            'прочитай все сообщения',
            'напиши',
            'отправь сообщение'
        )
        self.required_words = {'прочитай', 'войди', 'напиши', 'отправь', 'читай'}
        self.required_number_of_matches = 1
        self.api_id = int(os.getenv('telegram_api_id'))
        self.api_hash = os.getenv('telegram_api_hash')
        self.client = TelegramClient('anon', self.api_id, self.api_hash)
        self.client.add_event_handler(self.messages_handler, events.NewMessage)
        self.messages = []
        self.user_id = None
        self.vector = vector
        self.number = None
        self.enter_code = None
        self.password = None
        self.contacts_name = []
        self.contacts_id = []

    async def get_user_contacts(self):
        async for x in self.client.iter_dialogs():
            if isinstance(x.entity, User):
                self.contacts_name.append(x.name)
                self.contacts_id.append(x.id)

    async def messages_handler(self, event):
        if event.message.from_id is not None:
            sender_id = event.message.from_id.user_id
            from_user = await self.client.get_entity(sender_id)
            if sender_id != self.user_id:
                if vector.settings.get('notifications'):
                    playsound.playsound('sounds/notification.mp3', False)
                name = ''
                if from_user.contact:
                    if from_user.first_name is not None:
                        name += from_user.first_name
                    if from_user.last_name is not None:
                        name += from_user.last_name
                else:
                    name += 'неизвестный контакт'
                self.messages.append((name, event.message.message))
                if len(self.messages) > 10:
                    self.messages = self.messages[-10:]

    async def enter(self):
        self.vector.condition = self
        while self.number is None:
            await asyncio.sleep(0)
        await self.client.send_code_request(self.number)
        while self.password is None:
            await asyncio.sleep(0)
        try:
            await self.client.sign_in(self.number, self.enter_code, password=self.password)
        except PhoneCodeInvalidError:
            return 'Неверный код подтверждения'
        except PasswordHashInvalidError:
            return 'Неверный пароль'
        loop = asyncio.get_event_loop()
        loop.create_task(self.client.start())
        me = await self.client.get_me()
        self.user_id = me.id
        self.vector.telegram_id = me.id
        await self.get_user_contacts()
        return 'Вход выполнен'
    
    def get_next_command(self, text):
        if not self.number:
            self.number = text
            return 'введите код подтверждения'
        if not self.enter_code:
            self.enter_code = text
            return 'введите пароль или ничего если не задан'
        if not self.password:
            self.password = text
        self.vector.condition = None
        return 'Произвожу попытку входа'


    def result(self, text):
        if 'войди' in text:
            self.vector.telegram_enter = True
            self.number = None
            self.enter_code = None
            self.password = None
            return 'Введите номер телефона'
        if 'напиши' in text or 'отправь' in text:
            text = text.replace('сообщение', '', 1)
            text = text.replace('контакту', '', 1)
            text = text.split()
            contact = text[1]
            contact = fuzzywuzzy.process.extractOne(contact, self.contacts_name)
            mess = ' '.join(text[2:])
            id = self.contacts_id[self.contacts_name.index(contact[0])]
            self.vector.event_loop.create_task(self.client.send_message(id, mess))
            return 'отправил сообщение контакту ' + contact[0]
        rez = ''
        if 'последнее' in text:
            i = -1
        elif 'последние' in text:
            n = text.split(' последние ')[1].split()[0]
            if n in variables.digits:
                i = -(variables.digits.index(n))
            else:
                return 'укажите нужное количество сообщений'
            
            if abs(i) > len(self.messages):
                if len(self.messages) == 0:
                    return 'входящих сообщений нет'
                s = word_with_digit(['сообщение', 'сообщения', 'сообщений'], len(self.messages))
                return f'пришло только {len(self.messages)} {s}'     
        else:
            i = -len(self.messages)
        if not self.messages:
            return 'Нет входящих сообщений'
        for x in self.messages[i:]:
            rez += f' от {x[0]}: {x[1]}.\n'
        return rez