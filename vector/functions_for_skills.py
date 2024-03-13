import vector.variables as variables
import socket
import dotenv
import os
import datetime as dt
dotenv.load_dotenv('.env')


def word_with_digit(words, digit):
    digit = abs(digit)
    if digit % 10 == 1 and digit != 11:
        word = words[0]
    elif str(digit)[-1] in '234' and (digit < 10 or digit > 20):
        word = words[1]
    else:
        word = words[2]
    return word


def total_seconds_in_command(text):
    if ' через ' in text or 'таймер' in text:
        remind = text.split(' через ')[0][8:]
        text = text.replace('секунды', 'секунд').replace('секунду', 'секунд')
        text = text.replace('часа', 'час').replace('часов', 'час')
        text = text.replace('минуту', 'минут').replace('минуты', 'минут')
        text = text.split()
        sm = 0
        if 'секунд' in text:
            i = text.index('секунд')
            s = text[i - 1]
            if not s.isdigit():
                if s == 'одну':
                    s = 'один'
                if s == 'две':
                    s = 'два'
                if text[i - 2] in variables.digits:
                    s = text[i - 2] + ' ' + s
                sm += (variables.digits.index(s))
            else:
                sm += int(s)
        if 'минут' in text:
            i = text.index('минут')
            s = text[i - 1]
            if not s.isdigit():
                if s == 'одну':
                    s = 'один'
                if s == 'две':
                    s = 'два'
                if text[i - 2] in variables.digits:
                    s = text[i - 2] + ' ' + s
                sm += (variables.digits.index(s)) * 60
            else:
                sm += int(s) * 60
        if 'час' in text:
            i = text.index('час')
            s = text[i - 1]
            if not s.isdigit():
                if text[i - 2] in variables.digits:
                    s = text[i - 2] + ' ' + s
                sm += (variables.digits.index(s)) * 60 * 60
            else:
                sm += int(s) * 60 * 60
    if ' в ' in text:
        time = []
        remind = text.split(' в ')[0][8:]
        text = text.replace('часов', '').replace('часа', '').replace('час', '')
        text = text.replace('минуты', '').replace('минута', '').replace('минут', '')
        for x in text.split(' в ')[1].split():
            if x in variables.digits:
                time.append(variables.digits.index(x))
            else:
                return 'время указано некорректно'
        if len(time) > 4 or len(time) < 2:
            return 'время указано некорректно'
        if len(time) == 2:
            hours = time[0]
            minutes = time[1]
        elif len(time) == 4:
            hours = int(str(time[0])[0] + str(time[1]))
            minutes = int(str(time[2])[0] + str(time[3]))
        elif len(time) == 3:
            if time[0] > 19:
                if time[1] > 9:
                    hours = time[0]
                    minutes = int(str(time[1])[0] + str(time[2]))
                else:
                    hours = int(str(time[0])[0] + str(time[1]))
                    minutes = time[2]
            else:
                hours = time[0]
                minutes = int(str(time[1])[0] + str(time[2]))
        d = dt.datetime.today()
        d = dt.datetime(year=d.year, day=d.day, month=d.month, hour=hours, minute=minutes)
        sm = int((d - dt.datetime.now()).total_seconds())
        if sm < 0:
            sm = 24 * 60 * 60 + sm
    return (sm, remind)


def request_to_planner_server(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((os.getenv('planer_server_ip'), int(os.getenv('planer_server_port'))))
        sock.sendall(request)
        res = sock.recv(1024)
        sock.close()
        return res
