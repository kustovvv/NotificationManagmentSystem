FROM python:3.10-slim

WORKDIR /app

COPY shared /app/shared
COPY shared/requirements.txt shared-requirements.txt

COPY product-service/app /app/app
COPY product-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r shared-requirements.txt

EXPOSE 5003

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5003"]
