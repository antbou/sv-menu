FROM python:3-alpine

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* README.md ./

COPY src ./src

RUN poetry install

ENTRYPOINT ["poetry", "run", "sv-menu"]
