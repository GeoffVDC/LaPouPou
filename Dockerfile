FROM python:3.9-slim
COPY /bot requirements.txt /bot/
# TODO figure how to install ffmpeg on docker image
# RUN apt-get install ffmpeg
WORKDIR /bot
RUN apt-get -y update \
    && apt-get install -y ffmpeg \
    && pip install -r /bot/requirements.txt
# TODO ADD DISCORD BOT TOKEN TO ENV
CMD ["python", "bot.py"]