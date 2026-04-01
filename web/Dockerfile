FROM ghcr.io/astral-sh/uv:python3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN uv sync --frozen --no-dev --no-editable --locked --system

COPY . ./web

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
