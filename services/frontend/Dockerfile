FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

COPY --from=common . common/
COPY app/ .

CMD ["streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0"]