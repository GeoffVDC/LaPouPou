from enums import SOURCES


def get_guild(bot, command):
    """
    Gets the guild (server) a command belongs to, even via DM
    :return: The guild the command belongs to
    """
    if command.guild is not None:
        return command.guild
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if command.author in channel.members:
                return guild
    return None


def get_source_from_url(url: str) -> SOURCES:
    if "https://www.youtu" in url or "https://youtu.be" in url:
        return SOURCES.YOUTUBE

    if "https://open.spotify.com/track" in url:
        return SOURCES.SPOTIFY

    if "https://open.spotify.com/playlist" in url or "https://open.spotify.com/album" in url:
        return SOURCES.SPOTIFY_PLAYLIST

    return SOURCES.OTHER
