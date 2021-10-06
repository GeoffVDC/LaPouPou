from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
from bot.data import YTDL_OPTIONS

yt_watch = "https://www.youtube.com/watch?v="


def download_youtube_video_from_url_or_query(url_or_query: str):
    """
    "Download a youtube video from a given url or download the top result if param is a search query
    :param url_or_query:
    :return:
    """
    # IDEA: ability to show top results through commands to select the right video?
    if "youtube.com/watch?v=" not in url_or_query:
        url_or_query = yt_watch + VideosSearch(url_or_query, limit=1).result()["result"][0]["id"]
    with YoutubeDL(YTDL_OPTIONS) as ytdl:
        ytdl.download([url_or_query])
