import requests
from enum import Enum

class Mimic3Voices(Enum):
    ALICE = 'en_US/vctk_low#p239'

class Mimic3AudioFetcher():
    def __init__(self, voice = Mimic3Voices.ALICE, serverurl='localhost',port=59125) -> None:
        self.voice = voice
        self.url=serverurl
        self.port = port
    
    def changeVoice(self, voice):
        if voice.upper() in list(map(lambda x: x.name, Mimic3Voices)):
            self.voice = Mimic3Voices[voice.upper()].value
    
    def fetchAudio(self,text,filename, sufix=''):
        if sufix:
            text +=sufix
        audio = requests.post(f'http://{self.url}:{self.port}/api/tts?voice={self.voice}',data=text)
        with open(f'{filename}.wav','wb') as f:
            f.write(audio.content)
