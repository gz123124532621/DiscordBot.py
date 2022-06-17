from discord.ext import commands
import discord

token = 'OTY0NTIzNDEyMTEyNDI5MDY2.GP4zVx.tH0KkQZY32tsHIZEoDYEnh4GeVh1C6KRu-Zt28'

intents = discord.Intents.all()
discord.member = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print('Я работаю!')


@bot.event
async def on_member_join(member):
    await member.send(f"Рад что ты теперь с нами {member}!")
    channel = bot.get_channel(967720241511661620)  # channel id 967720241511661620
    role = discord.utils.get(member.guild.roles, id=972542639570321438)  # novice id 972542639570321438
    await member.add_roles(role)
    await channel.send("Теперь ты новичок! Поздравляю тебя!")
# friends id 972536725157064734


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, arg=100):
    await ctx.channel.purge(limit=arg)


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="commands", color=discord.Color.gold())
    emb.set_thumbnail(url="https://english4life.ru/wp-content/uploads/2017/05/help.jpg")
    emb.add_field(name="!help", value="Выводит это сообщение")
    emb.add_field(name="!clear", value="Очищает чат. По стандарту 100 сообщений")
    emb.add_field(name="!kick", value="Исключает пользователя на сервера")
    emb.add_field(name="!ban", value="Блокирует пользователя на сервере")
    emb.add_field(name="!mute", value="Изменяет роль пользователя, не позволяя ему ничего делать на сервере.")
    emb.add_field(name="!unmute", value="Изменяет роль пользователя, возвращает ему роль новичка как следствие он может делать всё что делал до этого")
    emb.add_field(name="!repeat", value="Повторяет сообщение отправителя. Команды не видно.")
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
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    mute = discord.utils.get(ctx.message.guild.roles, name="Mute")
    role = discord.utils.get(member.guild.roles, name="Новичок")
    await member.remove_roles(role)
    await member.add_roles(mute)


@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    novice = discord.utils.get(ctx.message.guild.roles, name="Новичок")
    role = discord.utils.get(member.guild.roles, name="Mute")
    await member.remove_roles(role)
    await member.add_roles(novice)


@bot.command()
async def repeat(ctx, *, arg):
    await ctx.channel.purge(limit=1)
    await ctx.send(arg)


bot.run(token)
