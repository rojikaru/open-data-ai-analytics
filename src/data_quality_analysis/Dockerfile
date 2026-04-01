FROM ghcr.io/astral-sh/uv:python3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN uv sync --frozen --no-dev --no-editable --locked --system

COPY . ./src

CMD ["python", "-m", "src.data_quality_analysis"]
