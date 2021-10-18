import os
import discord
from discord.ext import commands
from text import *
import random

from music_bot import Music

TOKEN = 'ODk4MTI4MzI0OTE4OTExMDA3.YWftLw.rXuIKU2KP-8cAST3Siplb4IL7E4'

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

DEFAULT_ROLE = None

@bot.command()
async def 동전던지기(ctx):
    if random.randrange(0, 2)==0:
        await ctx.send('**앞면**이다.')
    else:
        await ctx.send('**뒷면**이다.')
    return

@bot.command()
async def 역할(ctx, *arg):
    global DEFAULT_ROLE

    if arg[0] == '기본':
        temp = [discord.utils.get(ctx.guild.roles, name=n) for n in arg[1:]]
        role = list(filter(lambda x: x != None, temp))
        if len(role) == 0:
            await ctx.send('설정 실패 : 그런 이름의 역할은 없는데')
        else:
            DEFAULT_ROLE = role
            s = ', '.join([r.name for r in role])
            await ctx.send(f'설정 완료 : 이제 자동으로 새로운 멤버한테 **[{s}]** 역할 줌')
            for guild in bot.guilds:
                for member in guild.members:
                    if len(member.roles) == 1:
                        for r in DEFAULT_ROLE:
                            await member.add_roles(r)
    elif arg[0] == '추가':
        role = discord.utils.get(ctx.guild.roles, name=arg[1])
        temp = [discord.utils.get(ctx.guild.roles, name=n) for n in arg[2:]]
        role_add = list(filter(lambda x: x!=None, temp))
        miss = len(temp) - len(role_add)
        if (role == None):
            await ctx.send('설정 실패 : 그런 이름의 역할은 없는데')
        else:
            s = ', '.join([r.name for r in role_add])
            await ctx.send(f'설정 완료 : **[{role.name}]** 역할인 멤버한테 **[{s}]** 역할도 줌')
            for guild in bot.guilds:
                for member in guild.members:
                    if role in member.roles:
                        for r in role_add:
                            await member.add_roles(r)

    elif arg[0] == '삭제':
        role = discord.utils.get(ctx.guild.roles, name=arg[1])
        temp = [discord.utils.get(ctx.guild.roles, name=n) for n in arg[2:]]
        role_del = list(filter(lambda x: x != None, temp))
        miss = len(temp) - len(role_del)
        if (role == None):
            await ctx.send('설정 실패 : 그런 이름의 역할은 없는데')
        else:
            s = ', '.join([r.name for r in role_del])
            await ctx.send(f'설정 완료 : **[{role.name}]** 역할인 멤버한테서 **[{s}]** 역할 뺏어옴')
            for guild in bot.guilds:
                for member in guild.members:
                    if role in member.roles:
                        for r in role_del:
                            if r in member.roles:
                                await member.remove_roles(r)

@bot.event
async def on_member_join(member):
    for r in DEFAULT_ROLE:
        await member.add_roles(r)


@bot.event
async def on_member_update(before, after):
    pass

@bot.event
async def on_user_update(before, after):
    print('user update')

@bot.event
async def on_message(message):
    username = message.author.name
    user_message = str(message.content)
    channel = message.channel
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if user_message in HI:
        await channel.send('ㅎㅇ')
        return
    if user_message in BYE:
        await channel.send('ㅂㅇ')
        return
    if user_message in LAUGH:
        await channel.send('ㅋ'*random.randint(3, 7))
        return
    if user_message in MY_NAME:
        await channel.send('ㅇ?')
    await bot.process_commands(message)



bot.add_cog(Music(bot))
bot.run(TOKEN)