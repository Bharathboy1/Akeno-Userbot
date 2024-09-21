FROM rendyprojects/python:latest

# Set the working directory
WORKDIR /app
WORKDIR /.cache

# Install system dependencies
RUN apt -qq update && apt -qq install -y --no-install-recommends \
    ffmpeg curl git gnupg2 unzip wget xvfb libxi6 libgconf-2-4 libappindicator3-1 \
    libxrender1 libxtst6 libnss3 libatk1.0-0 libxss1 fonts-liberation libasound2 \
    libgbm-dev libu2f-udev libvulkan1 libgl1-mesa-dri xdg-utils python3-dev \
    python3-pip libavformat-dev libavcodec-dev libavdevice-dev libavfilter-dev \
    libavutil-dev libswscale-dev libswresample-dev chromium chromium-driver \
    neofetch && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt -fqqy install && \
    rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip -o /tmp/chromedriver.zip -d /usr/bin/ && \
    rm /tmp/chromedriver.zip

# Set Chrome environment variables
ENV CHROME_DRIVER /usr/bin/chromedriver
ENV CHROME_BIN /usr/bin/google-chrome-stable

# Copy application files and install Python dependencies
COPY . .
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools==59.6.0
RUN pip3 install -r requirements.txt

# Set permissions for the app and cache
RUN mkdir -p /app /.cache && chown -R 1000:0 /app /.cache && chmod -R 777 /app /.cache

# Download and set up FFmpeg
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz && \
    wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5 && \
    md5sum -c ffmpeg-git-amd64-static.tar.xz.md5 && \
    tar xvf ffmpeg-git-amd64-static.tar.xz && \
    mv ffmpeg-git*/ffmpeg ffmpeg-git*/ffprobe /usr/local/bin/

# Expose the port the app runs on
EXPOSE 7860

# Start the server using supervisord to manage multiple processes
CMD ["bash", "-c", "python3 server.py & python3 -m Akeno"]
