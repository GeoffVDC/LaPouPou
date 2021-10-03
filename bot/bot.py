import asyncio
import functools
import logging
from random import choice

import discord
import youtube_dl
from discord.ext import commands
from pydantic import BaseSettings
from pydantic.types import SecretStr

from data import WELCOME_MESSAGES, YTDL_OPTIONS, DISCONNECT_ALIASES
from enums import BOT_STATUS

try:
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except:
    logging.error("Failed to load env vars")


# TODO make the bot listen to a specific channel only
# ctx.channel.id in [list of channel IDs] -> check to make bot only listen to specific channels
# TODO figure out how to make a queue
# TODO put commands and events each in it's own file
# TODO Split into functionality (music, stats, info, tools, ...)


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr


# TODO take a look at this and check how other projects do it because the youtube dude doesn't get it
# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)
#
#         self.data = data
#
#         self.title = data.get('title')
#         self.url = data.get('url')
#
#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
#
#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]
#
#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise Exception('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise Exception('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise Exception('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise Exception('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


config = BotConfig()

youtube_dl.utils.bug_reports_message = lambda: ''
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
async def play(ctx, search):
    # TODO figure out how to check if bot is already in channel
    # (create function for checking, use in other commands)
    # (Look at the other bots how they do this)
    # -> Play song if already in channel
    # -> Join channel if not in channel yet and then play song
    # try:
    #     server = ctx.message.guild
    #     voice_channel = server.voice_client
    #     async with ctx.typing():
    #         filename = await YTDLSource.from_url(url, loop=musicbot.loop)
    #         voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    #     await ctx.send('**Now playing:** {}'.format(filename))
    # except Exception as e:
    #     await ctx.send(f"The bot is not connected to a voice channel. ERROR {e}")
    # await join(ctx)
    # if not ctx.message.author.voice:
    #     await ctx.send('you are not connected to a voice channel')
    #     return
    #
    # else:
    #     channel = ctx.message.author.voice.channel
    #
    # voice_client = await channel.connect()
    #
    # # guild = ctx.message.guild
    #
    # with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
    #     file = ydl.extract_info(url, download=True)
    #     path = str(file['title']) + "-" + str(file['id'] + ".mp3")
    #
    # voice_client.play(discord.FFmpegPCMAudio(path))
    # voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
    """Plays a song.
    If there are songs in the queue, this will be queued until the
    other songs finished playing.
    This command automatically searches from various sites if no URL is provided.
    A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
    """
    async with ctx.typing():
        try:
            source = await YTDLSource.create_source(ctx, search, loop=musicbot.loop)
        except Exception as e:
            await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
        else:
            song = Song(source)

            await ctx.voice_state.songs.put(song)
            await ctx.send('Enqueued {}'.format(str(source)))


@musicbot.command(name="pause", help="Pauses the current audio")
async def pause(ctx):
    pass


@musicbot.command(name="disconnect",
                  help=f"Leave channel. Also: {' '.join(DISCONNECT_ALIASES)}",
                  aliases=DISCONNECT_ALIASES)
async def disconnect(ctx):
    if ctx.message.guild.voice_client and ctx.message.guild.voice_client.is_connected():
        await ctx.message.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to a voice channel")


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
