FROM python:3.11-buster as builder

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.6.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml README.md poetry.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

RUN curl -L https://github.com/golang-migrate/migrate/releases/download/v4.16.2/migrate.linux-amd64.tar.gz | tar xvz

FROM python:3.11-slim-buster as runtime
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /app/migrate /app/migrate
COPY fast_todo ./fast_todo
COPY database ./database
COPY docker ./docker


ENTRYPOINT ["/app/docker/start.sh"]