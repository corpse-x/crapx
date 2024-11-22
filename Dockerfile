FROM ubuntu:20.04

# Install dependencies and ttyd
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    libjson-c-dev \
    libwebsockets-dev && \
    apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-distutils \
    python3-pip && \
    apt-get clean \
    && git clone https://github.com/tsl0922/ttyd.git \
    && cd ttyd && mkdir build && cd build \
    && cmake .. && make && make install


RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10
# Set working directory
WORKDIR /root

# Expose port for web access
EXPOSE 7681

# Command to start ttyd with /bin/bash
CMD ["ttyd", "-p", "7681", "/bin/bash"]
