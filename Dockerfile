FROM python:3.9
COPY /bot /bot
COPY requirements.txt .
WORKDIR /bot
RUN pip install -r /requirements.txt
# TODO ADD DISCORD BOT TOKEN TO ENV
CMD ["python", "bot.py"]