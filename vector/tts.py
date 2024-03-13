import io
import grpc
import pydub
import cloudapi.output.yandex.cloud.ai.tts.v3.tts_pb2 as tts_pb2
import cloudapi.output.yandex.cloud.ai.tts.v3.tts_service_pb2_grpc as tts_service_pb2_grpc
import playsound
import vector.settings as settings
import dotenv
import os
import pyttsx3
dotenv.load_dotenv('.env')


class Tts:
    def talk(self, text):
        if settings.get('tts') == 'yandex':
            audio = self.synthesize_yandex(os.getenv('yandex_tts'), text)
            with open('sounds/res.wav', 'w+') as f:
                audio.export('sounds/res.wav', format='wav')
            playsound.playsound('sounds/res.wav', block=False)
        else:
            self.synthesize_silero(text)

    def synthesize_yandex(self, iam_token, text):
        request = tts_pb2.UtteranceSynthesisRequest(
            text=text,
            output_audio_spec=tts_pb2.AudioFormatOptions(
                container_audio=tts_pb2.ContainerAudio(
                    container_audio_type=tts_pb2.ContainerAudio.WAV
                )
            ),
            loudness_normalization_type=tts_pb2.UtteranceSynthesisRequest.LUFS,
            hints=[
                tts_pb2.Hints(voice=settings.get('yandex_speaker')),
                tts_pb2.Hints(speed=1.2)
            ],
            unsafe_mode=True
        )
        cred = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel('tts.api.cloud.yandex.net:443', cred)
        stub = tts_service_pb2_grpc.SynthesizerStub(channel)
        it = stub.UtteranceSynthesis(request, metadata=(
            ('authorization', f'Api-Key {iam_token}'),
        ))
        try:
            audio = io.BytesIO()
            for response in it:
                audio.write(response.audio_chunk.data)
            audio.seek(0)
            return pydub.AudioSegment.from_wav(audio)
        except grpc._channel._Rendezvous as err:
            print(f'Error code {err._state.code}, message: {err._state.details}')
            raise err

    def synthesize_silero(self, text):
        s = pyttsx3.init()
        s.setProperty('voice', 'russian')
        s.say(text)
        s.runAndWait()
