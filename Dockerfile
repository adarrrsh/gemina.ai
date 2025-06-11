# Use official Python slim image
FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install system dependencies required by Manim, Whisper, etc.
RUN apt-get update && \
    apt-get install -y ffmpeg libcairo2-dev pkg-config git && \
    apt-get clean

# Copy requirements and install Python packages
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project into the image
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]

