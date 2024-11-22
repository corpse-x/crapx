# Start with an Ubuntu base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Set DEBIAN_FRONTEND to noninteractive to avoid tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive

# Pre-configure tzdata to avoid interactive prompt
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Etc select UTC" | debconf-set-selections

# Install required packages and Python 3.10
RUN apt update && apt install -y \
    software-properties-common \
    curl \
    bash \
    bzip2 \
    git \
    neofetch \
    wget \
    sudo \
    xvfb \
    unzip \
    ffmpeg && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-distutils \
    python3-pip && \
    apt-get clean

# Set Python 3.10 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Upgrade pip to the latest version to avoid internal issues
RUN pip3 install --upgrade pip

# Install html5lib explicitly (in case it is needed for pip internally)
RUN pip3 install html5lib

# Verify Python and pip versions
RUN python3 --version && pip3 --version

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Set the default command to run the application
CMD ["python3", "bot.py"]
