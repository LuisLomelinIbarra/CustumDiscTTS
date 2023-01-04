
import discord
from discord.ext import commands
import os
import asyncio
import keep_alive
from gtts import gTTS
import hashlib
import time



intents = discord.Intents().all()
client = discord.Client(intents=intents)
TOKEN = os.environ['BOT_TOKEN']

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


@bot.event
async def on_ready():
    print("Logged in as [{0.user}]".format(bot))

#####  
# Function: generateMP3fromText
# Desc: Given a text generates a mp3 file with a hashed name,
# Returns: The file name of the generated text
# 
def generateMP3fromText(intxt):
    t = int(time.time()*1000)
    
    current_time = str(t)
    hashtxt = intxt + current_time
    mp3filename = hashlib.sha256(hashtxt.encode('utf-8')).hexdigest()
    readOutLoud = (intxt)
    tts = gTTS(text=readOutLoud, lang='en') #, tld='ie')
    tts.save(mp3filename + ".mp3")
    #os.remove(mp3filename+".mp3")
    return mp3filename

#####  
# Function: deleteSoundFile
# Desc: Given a filename deletes the given file
# 
def deleteSoundFile(filename):
  try:
    os.remove(filename + ".mp3")
  except Exception as e:
    print("ERROR DELETEING ERROR MSG: ")
    print(e)

#####  
# Function: playAudio
# Desc: Plays the audio file and deletes it
# 
async def playAudio(filename, voice_channel):
  print('is connected')
  audio_source = discord.FFmpegPCMAudio('./' + filename + '.mp3', before_options=f'-nostdin -ss 0.0', options='-vn -b:a 128k -af bass=g=2')
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

keep_alive.keep_alive()
bot.run(TOKEN)
