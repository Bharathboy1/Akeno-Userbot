FROM rendyprojects/python:latest

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt -qq update && apt -qq install -y --no-install-recommends \
    ffmpeg curl git python3-dev python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application files and install Python dependencies
COPY . . 
COPY requirements.txt . 
RUN pip3 install --upgrade pip setuptools==59.6.0
RUN pip3 install -r requirements.txt

# Set permissions for the app
RUN chown -R 1000:0 /app && chmod -R 777 /app

# Expose the port the app runs on
EXPOSE 7860

# Start the server
CMD ["bash", "-c", "python3 server.py & python3 -m Akeno"]
