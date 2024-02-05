FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install

COPY ./matte ./matte
COPY ./migrations ./migrations
COPY ./alembic.ini .
COPY ./poll.py .
COPY ./run.py .
COPY ./sample.xml .

CMD ls -al && /bin/bash
