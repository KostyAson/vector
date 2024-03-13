from shazamio import Shazam
import pyaudio
import wave


class GuessSongSkill:
    def __init__(self, vector):
        self.calling_the_command = ('угадай песню', 'назови мелодию')
        self.required_words = {'назови', 'угадай', 'песню', 'мелодию'}
        self.required_number_of_matches = 2
        self.vector = vector
        self.frame = []

    def result(self, text):
        self.vector.event_loop.create_task(self.start_guess())
        return 'Слушаю'

    async def start_guess(self):
        print('start guess')
        shazam = Shazam(language='ru')
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()
        frames = []  
        for _ in range(0, int(16000 / 8000 * 5)):
            data = stream.read(8000)
            frames.append(data)
        sf = wave.open('sounds/song.wav', 'wb')
        sf.setnchannels(1)
        sf.setframerate(16000)
        sf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        sf.writeframes(b''.join(frames))
        sf.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        out = await shazam.recognize_song('sounds/song.wav')
        self.vector.condition = None
        try:
            self.vector.get_result(out['track']['subtitle'] + ' - ' + out['track']['title'])
        except KeyError:
            self.vector.get_result('Песня не распознана')
