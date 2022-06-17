from discord.ext import commands
import discord
from youtube_dl import YoutubeDL
from asyncio import sleep
from DiscordBotMusicInf import *

intents = discord.Intents.all()
discord.member = True
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

global voice_enter


def play_music(arg):
    with YoutubeDL(YDL_OPTIONS) as y_dl:
        if "https://" in arg:
            info = y_dl.extract_info(arg, download=False)
        else:
            info = y_dl.extract_info(f"ytsearch:{arg}", download=False)["entries"][0]
    url = info["formats"][0]["url"]
    voice_enter.play(discord.FFmpegPCMAudio(executable="music\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!music"))
    print('Я работаю!')


@bot.command()
async def music(ctx, *, arg):
    global voice_enter
    voice_enter = await ctx.message.author.voice.channel.connect()
    play_music(arg)


@bot.command()
async def play_next(ctx, *, arg):
    url_arg.append(arg)

    while len(url_arg) > 0:
        while voice_enter.is_playing() or voice_enter.is_paused():
            await sleep(2)
        else:
            try:
                play_music(arg)
                url_arg.pop(0)
            except IndexError:
                pass
    else:
        await voice_enter.disconnect()


@bot.command()
async def pause_music(ctx):
    voice = discord.utils.get(bot.voice_clients)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Бот уже останавливал музыку =/")


@bot.command()
async def resume_music(ctx):
    voice = discord.utils.get(bot.voice_clients)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Бот уже играет музыку =/")


@bot.command()
async def leave(ctx):
    await voice_enter.disconnect()


@bot.command()
async def skip(ctx):
    voice_enter.stop()
    play_music(url_arg[0])
    url_arg.pop(0)


bot.run(token)
