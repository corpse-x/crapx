FROM ubuntu:20.04

# Set DEBIAN_FRONTEND to noninteractive to avoid tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive

# Pre-configure tzdata to avoid interactive prompt
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Etc select UTC" | debconf-set-selections

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    libjson-c-dev \
    libwebsockets-dev \
    software-properties-common \
    && apt-get clean

# Install Python 3.10.8
RUN apt-get update && \
    apt-get install -y gcc zlib1g-dev \
    && wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz \
    && tar xvf Python-3.10.8.tgz \
    && cd Python-3.10.8 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.10.8 Python-3.10.8.tgz

# Install ttyd
RUN git clone https://github.com/tsl0922/ttyd.git \
    && cd ttyd \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install

# Set working directory
WORKDIR /root

# Expose port for web access
EXPOSE 7681

# Start ttyd with /bin/bash
CMD ["ttyd", "-p", "7681", "/bin/bash"]
