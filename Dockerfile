FROM python:3.8.8-slim
USER root
MAINTAINER Colk <iam@colk.dev>

ENV LC_ALL=en_US.UTF-8 \
    TZ=JST-9 \
    TERM=xtermdocker-attachingdocker-attaching

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    locales ffmpeg \
    && apt-get upgrade -y \
    && localedef -f UTF-8 -i en_US en_US.UTF-8 \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools

COPY ./ /deploy/imperial-police

WORKDIR /deploy/imperial-police
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv \
    && pipenv sync --system --dev

CMD ["python","main.py"]
