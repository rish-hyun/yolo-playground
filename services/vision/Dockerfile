FROM python:3.13.2-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS builder

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base

COPY --from=builder /usr/local /usr/local
COPY --from=common . common/
COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]