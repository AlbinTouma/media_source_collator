# Use the official Python 3.12.4 base image
FROM python:3.12.4-slim

# Install dependencies for Poetry and other tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && /root/.local/bin/poetry config virtualenvs.create false

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set the working directory to /app
WORKDIR /app

# Debug: Check if Poetry is installed correctly
RUN /root/.local/bin/poetry --version

# Copy the pyproject.toml and poetry.lock (if available) into the Docker image
COPY pyproject.toml poetry.lock* /app/

# Install dependencies with Poetry
RUN /root/.local/bin/poetry install --only main

# Copy the rest of the application code into the Docker image
COPY . /app/

# Expose the port Streamlit will run on
EXPOSE 8501

# Define the command to run your Streamlit app
CMD ["streamlit", "run", "Cartier.py"]

