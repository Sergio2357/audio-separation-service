FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app

EXPOSE 80

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]



