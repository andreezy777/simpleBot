FROM python:3

RUN apt-get update

RUN pip3 install pyTelegramBotAPI cherrypy

RUN apt-get install -y sqlite3 

WORKDIR /usr/src/simpleBot

COPY . /usr/src/simpleBot

ENTRYPOINT ["python3"]

CMD [ "bot.py"]
