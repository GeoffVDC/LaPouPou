from enum import Enum


class BOT_STATUS(Enum):
    OFFLINE = "Offline"
    PLAYING = "Jamming to some tunes"
    ONLINE = "Online"


class SOURCES(Enum):
    SPOTIFY = "Spotify"
    SPOTIFY_PLAYLIST = "Spotify Playlist"
    YOUTUBE = "Youtube"
    OTHER = "Other"