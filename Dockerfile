FROM python:3.9-slim
COPY requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN apt-get -y update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    pip install --no-cache-dir -r /bot/requirements.txt && \
    rm -rf /var/lib/apt/lists/*
# TODO ADD DISCORD BOT TOKEN TO ENV
WORKDIR /bot
COPY ./bot /bot
CMD ["python", "bot.py"]