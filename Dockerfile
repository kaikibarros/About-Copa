FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app


RUN chmod +x start.sh
CMD ["./start.sh"]  