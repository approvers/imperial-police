FROM python:3
USER root
MAINTAINER Colk <iam@colk.dev>

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install discord

RUN apt-get install -y git
RUN apt-get install -y ffmpeg

ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN mkdir /bot
WORKDIR /bot
RUN git clone https://github.com/approvers/imperial-police.git

# CMD ["python3 /bot/imperial-police/main.py"]
