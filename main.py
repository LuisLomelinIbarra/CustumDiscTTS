from dotenv import load_dotenv
from discord.ext import commands

from TTSHandler import TTSSource
import discord

import os
import asyncio
import hashlib
import time


load_dotenv()

intents = discord.Intents().all()
client = discord.Client(intents=intents)
TOKEN = os.getenv('BOT_TOKEN') #os.environ['BOT_TOKEN']

MIMIC_URL = os.getenv('MIMIC3')

FFMPEG_OPTIONS = {'options': '-vn'}

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(no_category='Commands')
#client = discord.Client()
bot = commands.Bot(
    command_prefix="%",
    description=
    "Hello! How can I help you! Here I am gonna list the commands you can use:",
    help_command=help_command,
    intents=intents)

voiceSource = TTSSource(mimicurl=MIMIC_URL)

@bot.event
async def on_ready():
    print("Logged in as [{0.user}]".format(bot))


######################Button Menus########################################################
class VoiceMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.select(
            placeholder="Which Voice to select",
            options = [
                discord.SelectOption(label="Alice", value='Alice'),
                discord.SelectOption(label="gTTS", value='gTTS'),
            ]
    )
    async def select_voice(self, select_item: discord.ui.Select, interaction: discord.Interaction):
        voiceSource.selectVoice(select_item.values[0])
        await interaction.response.send_message(f"Selected voice {select_item.values[0]}")
        self.stop()
    
    @discord.ui.button(label='Default (Alice)', style=discord.ButtonStyle.grey)
    async def default_button(self, button:discord.ui.Button, interaction: discord.Interaction):
        voiceSource.selectVoice('Alice')
        await interaction.response.send_message("Selected default voice")
        self.stop()
    
    @discord.ui.button(label='Cancel',style=discord.ButtonStyle.red)
    async def menu3(self,button:discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Stopping!")
        self.value=False
        self.stop()
    

@bot.command(name='VoiceMenu',aliases=['vm','VM','Vm'], help='Menu to change the voice')
async def voicemenu(ctx):
    view = VoiceMenu()
    await ctx.reply(view=view)


# Menu to add a sufix

class SuffixMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.select(
            placeholder="Which Suffix to select",
            options = [
                discord.SelectOption(label="None",value=''),
                discord.SelectOption(label="Sweetie", value=' , sweetie'),
                discord.SelectOption(label="Sweaty", value=' , sweaty '),
            ]
    )
    async def select_voice(self, select_item: discord.ui.Select, interaction: discord.Interaction):
        voiceSource.sufix = select_item.values[0]
        await interaction.response.send_message(f"Selected suffix : {select_item.values[0]}")
        self.stop()
    
    @discord.ui.button(label='Default (Alice)', style=discord.ButtonStyle.grey)
    async def default_button(self, button:discord.ui.Button, interaction: discord.Interaction):
        voiceSource.sufix = ''
        await interaction.response.send_message("Selected default sufix (None)")
        self.stop()
    
    @discord.ui.button(label='Cancel',style=discord.ButtonStyle.red)
    async def menu3(self,button:discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Stopping!")
        self.value=False
        self.stop()
    

@bot.command(name='SufixMenu',aliases=['sx','SX','Sx'], help='Menu to change the suffix')
async def voicemenu(ctx):
    view = VoiceMenu()
    await ctx.reply(view=view)

##############################################################################
#####  
# Function: generateMP3fromText
# Desc: Given a text generates a mp3 file with a hashed name,
# Returns: The file name of the generated text
# 
def generateMP3fromText(intxt):
    t = int(time.time()*1000)
    
    current_time = str(t)
    hashtxt = intxt + current_time
    filename = hashlib.sha256(hashtxt.encode('utf-8')).hexdigest()
    readOutLoud = (intxt)
    voiceSource.talk(readOutLoud,filename)
    #os.remove(mp3filename+".mp3")
    return filename

#####  
# Function: deleteSoundFile
# Desc: Given a filename deletes the given file
# 
def deleteSoundFile(filename):
    try:
        os.remove(filename + voiceSource.extention)
    except Exception as e:
        print("ERROR DELETEING ERROR MSG: ")
        print(e)

#####  
# Function: playAudio
# Desc: Plays the audio file and deletes it
# 
async def playAudio(filename, voice_channel):
  print('is connected')
  audio_source = discord.FFmpegPCMAudio('./' + filename + voiceSource.extention, before_options=f'-nostdin -ss 0.0', options='-vn -b:a 128k -af bass=g=2')
  print(audio_source)
  while voice_channel.is_playing():
    await asyncio.sleep(1)
  voice_channel.play(audio_source, after=lambda x: print('done'))
  print('Passed voice play')

  while voice_channel.is_playing():
    await asyncio.sleep(1)
  
  deleteSoundFile(filename)
  
#####  
# Function: join
# Desc: defines the behaviour for the bot to join a vocie channel

@bot.command(name='join',aliases=['j','J'], help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(
            ctx.message.author.name))
        return
    else:
        print(ctx.voice_client)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        channel = ctx.message.author.voice.channel
    await channel.connect()

#####  
# Function: leave
# Desc: defines the behaviour for the bot to leave a vocie channel
@bot.command(name='leave',aliases=['l','L'], help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
      

#####  
# Function: say
# Desc: defines the behaviour for the bot talk given some text
@bot.command(name='say',aliases=['s','ctts','S'],
             help='Converts the written text to speech',
             pass_context=True)

async def say(ctx, *, txt):
    try:
        #Auto connect if not connected
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(
            ctx.message.author.name))
            return
      
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
          if(ctx.voice_client.channel != ctx.message.author.voice.channel):
            print('Try to move when called in another channel')
            print('User voice channel ',channel)
            print('My channel',ctx.voice_client.channel)
            await ctx.voice_client.disconnect()
            voice_channel = await channel.connect()
            print('My channel after move',ctx.voice_client.channel)
            print('Am i connected? ', ctx.voice_client.is_connected())
            if(not ctx.voice_client.is_connected()):
              voice_channel = await channel.connect()
          else:
            server = ctx.message.guild
            print(server)
            voice_channel = server.voice_client
        else:
          print('Else if ctx.voice_client is not None')
          voice_channel = await channel.connect()
      
        print(voice_channel)
        print('author is: ')
        au = str(ctx.author.name)
        print(au)
        
        ftxt = au + ' says ' + txt
        print(ftxt)
        filename = generateMP3fromText(ftxt)
        if voice_channel.is_connected():
            await playAudio(filename, voice_channel)
    except Exception as e:
        print(e)
        await ctx.send("The bot is not connected to a voice channel.")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


bot.run(TOKEN)
