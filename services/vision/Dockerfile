FROM ultralytics/ultralytics:8.3.236-python

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.docker.txt requirements.txt
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

COPY --from=common . common/
COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]