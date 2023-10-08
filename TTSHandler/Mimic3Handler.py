import requests
from enum import Enum

class Mimic3Voices(Enum):
    ALICE = 'en_US/vctk_low#p239'
    RAIN = 'en_US/vctk_low#p250'
    STEVEN = 'en_US/vctk_low#p259'
    DOUG = 'en_US/vctk_low#p263'
    MARY = 'en_US/vctk_low#p283'
    DORY = 'en_US/vctk_low#p276'
    JOHN = 'en_US/vctk_low#p270'
    ALAN = 'en_UK/apope_low'



class Mimic3AudioFetcher():
    def __init__(self, voice = Mimic3Voices.ALICE.value, serverurl='localhost',port=59125) -> None:
        self.voice = voice
        self.url=serverurl
        self.port = port
    
    def changeVoice(self, voice):
        print(f"Trying to change into voice {voice}")
        if voice.upper() in list(map(lambda x: x.name, Mimic3Voices)):
            self.voice = Mimic3Voices[voice.upper()].value
    
    def fetchAudio(self,text,filename, sufix=''):
        if sufix:
            text +=sufix
        audio = requests.post(f'http://{self.url}:{self.port}/api/tts?voices={self.voice}',data=text)
        with open(f'{filename}.wav','wb') as f:
            f.write(audio.content)
