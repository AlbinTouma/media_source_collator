FROM python:3.12.4-slim

#Install poetry dependencies
RUN apt-get update && apt-get install -y \
  curl \
  build-essential
  && rm -rf /var/lib/apt/list/*

# Install poetry
RUN PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

#Install libs with Poetry
RUN poetry install --no-root --no-dev

COPY . /app/

EXPOSE 8501

CMD ["streamlit", "run", "interface.py"]

