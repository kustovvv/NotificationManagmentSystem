FROM python:3.10-slim

WORKDIR /app

COPY shared /app/shared
COPY notification-service/app /app/app
COPY notification-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5005"]
