import asyncio
import logging
from random import choice

import discord
import youtube_dl
from discord.ext import commands
from pydantic import BaseSettings
from pydantic.types import SecretStr

from data import WELCOME_MESSAGES, YTDL_OPTIONS, BOT_STATUS, FFMPEG_OPTIONS

try:
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except Exception:
    logging.error("Failed to load env vars")


# TODO make the bot listen to a specific channel only
# ctx.channel.id in [list of channel IDs] -> check to make bot only listen to specific channels


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


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
    await musicbot.change_presence(activity=discord.Game(BOT_STATUS.OFFLINE.value))
    logging.info("Bot disconnecting")


# COMMANDS
@musicbot.command(name="join", help="Join your channel")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not in a voice channel. Join a channel to summon me.")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send(choice(WELCOME_MESSAGES))


@musicbot.command(name="play", help="Plays audio, or adds it to the queue if something is playing")
async def play(ctx):
    await join(ctx)


@musicbot.command(name="pause", help="Pauses the current audio")
async def pause(ctx):
    pass


@musicbot.command(name="disconnect", help="Disconnect the bot from the server")
async def disconnect(ctx):
    await ctx.message.guild.voice_client.disconnect()


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
    pass


musicbot.run(config.BOT_TOKEN.get_secret_value())
