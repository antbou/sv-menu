FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* README.md ./

COPY src ./src

RUN poetry install

ENTRYPOINT ["poetry", "run", "sv-menu"]
