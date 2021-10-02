import logging

import discord

import youtube_dl
from discord.ext import commands
from pydantic import BaseSettings
from pydantic.types import SecretStr
from random import choice

from data import WELCOME_MESSAGES, YTDL_OPTIONS, BOT_STATUS

try:
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except Exception:
    logging.error("Failed to load env vars")

# TODO make the bot listen to a specific channel only
# ctx.channel.id in [list of channel IDs] -> check to make bot only listen to specific channels


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr


config = BotConfig()

ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
musicbot = commands.Bot(command_prefix="!")


# EVENTS
@musicbot.event
async def on_ready():
    print("Bot is online")
    logging.info("Bot is online")


@musicbot.event
async def on_disconnect():
    await musicbot.change_presence(activity=discord.Game(BOT_STATUS.OFFLINE))
    logging.info("Bot disconnecting")


# COMMANDS
@musicbot.command(name="join", help="Join your channel")
async def join(ctx):
    await ctx.send(choice(WELCOME_MESSAGES))


@musicbot.command(name="play", help="Plays audio, or adds it to the queue if something is playing")
async def play(ctx):
    await join(ctx)


@musicbot.command(name="pause", help="Pauses the current audio")
async def pause(ctx):
    pass


@musicbot.command(name="disconnect", help="Disconnect the bot from the server")
async def disconnect(ctx):
    pass


@musicbot.command(name="skip", help="Skip The current audio")
async def skip(ctx):
    pass


@musicbot.command(name="clear", help="Clear the queue")
async def clear(ctx):
    pass


@musicbot.command(name="ping", help="Check latency of the bot")
async def ping(ctx):
    await ctx.send(f'Latency: {round(musicbot.latency*1000)}ms')


@musicbot.command(name="hoya", help="Ask for a hoooooooyaaaaaa")
async def hoya(ctx):
    # TODO pause playback and give a random hoya from a collection of hoyas?
    pass

musicbot.run(config.BOT_TOKEN.get_secret_value())