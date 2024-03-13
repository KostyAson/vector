import grpc
from cloudapi.output.yandex.cloud.ai.stt.v3 import stt_pb2
from cloudapi.output.yandex.cloud.ai.stt.v3 import stt_service_pb2_grpc
import time
import vector.settings as settings
from vosk import Model, KaldiRecognizer
import json
import speech_recognition
import pyaudio
import dotenv
import os
dotenv.load_dotenv('.env')


class Stt:
    def __init__(self, stream=None):
        self.stream = stream
        self.is_run = True
        self.start_talk = False
        self.start_time = time.time()

    def gen(self):
        recognize_options = stt_pb2.StreamingOptions(
            recognition_model=stt_pb2.RecognitionModelOptions(
                audio_format=stt_pb2.AudioFormatOptions(
                    raw_audio=stt_pb2.RawAudio(
                        audio_encoding=stt_pb2.RawAudio.LINEAR16_PCM,
                        sample_rate_hertz=16000,
                        audio_channel_count=1,
                    )
                ),
                language_restriction=stt_pb2.LanguageRestrictionOptions(
                    restriction_type=stt_pb2.LanguageRestrictionOptions.WHITELIST,
                    language_code=["ru-RU"],
                ),
                audio_processing_type=stt_pb2.RecognitionModelOptions.REAL_TIME,
            ),
            eou_classifier=stt_pb2.EouClassifierOptions(
                default_classifier=stt_pb2.DefaultEouClassifier(
                    type='HIGH',
                    max_pause_between_words_hint_ms=500
                )
            )
        )
        yield stt_pb2.StreamingRequest(session_options=recognize_options)
        while self.is_run:
            data = self.stream.read(512)
            yield stt_pb2.StreamingRequest(chunk=stt_pb2.AudioChunk(data=data))


    def run_yandex(self):
        cred = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel("stt.api.cloud.yandex.net:443", cred)
        stub = stt_service_pb2_grpc.RecognizerStub(channel)
        it = stub.RecognizeStreaming(
            self.gen(),
            metadata=(
                ("authorization", f"Api-Key {os.getenv('yandex_stt')}"),
            ),
        )
        try:
            for r in it:
                event_type = r.WhichOneof("Event")
                if event_type == "final":
                    self.is_run = False
                    return r.final.alternatives[0].text
                if event_type == 'partial':
                    if r.partial.alternatives:
                        self.start_talk = True
                    elif not self.start_talk and (time.time() - self.start_time) * 10 ** 3 > 5000:
                        self.is_run = False
                        return 'nothing'
        except grpc._channel._Rendezvous as err:
            print(f"Error code {err._state.code}, message: {err._state.details}")
            raise err
    
    def run_vosk(self):
        model = Model('models/vosk-model')
        rec = KaldiRecognizer(model, 16000)
        while True:
            data = self.stream.read(512)
            if rec.AcceptWaveform(data):
                return json.loads(rec.Result())['text']
            else:
                rec.PartialResult()

    def run_google(self):
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()
        with microphone:
            recognized_data = ""
            try:
                audio = recognizer.listen(microphone, timeout=5)
            except speech_recognition.WaitTimeoutError:
                return 'nothing'
            try:
                recognized_data = recognizer.recognize_google(audio, language="ru-RU").lower()
            except speech_recognition.UnknownValueError:
                return 'nothing'
            except speech_recognition.RequestError:
                return 'Interner disconnect'
            return recognized_data
    
    def convert(self):
        stt = settings.get('stt')
        if stt == "yandex":
            p = pyaudio.PyAudio()
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=512
            )
            return self.run_yandex()
        elif stt == "vosk":
            p = pyaudio.PyAudio()
            self.stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=512
            )
            return self.run_vosk()
        elif stt == "google":
            res = self.run_google()
            return res
