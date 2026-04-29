FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --no-editable --locked

COPY ./src ./src

CMD ["python", "-m", "src.data_research"]
