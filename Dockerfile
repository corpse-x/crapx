FROM python:3.8-slim-buster
WORKDIR /app

RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    bash \
    bzip2 \
    curl \
    figlet \
    git \
    neofetch \
    wget \
    sudo \
    ffmpeg \
    xvfb \
    unzip \
    && ls


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 app.py
