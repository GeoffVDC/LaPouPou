FROM
COPY /bot /bot
COPY requirements.txt .
# TODO figure how to install ffmpeg on docker image
# RUN apt-get install ffmpeg
WORKDIR /bot
RUN pip install -r /requirements.txt
# TODO ADD DISCORD BOT TOKEN TO ENV
CMD ["python", "bot.py"]