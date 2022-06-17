from discord.ext import commands
import string
import discord
from discord import utils
from BotDiscord.DisBotInf import *

intents = discord.Intents.all()
discord.member = True
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")
global voice_enter


# События бота.


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
    print('Я работаю!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Ты чё неправильно пишешь?А?")
    else:
        print(error)
    # pass


@bot.event
async def on_message(message):
    for i in message.content.split(" "):
        i = i.lower().translate(str.maketrans("", "", string.punctuation))
        for mat in mats:
            if i == mat:
                await message.delete()
                await message.channel.send(f"А так говорить плохо! {message.author.mention}")
                role = discord.utils.get(message.author.guild.roles, name="Новичок")
                ban_mute = discord.utils.get(message.author.guild.roles, name="Mute")
                await message.author.remove_roles(role)
                await message.author.add_roles(ban_mute)
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await member.send(f"Рад что ты теперь с нами {member}!")
    channel = on_member_join_channel
    role = discord.utils.get(member.guild.roles, id=on_member_join_role)
    await member.add_roles(role)
    await channel.send("Теперь ты новичок! Поздравляю тебя!")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == message_id:
        channel = bot.get_channel(payload.channel_id)  # получаем id канала через payload
        message = await channel.fetch_message(payload.message_id)  # получаем(отлавливаем) сообщение через payload
        member = utils.get(message.guild.members,
                           id=payload.user_id)  # получаем всех пользователей, получаем id пользователя оставившего реакцию
        emoji = str(payload.emoji)  # строковое значение emoji
        try:
            role = utils.get(message.guild.roles, id=roles[emoji])  # получаем все роли и получаем список id emoji

            print(member.roles[1])
            print(type(member.roles[0]))
            if max_roles > len([i for i in member.roles if i.id not in no_max_roles_roles]):
                await member.add_roles(role)
            else:
                await message.remove_reaction(payload.emoji, member)

        except KeyError as e:
            await message.remove_reaction(emoji, member)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == message_id:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        emoji = str(payload.emoji)
        try:
            role = utils.get(message.guild.roles, id=roles[emoji])
            await member.remove_roles(role)
        except KeyError as e:
            pass
        except UnboundLocalError as ee:
            pass


# Команды бота.


@bot.command()
async def kak(ctx, arg=None):
    if arg is None:
        await ctx.send("Как дела?")
    elif arg == 'dela':
        await ctx.send("Как дела?2")
    elif arg == 'nastroenie':
        await ctx.send("Как настроение?")
    else:
        await ctx.send("Что-то не так?")


@bot.command()
@commands.has_permissions(administrator=True)
async def privet(ctx, *, arg):
    await ctx.send(arg)


@privet.error
async def privet_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Недостаточно введённых данных.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Недостаточно прав.")
    else:
        print(error)
        await ctx.send(error)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, arg=100):
    await ctx.channel.purge(limit=arg)


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="commands", color=discord.Color.gold())
    emb.set_thumbnail(url="https://english4life.ru/wp-content/uploads/2017/05/help.jpg")
    emb.add_field(name="!kak", value="Данная функция спрашивает у вас как ваши дела и настроение")
    emb.add_field(name="!help", value="Выводит это сообщение")
    emb.add_field(name="!httintel", value="Выводит сообщение")
    emb.add_field(name="!music", value="При вводе ссылки или названия видео возможно прослушивание аудио.")
    emb.add_field(name="alpha_resume_music_bot", value="При вводе возобновляет остановленную музыку.")
    emb.add_field(name="alpha_pause_music_bot", value="При вводе останавливает музыку.")
    await ctx.send(embed=emb)


@bot.command()
async def adminhelp(ctx):
    emb = discord.Embed(title="Admin commands", color=discord.Color.blurple())
    emb.set_thumbnail(url="https://english4life.ru/wp-content/uploads/2017/05/help.jpg")
    emb.add_field(name="!privet", value="Эта функция повторяет написанные вами слова")
    emb.add_field(name="!clear", value="Очищает чат")
    emb.add_field(name="!kick", value="Исключает пользователя на сервера")
    emb.add_field(name="!ban", value="Блокирует пользователя на сервере")
    emb.add_field(name="!mute", value="Изменяет роль пользователя, не позволяя ему ничего делать на сервере.")
    emb.add_field(name="!unmute",
                  value="Изменяет роль пользователя, возвращает ему роль новичка как следствие он может делать всё что делал до этого")
    await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="Был кикнут пользователь", color=discord.Color.blurple(),
                          url="https://media.istockphoto.com/photos/fighting-guy-in-black-kimono-fighter-shows-kudo-technique-on-studio-picture-id1300003148?k=20&m=1300003148&s=612x612&w=0&h=7VS3LElnAsPdlJOH7deJ1b1Xk2A0fGEXuoeMv9C9fS4=")
    embed.add_field(name="Кикнут пользователь", value=f"{member.mention}, был удалён/а из группы!")
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="Причина не указана"):
    await member.ban(reason=reason)
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="Был заблокирован пользователь", color=discord.Color.blurple(),
                          url="https://st3.depositphotos.com/1005979/14240/i/600/depositphotos_142402140-stock-photo-banned-stamp-red-round.jpg")
    embed.add_field(name="Заблокирован пользователь", value=f"{member.mention}, был забанен за {reason}")
    await ctx.send(embed=embed)


@bot.command()
async def httintel(ctx):
    embed = discord.Embed(title='Немного об "intel"', color=discord.Color.blurple(),
                          url="https://ark.intel.com/content/www/ru/ru/ark.html")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.set_footer(text="H2", icon_url=ctx.author.avatar_url)
    embed.set_image(url="https://s3-symbol-logo.tradingview.com/intel--600.png")
    embed.set_thumbnail(url=(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Intel_logo_%282006-2020%29.svg/220px-Intel_logo_%282006-2020%29.svg.png"))
    embed.add_field(name="H1", value="Text")
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    ban_mute = discord.utils.get(ctx.message.guild.roles, name="Mute")
    role = discord.utils.get(member.guild.roles, name="Новичок")
    await member.remove_roles(role)
    await member.add_roles(ban_mute)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Был вписан пользователь которого не существует.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Недостаточно прав. Зачем вы вообще пытались?")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Недостаточно данных.")
    else:
        print(error)
        await ctx.send(error)
        await ctx.send("Вы сделали что-то не так :/")


@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    novice = discord.utils.get(ctx.message.guild.roles, name="Новичок")
    role = discord.utils.get(member.guild.roles, name="Mute")
    await member.remove_roles(role)
    await member.add_roles(novice)


bot.run(token)

# #NoBranch
