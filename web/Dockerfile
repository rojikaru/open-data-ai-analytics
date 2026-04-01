FROM ghcr.io/astral-sh/uv:python3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN uv pip install --system \
    fastapi==0.116.1 \
    jinja2==3.1.6 \
    uvicorn==0.35.0

COPY . ./web

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
