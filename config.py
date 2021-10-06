import logging

from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic.types import SecretStr

try:
    load_dotenv(verbose=True)
except:
    logging.error("Failed to load env vars")


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr
    SPOTIFY_CLIENT_ID: SecretStr
    SPOTIFY_SECRET: SecretStr


config = BotConfig()
