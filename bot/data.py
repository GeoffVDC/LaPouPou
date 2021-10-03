WELCOME_MESSAGES = [
    "¡Hola, bitchitos!",
    "Gutten tag",
    "What is love?",
    "'Sup",
    "Hello",
    "'Ello, mate!",
    "Pip pip cheerio chaps",
    "What's up, bitches",
    "Skkrrrrrrraaaaa",
]

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

FFMPEG_OPTIONS = {
    'options': '-vn',
}

DISCONNECT_ALIASES = ["leave", "getlost", "fuckoff"]
