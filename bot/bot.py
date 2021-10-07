import logging
from random import choice

import discord
import data
from discord.ext import commands

from config import config

from enums import BOT_STATUS
from utils import get_guild

# TODO make the bot listen to a specific channel only
# ctx.channel.id in [list of channel IDs] -> check to make bot only listen to specific channels
# TODO figure out how to make a queue
# TODO put commands and events each in it's own file
# TODO Split into functionality (music, stats, info, tools, ...)


musicbot = commands.Bot(command_prefix=data.BOT_PREFIX)


# EVENTS
@musicbot.event
async def on_ready():
    print("Bot is online")
    logging.info("Bot is online")


@musicbot.event
async def on_disconnect():
    await musicbot.change_presence(activity=discord.Game(BOT_STATUS.OFFLINE.value))
    logging.info("Bot disconnecting")


# COMMANDS
@musicbot.command(name="join", help=data.HELP_JOIN, description=data.DESCR_JOIN)
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(data.NOT_CONNECTED_MESSAGE)
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send(choice(data.WELCOME_MESSAGES))


@musicbot.command(name="play", help="Plays audio, or adds it to the queue if something is playing")
async def play(ctx, search):
    current_guild = get_guild(musicbot, ctx)



@musicbot.command(name="pause", help="Pauses the current audio")
async def pause(ctx):
    pass


@musicbot.command(name="disconnect",
                  help=f"Leave channel. Also: {' '.join(data.DISCONNECT_ALIASES)}",
                  aliases=data.DISCONNECT_ALIASES)
async def disconnect(ctx):
    if ctx.message.guild.voice_client and ctx.message.guild.voice_client.is_connected():
        await ctx.message.guild.voice_client.disconnect()
    else:
        await ctx.send(data.NOT_CONNECTED_MESSAGE)


@musicbot.command(name="skip", help="Skip The current audio")
async def skip(ctx):
    pass


@musicbot.command(name="stop", help="Stop playback and clear queue")
async def stop(ctx):
    pass


@musicbot.command(name="clear", help="Clear the queue")
async def clear(ctx):
    pass


@musicbot.command(name="ping", help="Check latency of the bot")
async def ping(ctx):
    await ctx.send(f'Latency: {round(musicbot.latency * 1000)}ms')


@musicbot.command(name="hoya", help="Ask for a hoooooooyaaaaaa")
async def hoya(ctx):
    # TODO pause playback and give a random hoya from a collection of hoyas?
    await ctx.send("HOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOYYYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


@musicbot.command(name="settings", help="Change music bot settings")
async def settings(ctx):
    # TODO make stuff like the prefix changeable through commands
    # TODO make a permissions system to only allow certain people to change these or some settings?
    pass


musicbot.run(config.BOT_TOKEN.get_secret_value())
