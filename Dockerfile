FROM python:3.9.18-alpine3.18

WORKDIR /app

RUN pip install pyrogram==2.0.106

COPY . .

CMD ["python", "main.py"]
