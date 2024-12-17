FROM python:3.10-slim

WORKDIR /app

COPY shared /app/shared
COPY user-service/app /app/app
COPY user-service/requirements.txt .
COPY user-service/.env .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5002"]
