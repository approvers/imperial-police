FROM python:3.8.8
USER root
MAINTAINER Colk <iam@colk.dev>

RUN apt-get update \
&& apt-get -y install locales \
&& apt-get install -y ffmpeg \
&& apt-get install -y --no-install-recommends \
&& apt-get -y clean \
&& rm -rf /var/lib/apt/lists/*

ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xtermdocker-attachingdocker-attaching
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN pip install --upgrade pip && pip install --upgrade setuptools

RUN mkdir /deploy/
COPY ./ /deploy/imperial-police

WORKDIR /deploy/imperial-police
RUN pip install -r requirements.txt

CMD ["python3","/deploy/imperial-police/main.py"]
