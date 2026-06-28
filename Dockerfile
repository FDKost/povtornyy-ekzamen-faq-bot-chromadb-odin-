# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==$POETRY_VERSION"

# Set work directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy source code
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY .env.example /app/.env

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
