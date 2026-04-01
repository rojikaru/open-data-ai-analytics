FROM ghcr.io/astral-sh/uv:python3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN uv pip install --system \
    matplotlib==3.10.8 \
    polars==1.38.1 \
    pyarrow==23.0.1 \
    requests==2.32.5 \
    seaborn==0.13.2

COPY . ./src

CMD ["python", "-m", "src.data_load"]
