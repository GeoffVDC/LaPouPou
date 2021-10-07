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
    "HOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOYYYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
]

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'videos/%(extractor)s-%(id)s-%(title)s.%(ext)s',
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

FFMPEG_OPTIONS = {'options': '-vn'}

BOT_PREFIX="!"

DISCONNECT_ALIASES = ["leave", "getlost", "fuckoff"]
NOT_CONNECTED_MESSAGE = "You are not in a voice channel. Join a channel to summon me."
HELP_JOIN = "Join your channel"
DESCR_JOIN = "Make the bot join your current voice channel"