# Need to store the extension of the file used
from .Mimic3Handler import Mimic3AudioFetcher
from .gTTSHandler import GTTSHandler
class TTSSource:
    


    def __init__(self, engine:str='mimic',mimicurl='localhost') -> None:
        engineDict = {'mimic':Mimic3AudioFetcher, 'gTTS':GTTSHandler}
        extDict = {'mimic':'.wav', 'gTTS':'.mp3'}
        self.selected = engine
        if engine == 'mimic':
            self.engine = engineDict[engine](serverurl=mimicurl)
        else:
            self.engine = engineDict[engine]
        self.extention = extDict[engine]
        self.sufix=''
    
    def selectEngine(self,engine:str='mimic'):
        """Change the TTS engine utilized it defaults to mimic"""

        engineDict = {'mimic':Mimic3AudioFetcher, 'gTTS':GTTSHandler}
        extDict = {'mimic':'.wav', 'gTTS':'.mp3'}
        self.engine = engineDict[engine]()
        self.extention = extDict[engine]
        self.selected = engine
    
    def selectVoice(self,voice='Alice'):
        """Changes the voice in use. It can also change the TTS depending on input"""
        if voice == 'gTTS' and self.selected != 'gTTS':
            self.selectEngine('gTTS')
        elif self.selected != 'mimic' and voice != 'gTTS':
            self.selectEngine()
            self.engine.changeVoice(voice)
        else:
            self.engine.changeVoice(voice)
            

    def talk(self,text,filename):
        self.engine.fetchAudio(text,filename,self.sufix)
