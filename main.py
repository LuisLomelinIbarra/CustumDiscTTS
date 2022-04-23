from replit import audio
import discord
from discord.ext import commands
import os
import asyncio
import keep_alive
from gtts import gTTS
import hashlib

intents = discord.Intents().all()
client = discord.Client(intents=intents)
TOKEN = os.environ['BOT_TOKEN']

FFMPEG_OPTIONS = {'options': '-vn'}

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(no_category='Commands')
#client = discord.Client()
bot = commands.Bot(
    command_prefix="/",
    description=
    "Hello! How can I help you! Here I am gonna list the commands you can use:",
    help_command=help_command,
    intents=intents)


@bot.event
async def on_ready():
    print("Logged in as [{0.user}]".format(bot))


def generateMP3fromText(intxt):
    mp3filename = hashlib.sha256(intxt.encode('utf-8')).hexdigest()
    readOutLoud = (intxt)
    tts = gTTS(text=readOutLoud, lang='en')
    tts.save(mp3filename + ".mp3")
    #os.remove(mp3filename+".mp3")
    return mp3filename


def deleteSoundFile(filename):
    os.remove(filename + ".mp3")


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(
            ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='say',
             help='Converts the written text to speech',
             pass_context=True)
async def say(ctx, *, txt):
    try:

        print('started the read')
        server = ctx.message.guild
        print(server)
        voice_channel = server.voice_client
        print(voice_channel)
        print('author is: ')
        au = str(ctx.author.name)
        print(au)
        ftxt = au + ' says ' + txt
        print(ftxt)
        filename = generateMP3fromText(ftxt)
        if voice_channel.is_connected():
            print('is connected')
            audio_source = discord.FFmpegPCMAudio('./' + filename + '.mp3', before_options=f'-nostdin -ss 0.0',
                                  options='-vn -b:a 128k -af bass=g=2')
            print(audio_source)
            voice_channel.play(audio_source, after=lambda: print('done'))
            print('Passed voice play')

        while voice_channel.is_playing():
            await asyncio.sleep(1)
        os.remove(filename + ".mp3")
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


keep_alive.keep_alive()
bot.run(TOKEN)
