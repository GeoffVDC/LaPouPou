import logging

import youtube_dl
from discord.ext import commands
from pydantic import BaseSettings
from pydantic.types import SecretStr

try:
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except Exception:
    logging.error("Failed to load env vars")


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr


config = BotConfig()


YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

BOT_STATUS = [
    "Offline",
    "Jamming to some tunes",
    "Idle",
]

ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
musicbot = commands.Bot(command_prefix="!")


# EVENTS
@musicbot.event
async def on_ready():
    pass


@musicbot.event
async def on_disconnect():
    pass


# COMMANDS
@musicbot.command(name="play", help="Plays audio, or adds it to the queue if something is playing")
async def play(ctx):
    pass


@musicbot.command(name="pause", help="Pauses the current audio")
async def pause(ctx):
    pass


@musicbot.command(name="join", help="Join your channel")
async def join(ctx):
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
    pass


@musicbot.command(name="hoya", help="Ask for a hoooooooyaaaaaa")
async def hoya(ctx):
    # TODO pause playback and give a random hoya from a collection of hoyas?
    pass

musicbot.run(config.BOT_TOKEN.get_secret_value())