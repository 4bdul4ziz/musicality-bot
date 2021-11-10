
'''Musicality. A music bot made with pain.''' 

from inspect import Arguments
import random
from subprocess import TimeoutExpired
import sys
import traceback
from urllib.request import urlretrieve
from discord.message import PartialMessage
import youtube_dl
from youtube_dl import YoutubeDL
import discord
import asyncio
import itertools
from webserver import keep_alive
import os

from discord import player
from discord.utils import get 
from discord import FFmpegPCMAudio
from discord import member
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import check



TOKEN = ''



client = commands.Bot(command_prefix='-')
client.remove_command('help')

client.lava_nodes = [
  {
    'host': 'lava.link',
    'port': 80,
    'rest_uri': f'http://lava.link:80',
    'identifier': 'MAIN',
    'password': 'nothing',
    'region': 'singapore'
  }
]


@client.event
async def on_ready():
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1

    await client.change_presence(status=discord.Status.idle, activity = discord.Activity(
        type = discord.ActivityType.watching,
        name = f'{servers} servers and {members} members'
    ))
    print("\nDue to unfortunate circumstances, I'm alive.")
    client.load_extension('dismusic')
    client.load_extension('dch')



@client.command()
async def ping(ctx):
    await ctx.send(f"The current latency is: {round(client.latency * 1000)}ms")

@client.command(aliases=['8ball', 'fortune'])
async def _8ball(ctx, *, question):
    responses = ['No, go away.',
                'Yesn\'t',
                'You really think that is possible?',
                'Ye.',
                'Maybe.',
                'Not for long.',
                'As long as I am alive, no.',
                'In your dreams.',
                'Probably.',
                'Perhaps?',
                'Not once in a million years.',
                'My sources says no.',
                'Without a doubt.',
                'No.',
                'Joe mama.',
                'Deez nuts!'
                ]

    await ctx.send(f'{random.choice(responses)}')

@client.command()
async def purge(ctx, amount : int):
    def is_me(m):
        return m.author == client.user
    deleted = await ctx.channel.purge(limit=amount, check=is_me)
    await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please mention the amount of messages to delete.')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.purple()
    )
    embed.set_author(name='List of Commands\n')
    embed.set_footer(text='Incase of additional support required, contact Unicorn✨ #9779', icon_url='https://cdn.discordapp.com/attachments/887837042652897323/888168246153474108/3a67ac9349717.56323aac30ee4.jpg')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/887837042652897323/888168296883568660/PngItem_719553.png')
    embed.set_image(url='https://cdn10.phillymag.com/wp-content/uploads/sites/3/2014/11/help-pink.png')
    embed.add_field(name='-ping', value='Returns the bot latency.', inline=False)
    embed.add_field(name='-play', value='Adds a song onto the queue.', inline=False)
    embed.add_field(name='-pause', value='Pauses the current song playing.', inline=False)
    embed.add_field(name='-np', value='Displays the current song playing.', inline=False)
    embed.add_field(name='-queue', value='Displays the current queued songs.', inline=False)
    embed.add_field(name='-purge', value='Purges the bot\'s message, based on the argument given.', inline=False)
    embed.add_field(name='-8ball', value='Predicts the future.', inline=False)

    await ctx.send(embed=embed)

#calculator    

@client.command() 
async def add(ctx, *nums):
    operation = " + ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def sub(ctx, *nums): 
    operation = " - ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def multiply(ctx, *nums): 
    operation = " * ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')

@client.command() 
async def divide(ctx, *nums): 
    operation = " / ".join(nums)
    await ctx.send(f'{operation} = {eval(operation)}')


#reminder

from datetime import datetime

datetime.utcnow()

@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please DM Unicorn✨ #9779", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 60:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)
 

'''
@client.command(aliases=['summon', 'connect'])
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

@client.command(aliases=['disconnect', 'goaway', 'pissoff', 'exit'])
async def leave(ctx):
    await ctx.voice_client.disconnect()

'''

keep_alive()

client.run(TOKEN)