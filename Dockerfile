# Use the base Ubuntu 20.04 image
FROM ubuntu:20.04

# Update and install required dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to /app
COPY requirements.txt .

# Activate the virtual environment and install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of your application to the working directory
COPY . .

EXPOSE 4003

ENTRYPOINT ["python3", "app.py"]
