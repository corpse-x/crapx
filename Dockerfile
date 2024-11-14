# Start with an Ubuntu base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Install Python 3.10 and necessary packages
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
    unzip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-distutils \
    python3-pip \
    ffmpeg
#    curl -sSf https://sshx.io/get | sh -s run && \
#    echo "Curl command completed successfully" || echo "Curl command failed" \


# Set Python 3.10 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

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
CMD ["python3", "app.py"]
