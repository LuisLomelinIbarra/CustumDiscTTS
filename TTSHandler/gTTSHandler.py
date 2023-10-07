from gtts import gTTS

class GTTSHandler:

    def fetchAudio(self,readOutLoud, mp3filename,sufix=''):
        tts = gTTS(text=readOutLoud+sufix, lang='en') #, tld='ie')
        tts.save(mp3filename + ".mp3")
        
    def changeVoice(self):
        pass