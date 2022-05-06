FROM python:3

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app

COPY requirements.txt /app
COPY .env /app

RUN pip install -r requirements.txt

EXPOSE port

COPY src /app/