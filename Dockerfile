FROM debian:latest

# Install dependencies and ttyd
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    libjson-c-dev \
    libwebsockets-dev \
    && git clone https://github.com/tsl0922/ttyd.git \
    && cd ttyd && mkdir build && cd build \
    && cmake .. && make && make install

# Set working directory
WORKDIR /root

# Expose port for web access
EXPOSE 7681

# Command to start ttyd with /bin/bash
CMD ["ttyd", "-p", "7681", "/bin/bash"]
